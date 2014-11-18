# -*-coding:Utf-8 -*

# Copyright (c) 2013 LE GOFF Vincent
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the copyright holder nor the names of its contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant la classe Equipage, détaillée plus bas."""

from random import choice

from vector import Vector

from abstraits.obase import BaseObj
from primaires.format.fonctions import supprimer_accents
from primaires.joueur.joueur import Joueur
from primaires.vehicule.vecteur import get_direction
from secondaires.navigation.equipage.configuration import Configuration
import secondaires.navigation.equipage.controles
from secondaires.navigation.equipage.controle import controles
from secondaires.navigation.equipage.ordre import ordres
from secondaires.navigation.equipage.matelot import Matelot
from secondaires.navigation.equipage.noms import NOMS_MATELOTS
from secondaires.navigation.equipage.postes.hierarchie import HIERARCHIE
from secondaires.navigation.equipage.volonte import volontes
from secondaires.navigation.equipage.volontes import *

class Equipage(BaseObj):

    """Classe représentant l'équipage d'un navire.

    Un équipage est le lien entre un navire et une liste de mâtelots.
    Il permet d'exécuter des ordres directement ou des volontés
    (les volontés sont des ordres décomposés).

    """

    noms_controles = {
            "cap": "direction",
            "vitesse": "vitesse",
    }

    def __init__(self, navire):
        """Constructeur du matelot."""
        BaseObj.__init__(self)
        self.navire = navire
        self.matelots = {}
        self.joueurs = {}

        # Volontés
        self.volontes = []

        # Caps choisis
        self.caps = []
        self.cap = None
        self.destination = None

        # Adversaires
        self.ennemis = []

        # Données de configuration
        self.configuration = Configuration(equipage=self)

        # Contrôles
        self.controles = {}

        self._construire()

    def __getnewargs__(self):
        return (None, )

    def __repr__(self):
        navire = self.navire and self.navire.cle or "aucun"
        return "<Équipage du navire {}>".format(repr(navire))

    @property
    def matelots_libres(self):
        """Retourne les matelots considérés comme libres."""
        matelots = tuple(self.matelots.values())
        return tuple(m for m in matelots if m.personnage and \
                not m.personnage.etats and len(m.ordres) == 0)

    @property
    def opt_destination(self):
        """Retourne le vecteur (Vector) correspondant à la destination.

        Si la destination n'est pas spécifiée, retourne None.

        """
        if self.destination:
            x, y = self.destination
            return Vector(x, y, self.navire.position.z)

        return None

    def get_matelots_ayant_ordre(self, cle_ordre):
        """Retourne la liste des matelots ayant l'ordre précisé."""
        return [m for m in self.matelots.values() if m.get_ordre(cle_ordre)]

    def ajouter_matelot(self, personnage, nom_poste="matelot"):
        """Ajoute un mâtelot à l'équipage."""
        matelot = Matelot(self, personnage)
        matelot.affectation = personnage.salle

        # Cherche le poste par défaut défini dans la fiche
        fiche = importeur.navigation.fiches.get(getattr(personnage, "cle", ""))
        if fiche:
            nom_poste = fiche.poste_defaut

        matelot.nom_poste = nom_poste
        matelot.nom = self.trouver_nom_matelot()
        self.matelots[supprimer_accents(matelot.nom.lower())] = matelot
        importeur.navigation.matelots[personnage.identifiant] = matelot
        return matelot

    def renommer_matelot(self, matelot, nouveau_nom):
        """Renomme un matelot."""
        del self.matelots[supprimer_accents(matelot.nom).lower()]
        matelot.nom = nouveau_nom
        self.matelots[supprimer_accents(matelot.nom.lower())] = matelot

    def changer_poste(self, personnage, poste):
        """Change le poste du matelot désigné.

        Si le matelot est un joueur, modifie juste le dictionnaire
        'joueurs'. Les joueurs ont leur libre arbitre sur l'équipage
        mais ils peuvent avoir des privilèges. Si c'est un personnage
        au contraire, recherche le matelot derrière et change son
        poste.

        """
        if isinstance(personnage, Joueur):
            self.joueurs[personnage] = poste
        else:
            matelot = self.get_matelot_depuis_personnage(personnage)
            if matelot is None:
                raise ValueError("Le matelot derrière le personnage " \
                        "{} est introuvable".format(personnage))

            matelot.nom_poste = poste

    def trouver_nom_matelot(self):
        """Trouve un nom de mâtelot non utilisé."""
        noms = [matelot.nom for matelot in self.matelots.values()]
        noms_disponibles = [nom for nom in NOMS_MATELOTS if nom not in noms]
        return choice(noms_disponibles)

    def supprimer_matelot(self, nom):
        """Supprime, si trouvé, le matelot depuis son nom."""
        nom = supprimer_accents(nom).lower()
        matelot = self.matelots[nom]
        identifiant = matelot.personnage and matelot.personnage.identifiant \
                or ""
        if identifiant in importeur.navigation.matelots:
            del importeur.navigation.matelots[identifiant]
        matelot.detruire()
        del self.matelots[nom]

    def ordonner_matelot(self, nom, ordre, *args, executer=False):
        """Ordonne à un mâtelot en particulier.

        Le mâtelot est trouvé en fonction de son nom. Si le nom est trouvé
        dans l'équipage, alors cherche l'ordre.

        L'ordre est un nom d'ordre également. Les paramètres optionnels
        sont transmis au constructeur de l'ordre.

        """
        matelot = self.get_matelot(nom)
        classe_ordre = ordres[ordre]
        ordre = classe_ordre(matelot, self.navire, *args)
        matelot.ordonner(ordre)
        if executer:
            matelot.executer_ordres()

        return ordre

    def ajouter_ennemi(self, ennemi):
        """Ajoute un navire ennemi dans la liste des ennemis."""
        if ennemi is self:
            return

        commandants = self.get_matelots_au_poste("commandant", libre=False)
        if commandants and ennemi not in self.ennemis:
            self.ennemis.append(ennemi)

    def demander(self, cle_volonte, *parametres, personnage=None,
            exception=None):
        """Exécute une volonté."""
        volonte = volontes[cle_volonte]
        volonte = volonte(self.navire, *parametres)
        if personnage:
            volonte.crier_ordres(personnage)

        self.executer_volonte(volonte, exception=exception)

    def executer_volonte(self, volonte, exception=None):
        """Exécute une volonté déjà créée."""
        self.volontes.append(volonte)
        Matelot.logger.debug("Demande de {}".format(volonte))
        retour = volonte.choisir_matelots(exception=exception)
        volonte.executer(retour)

    def controler(self, cle, *args):
        """Définit un nouveau contrôle.

        Le premier paramètre est la clé du contrôle (par exemple
        'direction'). Les paramètres optionnels sont passés au contrôle
        pour l'initialisation. La décomposition du contrôle (en volontés)
        est appelée immédiatement.

        """
        controle = controles.get(cle)
        if controle is None:
            raise ValueError("Aucun contrôle de clé {}".format(repr(cle)))

        controle = controle(self, *args)
        self.controles[cle] = controle
        Matelot.logger.debug("Création du contrôle {}".format(controle))
        controle.decomposer()
        return controle

    def retirer_controle(self, cle):
        """Retire le contrôle si existant.

        Le seul paramètre à préciser est la clé du contrôle.

        """
        if cle in self.controles:
            del self.controles[cle]

    def get_matelot(self, nom):
        """Retourne, si trouvé, le âtelot recherché.

        Si le mâtelot ne peut être trouvé, lève une exception KeyError.

        """
        nom = supprimer_accents(nom).lower()
        if nom not in self.matelots:
            raise KeyError("matelot {} introuvable".format(repr(nom)))

        return self.matelots[nom]

    def get_matelot_depuis_personnage(self, personnage):
        """Retourne le matelot correspondant au personnage ou None."""
        for matelot in self.matelots.values():
            if matelot.personnage is personnage:
                return matelot

        return None

    def get_matelots_au_poste(self, nom_poste, libre=True,
            endurance_min=None, exception=None):
        """Retourne les matelots au poste indiqué.

        Cette méthode retourne toujours une liste, bien que cette
        liste puisse être vide. Le nom de poste est l'un de ceux
        définis dans postes/hierarchie.py. Certains postes sont des
        noms standards dans la hiérarchie des postes (comme 'maître
        d'équipage'), certains sont des noms englobant plusieurs
        postes. Par exemple, si on demande les cannoniers d'un navire,
        on obteint toujours les matelots au poste de 'matelot' tout
        simplement. Les cannoniers sont les premiers à être retournés
        mais les matelots standards (c'est-à-dire ceux qui ne sont pas
        considérés avec une affectation très spécifique) sont retournés
        ensuite.

        Paramètres à préciser :
            nom_poste -- le nom du poste (par exemple "maître d'équipage")
            libre -- le matelot est-il libre (sans ordre ni état)
            endurance_min -- l'endurance minimum que doit avoir le personnage
            exception -- le matelot qui ne fera pas parti des choix

        """
        noms_poste = HIERARCHIE[nom_poste]
        matelots = []
        for matelot in self.matelots.values():
            if matelot is exception:
                continue

            if matelot.nom_poste in noms_poste:
                matelots.append(matelot)

        matelots.sort(key=lambda m: noms_poste.index(m.nom_poste))
        if libre:
            matelots = [m for m in matelots if \
                    not m.personnage.etats and len(m.ordres) == 0]
        if endurance_min is not None:
            matelots = [m for m in matelots if \
                    m.personnage.endurance >= endurance_min]

        return matelots

    def get_matelots_libres(self, exception):
        """Retourne les matelots libres."""
        matelots = self.matelots_libres
        return [m for m in matelots if m is not exception]

    def est_au_poste(self, personnage, nom_poste):
        """Retourne True si le matelot est au poste.

        À la différence de 'get_matelots_au_poste', cette méthode
        cherche aussi dans les joueurs.

        """
        noms_poste = HIERARCHIE[nom_poste]
        matelot = self.get_matelot_depuis_personnage(personnage)
        if matelot is not None:
            return matelot.nom_poste in noms_poste
        elif personnage in self.joueurs:
            return self.joueurs[personnage] in noms_poste

        return False

    def ajouter_trajet(self, trajet):
        """Ajoute le trajet à la liste des caps."""
        self.caps.append(trajet.cle)
        if len(self.caps) == 1:
            self.destination = trajet.point_depart

    def verifier_matelots(self):
        """Retire les matelots inexistants ou morts."""
        for cle, matelot in tuple(self.matelots.items()):
            if matelot.personnage is None or matelot.personnage.est_mort():
                del self.matelots[cle]

    def tick(self):
        """L'équipage se tick à chaque seconde.

        Cette méthode est appelée régulièrement pour les navires
        ayant un équipage (à chaque seconde, en fait). Elle permet
        d'effectuer des actions semi-automatiques (réparer la coque
        si il y a des voies d'eau, écoper si il y a du poids d'eau à
        bord) ou plus complexes (suivre un cap, couler un navire ennemi,
        réagir aux potentiels offensifs des autres). Les premirèes
        actions ne nécessitent aucun arrangement particulier : si il
        y a besoin, les actions sont accomplies par l'équipage. Les
        dernirèes nécessitent une autorité (un capitaine PNJ, second,
        maître d'équipage ou, si tout le monde est à l'eau, un officier
        suffira à assurer le commandement).

        Cette méthode est un point important d'optimisation. Ne pas
        oublier qu'elle est appelée souvent et sur potentiellement
        beaucoup de navires.

        """
        # Retire les matelots morts
        self.verifier_matelots()

        # Si le navire n'es tpas bien orienté face au vent, change
        # l'orientation de ces voiles
        self.orienter_voiles()

        # Si le navire est endommagé, envoie les charpentiers
        self.ordonner_reparations()

        # Si le navire est attaqué
        self.ordonner_attaque()

        commandants = self.get_matelots_au_poste("capitaine", False)
        if not self.destination:
            return

        if commandants:
            commandant = commandants[0]
            self.verifier_cap(commandant)

    def verifier_cap(self, commandant):
        """Vérifie le cap du navire.

        La direction du navire doit être (à peu près) celle nécessaire
        pour atteindre le point de destination (self.point). Si c'est
        le cas et que la distance au point est inférieure à une distance
        préétablie, le commandant prépare son équipage pour le point
        suivant.

        Si le cap nécessite une correction, il l'a fait ici aussi.

        """
        destination = self.opt_destination
        position = self.navire.opt_position
        distance = destination - position
        direction = get_direction(distance)
        ar_direction = round(direction / 3) * 3
        if self.cap:
            ar_cap = round(self.cap / 3) * 3

        if self.caps and distance.mag <= 2:
            # On cherche le point suivant sur la carte
            cle = self.caps[0]
            trajet = importeur.navigation.trajets[cle]
            suivant = trajet.points.get(self.destination)
            if suivant is None and len(self.caps) > 1:
                del self.caps[0]
                cle = self.caps[0]
                trajet = importeur.navigation.trajets[cle]
                suivant = trajet.point_depart
            self.destination = suivant

        if self.cap is None or ar_cap != ar_direction:
            # On change de cap
            self.demander("virer", round(direction),
                    personnage=commandant.personnage)
            self.cap = direction

    def orienter_voiles(self):
        """Oriente les voiles si nécessaire."""
        navire = self.navire
        vent = navire.vent
        voiles = navire.voiles
        voiles = [v for v in voiles if v.hissee]
        if not voiles:
            return

        facteur = sum(v.facteur_orientation(navire, vent) for v in voiles)
        facteur = facteur / len(voiles)
        if facteur < 0.85:
            self.demander("orienter_voiles")

    def ordonner_reparations(self):
        """Ordonne de faire des réparations si nécessaire."""
        salles = self.navire.salles_endommagees
        if salles:
            matelots = self.get_matelots_ayant_ordre("colmater")
            en_cours = [m.get_ordre("colmater").salle for m in matelots]
            for salle in salles:
                if salle in en_cours:
                    continue

                self.demander("colmater", salle)

    def ordonner_attaque(self):
        """Ordonne d'attaquer les navires qui sont dans les ennemis."""
        self.ennemis = [n for n in self.ennemis if n.e_existe]
        for ennemi in self.ennemis:
            self.demander("tirer", ennemi, False)

    def detruire(self):
        """Destruction de l'équipage et des matelots inclus."""
        for matelot in list(self.matelots.values()):
            matelot.detruire()

        BaseObj.detruire(self)

    @staticmethod
    def get_nom_matelot(pnj, personnage):
        """Retourne le nom du matelot si personnage est gradé."""
        matelot = importeur.navigation.matelots.get(pnj.identifiant)
        if matelot and matelot.equipage.est_au_poste(personnage, "officier"):
            return matelot.nom

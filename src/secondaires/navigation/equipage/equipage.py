# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 LE GOFF Vincent
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
from secondaires.navigation.constantes import PCT_XP, get_portee, get_hauteur
from secondaires.navigation.equipage.configuration import Configuration
import secondaires.navigation.equipage.controles
from secondaires.navigation.equipage.controle import controles
import secondaires.navigation.equipage.objectifs
from secondaires.navigation.equipage.objectif import objectifs
from secondaires.navigation.equipage.ordre import ordres
from secondaires.navigation.equipage.matelot import Matelot
from secondaires.navigation.equipage.noms import NOMS_MATELOTS
from secondaires.navigation.equipage.postes.hierarchie import HIERARCHIE
from secondaires.navigation.equipage.volonte import volontes
from secondaires.navigation.equipage.volontes import *
from secondaires.navigation.visible import Visible

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

        # Objectifs
        self.objectifs = []

        # Points observés pour la vigie
        self.vigie_terres = []
        self.vigie_navires = []
        self.vigie_tries = {}

        # Stratégie temporaire
        self.pirate = False

        # Points de poste
        self.points_max = 0

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

    @property
    def points_actuels(self):
        """Retourne la somme des points actuels des matelots.

        Chaque matelot, en fonction de son poste, a des points. Le
        total forme un nombre qui est comparé au nombre de points
        actuels en cas d'abordage. Par exemple, si l'équipage comprend
        un capitaine (qui vaut 10 points) et un matelot (qui en
        vaut 1), le total est 11. Si le capitaine est tué, le nombre
        de points actuels est 1 (il ne reste que le matelot). En
        fonction de la différence entre points au total et points
        actuels, on considère un navire comme capturable ou non.

        """
        return sum(m.poste.points for m in self.matelots.values())

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

        # Modifie le nombre de points
        self.points_max = self.points_actuels

        return matelot

    def est_matelot(self, personnage):
        """Retourne True si le personnage précisé est un matelot de l'équipage.

        Le personnage peut être soit un PNJ soit un joueur. Le
        propriétaire du navire est automatiquement considéré comme
        étant matelot de l'équipage.

        """
        navire = self.navire
        personnages = [m.personnage for m in self.matelots.values()]
        personnages.extend(list(self.joueurs.keys()))

        if navire.proprietaire:
            personnages.append(navire.proprietaire)

        return personnage in personnages

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

    def supprimer_matelot(self, nom, recalculer=True):
        """Supprime, si trouvé, le matelot depuis son nom.

        Si 'recalculer' est à True, recalcule le nombre de points
        maximum de l'équipage.

        """
        nom = supprimer_accents(nom).lower()
        matelot = self.matelots[nom]
        identifiant = matelot.personnage and matelot.personnage.identifiant \
                or ""
        if identifiant in importeur.navigation.matelots:
            del importeur.navigation.matelots[identifiant]
        matelot.detruire()
        del self.matelots[nom]

        if recalculer:
            # On recalcule le point max
            self.points_max = self.points_actuels

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

        if ennemi not in self.ennemis:
            self.ennemis.append(ennemi)

    def demander(self, cle_volonte, *parametres, personnage=None,
            exception=None):
        """Exécute une volonté."""
        volonte = volontes[cle_volonte]
        volonte = volonte(self.navire, *parametres)
        if personnage:
            volonte.initiateur = personnage
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

    def a_objectif(self, cle, *args):
        """Vérifie que l'équipage n'a pas déjà cet objectif."""
        for objectif in self.objectifs:
            t_args = tuple(objectif.arguments[:len(args)])
            if objectif.cle == cle and args == t_args:
                return True

        return False

    def ajouter_objectif(self, cle, *args):
        """Ajoute l'objectif dont la clé est spécifié.

        Les paramètres suplémentaires sont envoyés au constructeur
        de l'objectif.

        """
        objectif = objectifs.get(cle)
        if objectif is None:
            raise ValueError("Aucun objectif de clé {}".format(repr(cle)))

        objectif = objectif(self, *args)
        self.objectifs.insert(0, objectif)
        Matelot.logger.debug("Création de l'objectif {}".format(objectif))
        objectif.creer()
        return objectif

    def retirer_objectif(self, indice):
        """Retire l'objectif d'indice spécifié."""
        del self.objectifs[indice]

    def get_matelot(self, nom):
        """Retourne, si trouvé, le mâtelot recherché.

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
            endurance_min=None, exception=None, joueurs=False):
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
            joueurs -- doit-on inclure les matelots joueurs ?

        Si 'joueurs' est à True, retourne une liste de personnages
        (les joueurs ne sont pas liés à des matelots par défaut).

        """
        noms_poste = HIERARCHIE[nom_poste]
        matelots = []
        for matelot in self.matelots.values():
            if matelot is exception:
                continue

            if matelot.nom_poste in noms_poste:
                matelots.append(matelot)

        matelots.sort(key=lambda m: m.personnage.endurance, reverse=True)
        matelots.sort(key=lambda m: noms_poste.index(m.nom_poste))
        if libre:
            matelots = [m for m in matelots if \
                    not m.personnage.etats and len(m.ordres) == 0]
        if endurance_min is not None:
            matelots = [m for m in matelots if \
                    m.personnage.endurance >= endurance_min]

        if joueurs:
            matelots = [m.personnage for m in matelots]
            for joueur, poste in self.joueurs.items():
                if poste in noms_poste:
                    matelots.insert(0, joueur)

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
            self.destination = list(trajet.points.values())[0]
        commandants = self.get_matelots_au_poste("commandant", False)
        if commandants and not self.objectifs:
            self.ajouter_objectif("suivre_cap", 1.5)

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
        # Si le navire n'es tpas bien orienté face au vent, change
        # l'orientation de ces voiles
        self.orienter_voiles()

        # Si le navire est endommagé, envoie les charpentiers
        self.ordonner_reparations()

    def verifier_vigie(self):
        """Vérifie les vigies pour détecter les terres et navires.

        Il y a des règles strictes pour avertir des nouveaux points :
            * Pour les terres, on annonce la première qu'on voit si on
              ne voyait rien avant
            * Pour les navires, on annonce tous ceux qui apparaissent
              et n'avaient pas été signalés

        """
        navire = self.navire

        # Si le navire est immobilisé, la vigie n'est pas active
        if navire.immobilise:
            return

        vigies = self.get_matelots_au_poste("vigie")
        if not vigies:
            return

        vigie = vigies[0]
        personnage = vigie.personnage
        distinction = personnage.distinction_audible
        salle = personnage.salle
        portee = get_portee(salle)
        points = Visible.observer(personnage, portee, 5,
                {"": navire})

        tries = points.get_tries()
        self.vigie_tries = tries

        # D'abord on cherche les navires
        navires = tries.get("navire", {})
        for angle, (vecteur, point) in navires.items():
            if point.immobilise:
                continue

            if point in self.vigie_navires:
                continue

            navire.envoyer(distinction + get_hauteur(angle,
                    " s'écrie : navire en vue ! Navire {direction} !"))
            self.vigie_navires.append(point)

            # Pour l'instant on fait le branchement conditionnel ici
            if self.pirate:
                self.ajouter_objectif("rejoindre_et_couler", point)

            break

        # Ensuite, on cheerche les obstacles
        obstacles = tries.get("obstacle", {}).copy()
        obstacles.update(tries.get("salle", {}))
        obstacles.update(tries.get("sallenavire", {}))
        obstacles.update(tries.get("repere", {}))

        if not self.vigie_terres and obstacles:
            # Il n'y avait rien en vu auparavant
            angle, (vecteur, point) = tuple(obstacles.items())[0]
            navire.envoyer(distinction + get_hauteur(angle,
                    " s'écrie : terre ! Terre {direction} !"))

        self.vigie_terres = [p for a, (v, p) in obstacles.items()]

    def orienter_voiles(self):
        """Oriente les voiles si nécessaire."""
        navire = self.navire
        vent = navire.vent
        voiles = navire.voiles
        voiles = [v for v in voiles if v.hissee]
        if navire.nom_allure == "vent debout":
            return

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

    def get_canons_libres(self):
        """Retourne les canons libres du navire."""
        canons = []
        matelots = self.get_matelots_ayant_ordre("charger_boulet")
        utilises = [m.get_ordre("charger_boulet").canon for m in matelots]
        for salle in self.navire.salles.values():
            canon = salle.get_element("canon")
            if canon and canon not in utilises:
                canons.append(canon)

        return canons

    def recompenser_ennemis(self):
        """Cette méthode récompense les navires ennemis.

        Elle est souvent appelée quand le navire sombre.

        """
        navire = self.navire
        xp = importeur.perso.gen_niveaux.grille_xp[navire.modele.niveau][1]
        xp = xp * PCT_XP / 100

        # On ne prend en compte que les navires proches
        ennemis = [n for n in self.ennemis if (n.opt_position - \
                navire.opt_position).mag < 30]

        # Maintenant on récompense en proportion de la distance
        for ennemi in ennemis:
            distance = (ennemi.opt_position - navire.opt_position).mag
            facteur = (30 - distance) / (len(ennemis) * 30)
            don = xp * facteur
            personnages = ennemi.personnages
            don = int(xp / len(personnages))
            if don > 0:
                for personnage in personnages:
                    personnage.gagner_xp("navigation", xp)

    def reagir_collision(self, salle, contre):
        """Réagit à une collision.

        Si un objectif est défini, la méthode 'reagir_collision' de
        l'objectif prioritaire (le premier) est appelée. En d'autres
        termes, si le navire est contrôlé par le système, ou par
        le joueur en mode automatique, l'équipage va essayer de
        réagir face à une collision (en reculant, par exemple, si
        cela est possible, ou tout au moins en interrompant la
        vitesse).

        """
        if self.objectifs:
            self.objectifs[0].reagir_collision(salle, contre)

    def detruire(self):
        """Destruction de l'équipage et des matelots inclus."""
        for nom in list(self.matelots.keys()):
            self.supprimer_matelot(nom)

        BaseObj.detruire(self)

    @staticmethod
    def get_nom_matelot(pnj, personnage):
        """Retourne le nom du matelot si personnage est gradé."""
        matelot = importeur.navigation.matelots.get(pnj.identifiant)
        navire = getattr(matelot, "navire", None)
        proprietaire = getattr(navire, "proprietaire", None)
        if matelot and (matelot.equipage.est_au_poste(personnage,
                "officier") or personnage is proprietaire):
            return matelot.nom

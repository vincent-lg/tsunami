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
from primaires.vehicule.vecteur import get_direction
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

    def __init__(self, navire):
        """Constructeur du matelot."""
        BaseObj.__init__(self)
        self.navire = navire
        self.matelots = {}

        # Caps choisis
        self.caps = []
        self.cap = None
        self.destination = None

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
        return tuple(m for m in matelots if m.personnage.cle_etat == "" and \
                len(m.ordres) == 0)

    @property
    def opt_destination(self):
        """Retourne le vecteur (Vector) correspondant à la destination.

        Si la destination n'est pas spécifiée, retourne None.

        """
        if self.destination:
            x, y = self.destination
            return Vector(x, y, self.navire.position.z)

        return None

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
        return matelot

    def trouver_nom_matelot(self):
        """Trouve un nom de mâtelot non utilisé."""
        noms = [matelot.nom for matelot in self.matelots.values()]
        noms_disponibles = [nom for nom in NOMS_MATELOTS if nom not in noms]
        return choice(noms_disponibles)

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

    def demander(self, cle_volonte, *parametres, personnage=None):
        """Exécute une volonté."""
        volonte = volontes[cle_volonte]
        volonte = volonte(self.navire, *parametres)
        if personnage:
            volonte.crier_ordres(personnage)

        self.executer_volonte(volonte)

    def executer_volonte(self, volonte):
        """Exécute une volonté déjà créée."""
        Matelot.logger.debug("Demande de {}".format(volonte))
        retour = volonte.choisir_matelots()
        volonte.executer(retour)

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

        return matelot

    def get_matelots_au_poste(self, nom_poste, libre=True,
            endurance_min=None):
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

        """
        noms_poste = HIERARCHIE[nom_poste]
        matelots = []
        for matelot in self.matelots.values():
            if matelot.nom_poste in noms_poste:
                matelots.append(matelot)

        matelots.sort(key=lambda m: noms_poste.index(m.nom_poste))
        if libre:
            matelots = [m for m in matelots if \
                    m.personnage.cle_etat == "" and len(m.ordres) == 0]
        if endurance_min is not None:
            matelots = [m for m in matelots if \
                    m.personnage.endurance <= endurance_min]

        return matelots

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
        if not self.destination:
            return

        commandants = self.get_matelots_au_poste("capitaine", False)
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

        if self.cap is None or ar_cap != ar_direction:
            # On change de cap
            print("Le cap actuel", self.cap, "!=", direction, "pour", destination)
            self.demander("virer", round(direction),
                    personnage=commandant.personnage)
            self.cap = direction

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


"""Fichier contenant la volonté Tirer."""

import re

from vector import Vector

from primaires.format.fonctions import contient
from primaires.vehicule.vecteur import get_direction
from secondaires.navigation.constantes import get_portee
from secondaires.navigation.equipage.ordres.charger_boulet import ChargerBoulet
from secondaires.navigation.equipage.ordres.charger_poudre import ChargerPoudre
from secondaires.navigation.equipage.ordres.feu import Feu
from secondaires.navigation.equipage.ordres.long_deplacer import LongDeplacer
from secondaires.navigation.equipage.ordres.viser import Viser
from secondaires.navigation.equipage.volonte import Volonte
from secondaires.navigation.visible import Visible

class Tirer(Volonte):

    """Classe représentant une volonté.

    Cette volonté choisit un matelot pour, si besoin, se déplacer
    dans la salle d'un canon, le charger (en poudre et boulet), viser un
    navire adverse et tirer.

    """

    cle = "tirer"
    ordre_court = re.compile(r"^t\s+(.*)$", re.I)
    ordre_long = re.compile(r"^tirer\s+(.*)$", re.I)
    def __init__(self, navire, adverse=None, bruyant=True):
        """Construit une volonté."""
        Volonte.__init__(self, navire)
        self.adverse = adverse
        self.bruyant = bruyant

    @property
    def arguments(self):
        """Propriété à redéfinir si la volonté comprend des arguments."""
        return (self.adverse, self.bruyant)

    def trouver_canon(self, adverse):
        """Trouve le canon qui peut pointer vers adverse."""
        centre = adverse.salles.get((0, 0, 0))
        equipage = self.navire.equipage
        canons = equipage.get_canons_libres()
        vec_adverse = Vector(*centre.coords.tuple())
        nav_direction = self.navire.direction.direction
        for canon in canons:
            salle = canon.parent
            vecteur = Vector(*salle.coords.tuple())
            distance = vec_adverse - vecteur
            direction = get_direction(distance)
            direction = (direction - nav_direction) % 360
            if salle.sabord_oriente(direction):
                return canon

        return None

    def choisir_matelots(self, exception=None):
        """Retourne le matelot le plus apte à accomplir la volonté."""
        navire = self.navire
        equipage = navire.equipage
        canon = self.trouver_canon(self.adverse)
        if canon is None:
            return None

        proches = []
        matelots = equipage.get_matelots_au_poste("artilleur",
                exception=exception)
        graph = self.navire.graph
        for matelot in matelots:
            origine = matelot.salle.mnemonic
            destination = canon.parent.mnemonic
            if origine == destination:
                proches.append((matelot, [], canon))
            else:
                chemin = graph.get((origine, destination))
                if chemin:
                    proches.append((matelot, chemin, canon))

        proches = sorted([couple for couple in proches],
                key=lambda couple: len(couple[1]))
        if proches:
            return proches[0]

        return None

    def executer(self, couple):
        """Exécute la volonté."""
        if couple is None:
            self.terminer()
            return

        navire = self.navire
        adverse = self.adverse
        matelot, sorties, canon = couple
        personnage = matelot.personnage
        ordres = []
        if sorties:
            aller = LongDeplacer(matelot, navire, *sorties)
            ordres.append(aller)

        if canon.onces == 0:
            charger_poudre = ChargerPoudre(matelot, navire, canon,
                    self.bruyant)
            ordres.append(charger_poudre)

        if canon.projectile is None:
            charger_boulet = ChargerBoulet(matelot, navire, canon,
                    self.bruyant)
            ordres.append(charger_boulet)

        viser = Viser(matelot, navire, canon, adverse, self.bruyant)
        ordres.append(viser)

        feu = Feu(matelot, navire, canon, self.bruyant)
        ordres.append(feu)
        self.ajouter_ordres(matelot, ordres)

    def crier_ordres(self, personnage):
        """On fait crier l'ordre au personnage."""
        adverse = self.adverse
        msg = "{} s'écrie : un boulet sur {} !".format(
                personnage.distinction_audible, adverse.desc_survol)
        self.navire.envoyer(msg)

    @classmethod
    def extraire_arguments(cls, navire, nom_navire):
        """Extrait les arguments de la volonté."""
        for navire in cls.trouver_navires(navire):
            if contient(navire.desc_survol, nom_navire):
                return (navire, )

        raise ValueError("Le navire {} n'est pas en vue.".format(
                nom_navire))

    @staticmethod
    def trouver_navires(navire):
        """Trouve les navires autour de navire."""
        # On recherche d'abord le personnage
        equipage = navire.equipage
        vigies = equipage.get_matelots_au_poste("vigie")
        if vigies:
            personnage = vigies[0]
        else:
            personnage = navire.personnages[0]

        portee = get_portee(personnage.salle)
        points = Visible.observer(personnage, portee, 5,
                {"": navire})
        navires = [p[1] for p in points.points.values() if \
                isinstance(p[1], type(navire))]
        return navires

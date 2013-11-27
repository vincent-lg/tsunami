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


"""Fichier contenant la volonté Virer."""

import re

from corps.fonctions import lisser
from secondaires.navigation.equipage.ordres.long_deplacer import LongDeplacer
from secondaires.navigation.equipage.ordres.relacher_gouvernail import \
        RelacherGouvernail
from secondaires.navigation.equipage.ordres.tenir_gouvernail import \
        TenirGouvernail
from secondaires.navigation.equipage.ordres.virer import Virer as OrdreVirer
from secondaires.navigation.equipage.volonte import Volonte

class Virer(Volonte):

    """Classe représentant une volonté.

    Cette volonté choisit un matelot pour, si besoin, se déplacer
    dans la salle du gouvernail, le prendre en main et lui demander de
    virer (soit sur bâbord soit sur tribord, en fonction de la direction
    actuelle du navire).

    """

    cle = "virer"
    ordre_court = re.compile(r"^v([0-9]{1,3})$", re.I)
    ordre_long = re.compile(r"^virer\s+([0-9]{1,3})$", re.I)
    def __init__(self, navire, direction=0):
        """Construit une volonté."""
        Volonte.__init__(self, navire)
        self.direction = direction

    @property
    def arguments(self):
        """Propriété à redéfinir si la volonté comprend des arguments."""
        return (self.direction, )

    def choisir_matelots(self):
        """Retourne le matelot le plus apte à accomplir la volonté."""
        navire = self.navire
        equipage = navire.equipage
        gouvernail = self.navire.gouvernail
        if gouvernail is None:
            return None

        personnage = gouvernail.tenu
        matelot = equipage.get_matelot_depuis_personnage(personnage)
        if gouvernail.tenu:
            return (matelot, [])

        proches = []
        matelots = equipage.get_matelots_au_poste("officier")
        graph = self.navire.graph
        gouvernail = navire.gouvernail
        for matelot in matelots:
            origine = matelot.salle.mnemonic
            destination = gouvernail.parent.mnemonic
            if origine == destination:
                proches.append((matelot, []))
            else:
                chemin = graph.get((origine, destination))
                if chemin:
                    proches.append((matelot, chemin))

        proches = sorted([couple for couple in proches],
                key=lambda couple: len(couple[1]))
        if proches:
            return proches[0]

        return None

    def executer(self, couple):
        """Exécute la volonté."""
        if couple is None:
            return

        gouvernail = self.navire.gouvernail
        if gouvernail.tenu:
            ordre = couple[0].get_ordre("virer")
            if ordre:
                ordre.direction = self.direction
                return

        matelot, sorties = couple
        personnage = matelot.personnage
        relacher = False
        navire = self.navire
        direction = self.direction
        nav_direction = navire.direction.direction
        ordres = []
        if sorties:
            aller = LongDeplacer(matelot, navire, *sorties)
            aller.volonte = self
            ordres.append(aller)

        if gouvernail.tenu is not personnage:
            relacher = True
            tenir = TenirGouvernail(matelot, navire)
            tenir.volonte = self
            ordres.append(tenir)

        virer = OrdreVirer(matelot, navire, direction)
        virer.volonte = self
        ordres.append(virer)

        if relacher:
            relacher = RelacherGouvernail(matelot, navire)
            relacher.volonte = self
            ordres.append(relacher)
            ordres.append(self.revenir_affectation(matelot))

        for ordre in ordres:
            if ordre:
                matelot.ordonner(ordre)

        matelot.executer_ordres()

    def crier_ordres(self, personnage):
        """On fait crier l'ordre au personnage."""
        direction = self.direction
        if direction < 23 or direction > 337:
            nom_dir = "l'est"
        elif direction < 67:
            nom_dir = "le sud-est"
        elif direction < 112:
            nom_dir = "le sud"
        elif direction < 157:
            nom_dir = "le sud-ouest"
        elif direction < 202:
            nom_dir = "l'ouest"
        elif direction < 247:
            nom_dir = "le nord-ouest"
        elif direction < 292:
            nom_dir = "le nord"
        else:
            nom_dir = "le nord-est"

        direction = (direction + 90) % 360
        nom_dir = lisser("virez à " + nom_dir)
        msg = "{} s'écrie : {}, {}° !".format(
                personnage.distinction_audible, nom_dir, direction)
        self.navire.envoyer(msg)

    @classmethod
    def extraire_arguments(cls, navire, direction):
        """Extrait les arguments de la volonté."""
        direction = (int(direction) - 90) % 360
        return (direction, )

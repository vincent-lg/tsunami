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


"""Fichier contenant la volonté Colmater."""

import re

from secondaires.navigation.equipage.ordres.colmater import Colmater as \
        OrdreColmater
from secondaires.navigation.equipage.ordres.ecoper import Ecoper
from secondaires.navigation.equipage.ordres.long_deplacer import LongDeplacer
from secondaires.navigation.equipage.volonte import Volonte

class Colmater(Volonte):

    """Classe représentant une volonté.

    Cette volonté choisit un matelot pour, si besoin, se déplacer
    dans la salle cible, écoper et colmater la brèche, avant de
    revenir au point de départ.

    """

    cle = "colmater"
    ordre_court = None
    ordre_long = None
    def __init__(self, navire, salle):
        """Construit une volonté."""
        Volonte.__init__(self, navire)
        self.salle = salle

    def choisir_matelots(self):
        """Retourne le matelot le plus apte à accomplir la volonté."""
        navire = self.navire
        salle = self.salle
        equipage = navire.equipage
        proches = []
        matelots = equipage.get_matelots_au_poste("charpentier")
        graph = self.navire.graph
        for matelot in matelots:
            origine = matelot.salle.mnemonic
            destination = salle.mnemonic
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

        matelot, sorties = couple
        personnage = matelot.personnage
        navire = self.navire
        salle = self.salle
        ordres = []
        if sorties:
            aller = LongDeplacer(matelot, navire, *sorties)
            aller.volonte = self
            ordres.append(aller)

        ecoper = Ecoper(matelot, navire, salle)
        ecoper.volonte = self
        ordres.append(ecoper)

        colmater = OrdreColmater(matelot, navire, salle)
        colmater.volonte = self
        ordres.append(colmater)

        for ordre in ordres:
            if ordre:
                matelot.ordonner(ordre)

        matelot.executer_ordres()

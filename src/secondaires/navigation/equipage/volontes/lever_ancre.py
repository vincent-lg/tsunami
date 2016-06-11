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


"""Fichier contenant la volonté LeverAncre"""

import re

from secondaires.navigation.equipage.ordres.lever_ancre import LeverAncre as \
        Ordre
from secondaires.navigation.equipage.ordres.long_deplacer import LongDeplacer
from secondaires.navigation.equipage.volonte import Volonte

class LeverAncre(Volonte):

    """Classe représentant une volonté.

    Cette volonté choisit un ou plusieurs matelots pour lever une ancre.
    Plusieurs matelots sont nécessaires si l'ancre est lourde.

    """

    cle = "lever_ancre"
    ordre_court = re.compile(r"^la$", re.I)
    ordre_long = re.compile(r"^lever\s+ancre$", re.I)

    def choisir_matelots(self, exception=None):
        """Retourne le matelot le plus apte à accomplir la volonté."""
        proches = []
        navire = self.navire
        matelots = navire.equipage.get_matelots_libres(exception)
        graph = self.navire.graph
        ancre = self.navire.ancre
        if not ancre:
            return

        if not ancre.jetee:
            return

        if navire.passerelle:
            return

        for n in range(ancre.nb_lever):
            proche = []
            for matelot in matelots:
                if matelot in [t[0] for t in proches]:
                    continue

                if matelot.personnage.stats.endurance < 50:
                    continue

                origine = matelot.salle.mnemonic
                destination = ancre.parent.mnemonic
                if origine == destination:
                    proche.append((matelot, [], ancre))
                else:
                    chemin = graph.get((origine, destination))
                    if chemin:
                        proche.append((matelot, chemin, ancre))
            proches.append(min(proche, key=lambda c: len(c[1])))

        proches = proches[:ancre.nb_lever]
        return proches

    def executer(self, proches):
        """Exécute la volonté."""
        if not proches:
            return

        navire = self.navire
        for matelot, sorties, ancre in proches:
            ordres = []
            if sorties:
                aller = LongDeplacer(matelot, navire, *sorties)
                ordres.append(aller)

            lever = Ordre(matelot, navire)
            ordres.append(lever)
            ordres.append(self.revenir_affectation(matelot))
            self.ajouter_ordres(matelot, ordres)


    def crier_ordres(self, personnage):
        """On fait crier l'ordre au personnage."""
        msg = "{} s'écrie : levez l'ancre !".format(personnage.distinction_audible)
        self.navire.envoyer(msg)

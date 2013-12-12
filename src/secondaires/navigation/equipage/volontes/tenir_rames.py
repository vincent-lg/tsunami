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


"""Fichier contenant la volonté TenirRames"""

import re

from secondaires.navigation.equipage.ordres.tenir_rames import \
        TenirRames as OrdreTenirRames
from secondaires.navigation.equipage.ordres.long_deplacer import LongDeplacer
from secondaires.navigation.equipage.volonte import Volonte

class TenirRames(Volonte):

    """Classe représentant une volonté.

    Cette volonté choisit parmi les rameurs pour les affecter aux
    rames du bâtiment.

    """

    cle = "tenir_rames"
    ordre_court = re.compile(r"^tr$", re.I)
    ordre_long = re.compile(r"^tenir\s+rames?$", re.I)
    def choisir_matelots(self):
        """Retourne le matelot le plus apte à accomplir la volonté."""
        objectifs = []
        matelots = self.navire.equipage.get_matelots_au_poste("rameur",
                endurance_min=30)
        graph = self.navire.graph
        rames = self.navire.rames
        rames = [r for r in rames if r.tenu is None]
        for paire in rames:
            proches = []
            destination = paire.parent.mnemonic
            for matelot in matelots:
                origine = matelot.salle.mnemonic
                if origine == destination:
                    proches.append((matelot, [], paire))
                else:
                    chemin = graph.get((origine, destination))
                    if chemin:
                        proches.append((matelot, chemin, paire))

            proches.sort(key=lambda couple: len(couple[1]))
            if proches:
                couple = proches[0]
                matelot = couple[0]
                matelots.remove(matelot)
                objectifs.append(couple)

        return objectifs

    def executer(self, objectifs):
        """Exécute la volonté."""
        print(self, objectifs)
        for sequence in objectifs:
            matelot, sorties, rames = sequence
            navire = self.navire
            ordres = []
            if sorties:
                aller = LongDeplacer(matelot, navire, *sorties)
                aller.volonte = self
                ordres.append(aller)

            tenir = OrdreTenirRames(matelot, navire, rames)
            tenir.volonte = self
            ordres.append(tenir)
            for ordre in ordres:
                if ordre:
                    matelot.ordonner(ordre)

            matelot.executer_ordres()

    def crier_ordres(self, personnage):
        """On fait crier l'ordre au personnage."""
        msg = "{} s'écrie : rameurs, à vos postes !".format(
                personnage.distinction_audible)
        self.navire.envoyer(msg)

    @classmethod
    def extraire_arguments(cls, navire):
        """Extrait les arguments de la volonté."""
        return ()

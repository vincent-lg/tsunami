# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
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


"""Fichier contenant la volonté OrienterVoiles"""

import re

from secondaires.navigation.equipage.ordres.orienter_voile import OrienterVoile
from secondaires.navigation.equipage.ordres.long_deplacer import LongDeplacer
from secondaires.navigation.equipage.volonte import Volonte

class OrienterVoiles(Volonte):

    """Classe représentant une volonté.

    Cette volonté choisit un ou plusieurs matelots pour orienter toutes
    les voiles.

    """

    cle = "orienter_voiles"
    ordre_court = re.compile(r"^ov$", re.I)
    ordre_long = re.compile(r"^orienter\s+voiles?$", re.I)
    def choisir_matelots(self, exception=None):
        """Retourne le matelot le plus apte à accomplir la volonté."""
        proches = []
        matelots = self.navire.equipage.get_matelots_libres(exception)
        graph = self.navire.graph
        voiles = self.navire.voiles
        voiles = [v for v in voiles if v.hissee]
        for voile in voiles:
            proche = []
            for matelot in matelots:
                origine = matelot.salle.mnemonic
                destination = voile.parent.mnemonic
                if origine == destination:
                    proche.append((matelot, [], voile))
                else:
                    chemin = graph.get((origine, destination))
                    if chemin:
                        proche.append((matelot, chemin, voile))

            # Détermine le matelot le plus proche de la voile
            proches.append(min(proche, key=lambda c: len(c[1])))

        return proches

    def executer(self, proches):
        """Exécute la volonté."""
        navire = self.navire
        for matelot, sorties, voile in proches:
            ordres = []
            if sorties:
                aller = LongDeplacer(matelot, navire, *sorties)
                ordres.append(aller)

            orienter = OrienterVoile(matelot, navire)
            ordres.append(orienter)
            ordres.append(self.revenir_affectation(matelot))
            self.ajouter_ordres(matelot, ordres)

    def crier_ordres(self, personnage):
        """On fait crier l'ordre au personnage."""
        msg = "{} s'écrie : orientez les voiles !".format(
                personnage.get_distinction_audible())
        self.navire.envoyer(msg)

    @classmethod
    def extraire_arguments(cls, navire):
        """Extrait les arguments de la volonté."""
        return ()

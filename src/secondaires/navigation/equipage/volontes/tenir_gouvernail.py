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


"""Fichier contenant la volonté TenirGouvernail"""

import re

from secondaires.navigation.equipage.ordres.tenir_gouvernail import \
        TenirGouvernail as OrdreTenirGouvernail
from secondaires.navigation.equipage.ordres.long_deplacer import LongDeplacer
from secondaires.navigation.equipage.volonte import Volonte

class TenirGouvernail(Volonte):

    """Classe représentant une volonté.

    Cette volonté choisit un matelot pour tenir le gouvernail
    du navire.

    """

    cle = "tenir_gouvernail"
    ordre_court = re.compile(r"^tg$", re.I)
    ordre_long = re.compile(r"^tenir\s+gouvernail?$", re.I)
    def choisir_matelots(self, exception=None):
        """Retourne le matelot le plus apte à accomplir la volonté."""
        proches = []
        matelots = self.navire.equipage.get_matelots_libres(exception)
        graph = self.navire.graph
        gouvernail = self.navire.gouvernail
        if gouvernail is None or gouvernail.tenu is not None:
            return None

        for matelot in matelots:
            origine = matelot.salle.mnemonic
            destination = gouvernail.parent.mnemonic
            if origine == destination:
                proches.append((matelot, [], gouvernail))
            else:
                chemin = graph.get((origine, destination))
                if chemin:
                    proches.append((matelot, chemin, gouvernail))

        proches = sorted([couple for couple in proches],
                key=lambda couple: len(couple[1]))
        if proches:
            return proches[0]

        return None

    def executer(self, sequence):
        """Exécute la volonté."""
        if sequence is None:
            self.terminer()
            return

        matelot, sorties, gouvernail = sequence
        navire = self.navire
        ordres = []
        if sorties:
            aller = LongDeplacer(matelot, navire, *sorties)
            ordres.append(aller)

        tenir = OrdreTenirGouvernail(matelot, navire)
        ordres.append(tenir)
        self.ajouter_ordres(matelot, ordres)

    def crier_ordres(self, personnage):
        """On fait crier l'ordre au personnage."""
        msg = "{} s'écrie : un homme à la barre !".format(
                personnage.distinction_audible)
        self.navire.envoyer(msg)

    @classmethod
    def extraire_arguments(cls, navire):
        """Extrait les arguments de la volonté."""
        return ()

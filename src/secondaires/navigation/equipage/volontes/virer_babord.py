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


"""Fichier contenant la volonté VirerBabord."""

import re

from corps.fonctions import lisser
from secondaires.navigation.equipage.ordres.long_deplacer import LongDeplacer
from secondaires.navigation.equipage.ordres.relacher_gouvernail import \
        RelacherGouvernail
from secondaires.navigation.equipage.ordres.tenir_gouvernail import \
        TenirGouvernail
from secondaires.navigation.equipage.ordres.virer import Virer as OrdreVirer
from secondaires.navigation.equipage.volontes.virer import Virer

class VirerBabord(Virer):

    """Classe représentant une volonté.

    Cette volonté choisit un matelot pour, si besoin, se déplacer
    dans la salle du gouvernail, le prendre en main et lui demander de
    virer sur bâbord. Cette volonté utilise donc l'alignement relatif,
    à la différence de 'virer' qui utilise l'alignement absolu.

    """

    cle = "virer_babord"
    ordre_court = re.compile(r"^vb([0-9]{1,3})$", re.I)
    ordre_long = re.compile(r"^virer\s+babord\s+([0-9]{1,3})$", re.I)
    def crier_ordres(self, personnage):
        """On fait crier l'ordre au personnage."""
        direction = int((self.navire.direction.direction - self.direction) % \
                180)
        msg = "{} s'écrie : virez de {}° bâbord !".format(
                personnage.distinction_audible, direction)
        self.navire.envoyer(msg)

    @classmethod
    def extraire_arguments(cls, navire, direction):
        """Extrait les arguments de la volonté."""
        direction = int(direction) % 180
        return ((navire.direction.direction - direction) % 360, )

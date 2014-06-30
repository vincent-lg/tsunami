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


"""Fichier contenant la volonté RelacherGouvernail"""

import re

from secondaires.navigation.equipage.ordres.relacher_gouvernail import \
        RelacherGouvernail as OrdreRelacherGouvernail
from secondaires.navigation.equipage.ordres.long_deplacer import LongDeplacer
from secondaires.navigation.equipage.volonte import Volonte

class RelacherGouvernail(Volonte):

    """Classe représentant une volonté.

    Cette volonté demande simplement au matelot qui tient le gouvernail
    de le relâcher. Comme la plupart des volontés, le matelot est
    encouragé à retourner dans sa salle d'affectation après coup.

    """

    cle = "relacher_gouvernail"
    ordre_court = re.compile(r"^rg$", re.I)
    ordre_long = re.compile(r"^relacher\s+gouvernail?$", re.I)
    def choisir_matelots(self, exception=None):
        """Retourne le matelot le plus apte à accomplir la volonté."""
        navire = self.navire
        equipage = navire.equipage
        gouvernail = self.navire.gouvernail
        if gouvernail is None or gouvernail.tenu is None:
            return None

        personnage = gouvernail.tenu
        matelot = equipage.get_matelot_depuis_personnage(personnage)
        return matelot

    def executer(self, matelot):
        """Exécute la volonté."""
        if matelot is None:
            self.terminer()
            return

        navire = self.navire
        ordres = []
        relacher = OrdreRelacherGouvernail(matelot, navire)
        ordres.append(relacher)
        ordres.append(self.revenir_affectation(matelot))
        self.ajouter_ordres(matelot, ordres)

    def crier_ordres(self, personnage):
        """On fait crier l'ordre au personnage."""
        msg = "{} s'écrie : relâchez la barre !".format(
                personnage.distinction_audible)
        self.navire.envoyer(msg)

    @classmethod
    def extraire_arguments(cls, navire):
        """Extrait les arguments de la volonté."""
        return ()

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


"""Fichier contenant l'ordre RelacherRames."""

from secondaires.navigation.equipage.signaux import *

from ..ordre import *

class RelacherRames(Ordre):

    """Ordre relacher_rames.

    Cet ordre est appelé pour demander à un matelot de relâcher
    les rames qu'il tient.

    """

    cle = "relacher_rames"
    etats_autorises = ("tenir_rames", "")
    peut_deleguer = False

    def __init__(self, matelot, navire, rames=None):
        Ordre.__init__(self, matelot, navire, rames)
        self.rames = rames

    def executer(self):
        """Exécute l'ordre : tient les rames."""
        personnage = self.matelot.personnage
        salle = personnage.salle
        rames = self.rames
        if salle is not rames.parent:
            yield SignalAbandonne("Je ne suis pas dans la salle des rames.")

        if rames.tenu is None:
            yield SignalInutile("ces rames ne sont pas tenues")
        else:
            rames.relacher()
            yield SignalTermine()

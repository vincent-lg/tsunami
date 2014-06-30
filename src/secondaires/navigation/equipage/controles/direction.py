# -*-coding:Utf-8 -*

# Copyright (c) 2014 LE GOFF Vincent
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


"""Fichier contenant le contrôle Direction."""

from math import fabs

from secondaires.navigation.equipage.controle import Controle

class Direction(Controle):

    """Classe représentant le contrôle 'direction'.

    Ce contrôle est en charge de la direction du navire. Si le navire
    est équipé de rames et gouvernail, les deux sont utilisés pour
    contrôler la direction du navire. Malgré tout, le gouvernail a tendance
    à être utilisé pour des tâches de précision alors que les rames
    (sauf si il n'y a pas de gouvernail) ne sont utilisées que pour
    augmenter la rapidité pour virer de bord.

    """

    cle = "direction"
    def __init__(self, equipage, direction):
        Controle.__init__(self, equipage)
        self.direction = direction

    def decomposer(self):
        """Décompose le contrôle en volontés."""
        commandant = self.commandant
        if commandant is None:
            return

        personnage = commandant.personnage
        equipage = self.equipage
        navire = self.navire
        gouvernail = navire.gouvernail
        rames = navire.rames
        actuelle = navire.direction.direction
        objectif = self.direction
        difference = fabs(objectif - actuelle)
        id difference <= 5 and sum(r.direction for r in rames) != 0:
            equipage.demander("ramer", "centre", personnage=personnage)
            return

        if gouvernail:
            equipage.demander("virer_gouvernail", objectif)
        if rames:
            if (gouvernail and difference > 5) or gouvernail is None:

                equipage.demander("ramer", direction, personnage=personnage)

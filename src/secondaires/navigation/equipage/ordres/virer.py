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


"""Fichier contenant l'ordre Virer."""

from secondaires.navigation.equipage.signaux import *

from ..ordre import *

class Virer(Ordre):

    """Ordre virer.

    Cet ordre demande au matelot de faire virer le navire sur bâbord
    ou tribord en fonction du besoin, jusqu'à ce qu'il soit dans une certaine
    direction. Le matelot ciblé doit tenir le gouvernail.

    """

    cle = "virer"
    etats_autorises = ("tenir_gouvernail", )
    def __init__(self, matelot, navire, direction=0):
        Ordre.__init__(self, matelot, navire, direction)
        self.direction = direction

    def executer(self):
        """Exécute l'ordre : vire sur bâbord."""
        navire = self.navire
        matelot = self.matelot
        personnage = matelot.personnage
        salle = personnage.salle
        direction = self.direction
        nav_direction = navire.direction.direction
        if not hasattr(salle, "gouvernail") or salle.gouvernail is None:
            return

        gouvernail = salle.gouvernail
        if gouvernail.tenu is not personnage:
            yield SignalInutile("je ne tiens pas ce gouvernail")
        else:
            par_babord = (nav_direction - direction) % 360
            par_tribord = (direction - nav_direction) % 360
            if par_tribord < par_babord:
                cote = 1
            else:
                cote = -1

            # On change d'inclinaison du gouvernail si nécessaire
            direction_actuelle = round(nav_direction)
            direction_voulue = round(direction)
            diff = (direction_voulue - direction_actuelle) % 360
            if diff > 180:
                diff = 360 - diff

            if diff == 0:
                gouvernail.centrer(personnage)
                yield SignalTermine()
            elif diff < 5:
                orientation = 1
            elif diff < 15:
                orientation = 3
            else:
                orientation = 5

            if gouvernail.orientation != cote * orientation:
                if cote == -1:
                    gouvernail.virer_babord(personnage, orientation, True)
                else:
                    gouvernail.virer_tribord(personnage, orientation, True)

            yield SignalRepete(1)

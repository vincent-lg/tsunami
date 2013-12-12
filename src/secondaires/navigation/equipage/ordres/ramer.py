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


"""Fichier contenant l'ordre Ramer."""

from secondaires.navigation.constantes import VIT_RAMES
from secondaires.navigation.equipage.signaux import *

from ..ordre import *

class Ramer(Ordre):

    """Ordre ramer.

    Cet ordre demande au matelot tenant les rames spécifiées de
    ramer à une vitesse spécifiée. Cet ordre peut être utilisé pour
    demander de s'arrêter de ramer (pas de relâcher les rames).

    """

    cle = "ramer"
    etats_autorises = ("tenir_rames", )

    def __init__(self, matelot, navire, rames=None, vitesse=""):
        Ordre.__init__(self, matelot, navire)
        self.rames = rames
        self.vitesse = vitesse

    def executer(self):
        """Exécute l'ordre : tient les rames."""
        matelot = self.matelot
        personnage = matelot.personnage
        salle = personnage.salle
        rames = self.rames
        vitesse = self.vitesse
        vitesses = tuple(VIT_RAMES.keys()) + ("centre", "gauche", "droite")
        if salle is not rames.parent:
            yield SignalAbandonne("Je ne suis pas dans la salle des rames.")
        elif vitesse not in vitesses:
            yield SignalAbandonne("Je ne connais pas la vitesse {}.".format(
                    vitesse))

        if rames.tenu is not personnage:
            yield SignalAbandonne("Je ne tiens pas ces rames.")
        else:
            if vitesse == "centre":
                rames.centrer()
            elif vitesse == "droite":
                rames.virer_tribord()
            elif vitesse == "gauche":
                rames.virer_babord()
            else:
                rames.changer_vitesse(vitesse)

            while personnage.stats.endurance > 20:
                yield 3

            rames.relacher()
            yield SignalRelais("Je suis trop fatigué.")

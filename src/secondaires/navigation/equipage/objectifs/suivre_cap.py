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


"""Objectif suivre_cap."""

from primaires.vehicule.vecteur import get_direction
from secondaires.navigation.constantes import *
from secondaires.navigation.equipage.objectifs.rejoindre import Rejoindre

# Constantes
DISTANCE_MIN = 3

class SuivreCap(Rejoindre):

    """Objectif suivre_cap.

    Cet objectif, basé sur l'objectif rejoindre, demande à un
    équipage de suivre un cap assigné. Cet objectif est responsable
    de trouver la destination indiquée, la distance qui l'en sépare
    et d'utiliser la vitesse nécssaire, ainsi que de modifier le
    cap si besoin, quand le navire atteint sa destination.

    """

    cle = "suivre_cap"
    def __init__(self, equipage, vitesse_max=None):
        Rejoindre.__init__(self, equipage)
        self.vitesse_max = vitesse_max

    def trouver_cap(self):
        """Trouve le cap (x, y, vitesse).

        Cette méthode trouve le cap tel que renseigné par
        l'équipage.

        """
        equipage = self.equipage
        navire = self.navire
        if equipage.destination:
            self.x, self.y = equipage.destination
            distance = self.get_distance()
            norme = distance.norme
            vitesse = get_vitesse_noeuds(norme)
            if vitesse > self.vitesse_max:
                vitesse = self.vitesse_max
            elif norme < 25:
                vitesse = 0.6
            elif norme < 10:
                vitesse = 0.2

            self.vitesse = vitesse
            direction = round(distance.direction)
            if distance.norme <= DISTANCE_MIN:
                # On cherche le point suivant sur la carte
                cle = equipage.caps[0]
                trajet = importeur.navigation.trajets[cle]
                suivant = trajet.points.get(equipage.destination)
                if suivant is None and len(equipage.caps) > 1:
                    del equipage.caps[0]
                    cle = equipage.caps[0]
                    trajet = importeur.navigation.trajets[cle]
                    suivant = trajet.point_depart
                equipage.destination = suivant

            # On retransmet les contrôles
            Rejoindre.trouver_cap(self)

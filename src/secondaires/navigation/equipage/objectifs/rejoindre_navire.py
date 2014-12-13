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


"""Objectif rejoindre_navire."""

from math import sqrt

from primaires.vehicule.vecteur import get_direction
from secondaires.navigation.constantes import *
from secondaires.navigation.equipage.objectifs.rejoindre import Rejoindre

class RejoindreNavire(Rejoindre):

    """Objectif rejoindre_navire.

    Cet objectif, basé sur l'objectif rejoindre, demande à un
    équipage de suivre navire. Au lieu de rejoindre un point statique,
    cet objectif est responsable de rejoindre un point mouvant en
    essayant de prévoir une interception. Le but de l'objectif est
    d'avoir une distance minimum telle que précisée entre le
    navire actuel et le navire cible.

    """

    cle = "rejoindre_navire"
    def __init__(self, equipage, cible=None, distance_min=1.3):
        Rejoindre.__init__(self, equipage)
        self.cible = cible
        self.distance_min = distance_min

    def trouver_distance_min(self):
        """Trouve la distance minimum.

        Cette distance est fonction de la distance minimum entre
        une salle du navire d'origine et une salle du navire cible.

        """
        navire = self.navire
        etendue = navire.etendue
        altitude = etendue.altitude
        salle_cible = None
        distance = None

        for salle in navire.salles.values():
            if salle.coords.z != altitude:
                continue

            x, y = salle.coords.x, salle.coords.y
            for t_salle in self.cible.salles.values():
                if t_salle.coords.z != altitude:
                    continue

                t_x, t_y = t_salle.coords.x, t_salle.coords.y
                t_distance = sqrt((t_x - x) ** 2 + (t_y - y) ** 2)
                if distance is None or t_distance < distance:
                    distance = t_distance
                    salle_cible = t_salle

        return distance, salle_cible

    def trouver_cap(self):
        """Trouve le cap (x, y, vitesse).

        Cette méthode trouve le cap en se basant sur la cible a
        atteindre et projetant en fonction de sa vitesse.

        """
        equipage = self.equipage
        navire = self.navire
        cible = self.cible
        distance_min = self.distance_min
        distance, salle_cible = self.trouver_distance_min()

        if distance <= distance_min:
            return
        elif distance < 10:
            self.x = salle_cible.coords.x
            self.y = salle_cible.coords.y
            self.vitesse = 0.5
        else:
            vecteur = cible.opt_position + cible.opt_vitesse * 10
            self.x = vecteur.x
            self.y = vecteur.y
            self.vitesse = None

        Rejoindre.trouver_cap(self)

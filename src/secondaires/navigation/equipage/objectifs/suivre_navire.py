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


"""Objectif suivre_navire."""

from secondaires.navigation.constantes import *
from secondaires.navigation.equipage.objectifs.rejoindre import Rejoindre

class SuivreNavire(Rejoindre):

    """Objectif suivre_navire.

    Cet objectif, basé sur l'objectif rejoindre, demande à un
    équipage de suivre un navire. Cet objectif est différent de
    'rejoindre_navire' en ce qu'il essaye de suivre le navire, pas de
    le rejoindre : si il est trop près de la cible, l'équipage reçoit
    l'ordre de s'arrêter. Si il est trop loin, il essaye de le
    rattraper. Sinon, il va s'accorder sur sa vitesse et sa direction.

    """

    cle = "suivre_navire"

    def __init__(self, equipage, cible=None, distance_min=1.3):
        Rejoindre.__init__(self, equipage)
        self.arguments = (cible, )
        self.cible = cible
        self.distance_min = distance_min
        self.autoriser_vitesse_sup = False

        if cible:
            self.x = cible.position.x
            self.y = cible.position.y

    @property
    def actif(self):
        """Retourne True si l'objectif est actif, False sinon."""
        navire = self.navire
        cible = self.cible
        if cible is None or not cible.e_existe:
            return False

        distance = (navire.opt_position - cible.opt_position).mag
        if distance > 200:
            return False

        return True

    def afficher(self):
        """Méthode à redéfinir retournant l'affichage de l'objectif."""
        navire = self.navire
        distance = self.get_distance()
        cible = self.cible
        direction = (distance.direction + 90) % 360
        msg_dist = get_nom_distance(distance)
        return "Suivre {}, cap sur {}° ({}), à {}".format(
                cible.desc_survol, round(direction), distance.nom_direction,
                msg_dist)

    def trouver_cap(self):
        """Trouve le cap (x, y, vitesse).

        Cette méthode trouve le cap en se basant sur la cible a
        atteindre et projetant en fonction de sa vitesse.

        """
        equipage = self.equipage
        navire = self.navire
        cible = self.cible
        self.x = cible.position.x
        self.y = cible.position.y
        distance = self.get_distance()
        norme, salle = self.trouver_distance_min(cible)

        if norme <= self.distance_min:
            self.vitesse = 0
        elif norme < 10:
            self.vitesse = round(cible.vitesse_noeuds, 1)
            if self.vitesse < 0.2:
                self.vitesse = 0.2
        else:
            self.vitesse = None

        Rejoindre.trouver_cap(self)

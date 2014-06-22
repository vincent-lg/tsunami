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


"""Fichier contenant la classe Repere, détaillée plus bas."""

from vector import *

from abstraits.obase import BaseObj
from primaires.format.description import Description
from primaires.vehicule.vecteur import get_direction
from secondaires.navigation.constantes import get_portee
from secondaires.navigation.visible import norme_angle, Visible

class Repere(BaseObj):

    """Classe représentant un repère dans une étendue d'eau.

    Les repères sont des détails généralement visibles à distance, des
    phares, de très hautes montagnes. Ils sont caractérisés par une
    position en 2D (x;y), un amplificateur de portée (qui détermine à quelle
    distance ils sont visibles) et plusieurs informations concernant
    comment ils sont affichés.

    """

    enregistrer = True
    def __init__(self, x, y):
        """Constructeur du repère."""
        BaseObj.__init__(self)
        self.x = x
        self.y = y
        self.nom = "un repère indéfini"
        self.description = Description(parent=self)
        self.amplificateur_portee = 1.5

    def __getnewargs__(self):
        return (0, 0)

    def __repr__(self):
        return "<Repère {}>".format(repr(self.nom))

    def __str__(self):
        return self.nom

    @property
    def desc_survol(self):
        return self.nom

    def get_nom_pour(self, personnage):
        return self.nom

    def regarder(self, personnage):
        """Le personnage regarde le repère."""
        salle = personnage.salle
        portee = get_portee(salle)
        visible = Visible.observer(personnage, portee, 5)
        points = [couple[1][1] for couple in visible.points.items()]
        if self not in points:
            personnage << "|err|Vous ne pouvez voir cela d'ici.|ff|"
            return

        salle.envoyer("{{}} regarde {}.".format(self.nom.lower()),
                personnage)
        msg = "Vous regardez " + self.nom + " :\n\n"
        msg += self.description.regarder(personnage, self)
        personnage << msg

    @staticmethod
    def trouver_reperes(visible, personnage, portee, precision,
            exceptions=None):
        """Cherche les repères visibles dans l'étendue."""
        navire = personnage.salle.navire
        etendue = navire.etendue
        altitude = etendue.altitude
        nav_direction = navire.direction.direction
        pos_coords = personnage.salle.coords.tuple()
        x, y, z = pos_coords
        position = Vector(x, y, altitude)

        for t_coords, repere in importeur.navigation.reperes.items():
            t_x, t_y = t_coords
            # On cherche l'angle entre la position du navire et du point
            v_point = Vector(t_x, t_y, altitude)
            v_dist = v_point - position
            if v_dist.mag > portee * repere.amplificateur_portee:
                continue

            direction = get_direction(v_dist)
            r_direction = (direction - navire.direction.direction) % 360
            # On détermine l'angle minimum fonction de la précision
            angle = norme_angle(round(r_direction / precision) * precision)
            visible.entrer_point(angle, v_dist, repere, nav_direction,
                    precision, exceptions=exceptions)

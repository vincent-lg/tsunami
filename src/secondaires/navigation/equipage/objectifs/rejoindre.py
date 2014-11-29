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


"""Objectif rejoindre."""

from math import fabs, radians

from vector import Vector

from primaires.vehicule.vecteur import Vecteur
from secondaires.navigation.constantes import *
from secondaires.navigation.equipage.objectif import Objectif

class Rejoindre(Objectif):

    """Objectif rejoindre.

    Cet objectif demande à un équipage de rejoindre un point précisé
    en coordonnées. Le point indiqué doit être statique (il existe un
    objectif particulier pour les points mobiles, comme les navires, qui
    intègrent leur propre calcul).

    Cet objectif est responsable de trouver un chemin entre le point
    actuel et le point visé. Cela inclut le choix de chemins
    détournés si le chemin direct ne peut être pris avec des calculs qui
    peuvent être assez complexes pour déterminer la vitesse et direction
    des chemins intermédiaires.

    """

    def __init__(self, equipage, x=None, y=None, vitesse=1):
        Objectif.__init__(self, equipage, x, y, vitesse)
        self.x = x
        self.y = y
        self.vitesse = vitesse
        self.n_x = None
        self.n_y = None
        self.n_vitesse = None

    def afficher(self):
        """Méthode à redéfinir retournant l'affichage de l'objectif."""
        navire = self.navire
        position = navire.opt_position
        o_x = position.x
        o_y = position.y
        d_x = self.x
        d_y = self.y
        distance = Vecteur(d_x - o_x, d_y - o_y, 0)
        direction = (distance.direction + 90) % 360
        msg_dist = get_nom_distance(distance)
        return "Cap sur {}° ({}), à {}".format(round(direction),
                distance.nom_direction, msg_dist)

    def get_distance(self):
        """Retourne la distance (Vecteur) entre le navire et la destination.

        Cette méthode crée un vecteur (class Vecteur définie dans
        le module primaire vehicule) qui représente la distance entre
        la position du navire et la destination.

        """
        navire = self.navire
        position = navire.opt_position
        o_x = position.x
        o_y = position.y

        if self.n_x is None and self.n_y is None:
            d_x = self.x
            d_y = self.y
        else:
            d_x = self.n_x
            d_y = self.n_y

        distance = Vecteur(d_x - o_x, d_y - o_y, 0)
        return distance

    def transmettre_controles(self):
        """Donne les contrôles indiqués (vitesse et direction)."""
        equipage = self.equipage
        navire = self.navire
        distance = self.get_distance()
        direction = round(distance.direction)

        # Crée ou modifie les contrôles
        if equipage.controles.get("direction"):
            equipage.controles["direction"].direction = direction
        else:
            equipage.controler("direction", direction)

        vitesse = self.vitesse if self.n_vitesse is None else self.n_vitesse
        if equipage.controles.get("vitesse"):
            if fabs(equipage.controles["vitesse"].vitesse - vitesse) >= 0.2:
                equipage.controles["vitesse"].vitesse_optimale = 0
            equipage.controles["vitesse"].vitesse = self.vitesse
        else:
            equipage.controler("vitesse", self.vitesse)

    def creer(self):
        """L'objectif est créé.

        On crée les contrôles associés pour atteindre l'objectif
        visé, à savoir, rejoindre le point (x, y), sans s'inquiéter
        des obstacles éventuels.

        """
        equipage = self.equipage
        commandant = self.commandant
        if commandant is None:
            return

        self.transmettre_controles()

    def verifier(self, prioritaire):
        """Vérifie que l'objectif est toujours valide.

        Dans cette méthode, on vérifie :
            Qu'il n'y a aucun obstacle sur la trajectoire assignée

        """
        equipage = self.equipage
        navire = self.navire
        commandant = self.commandant
        if commandant is None:
            return

        # On examine les points listés par la vigie
        # Si il n'y a pas de vigie, pas le moyen de les éviter
        tries = equipage.vigie_tries

        # Si le dictionnaire est vide, ne fait rien
        if not tries:
            return

        # On n'examine que les obstacles
        obstacles = tries.get("obstacle", {}).copy()
        obstacles.update(tries.get("salle", {}))
        obstacles.update(tries.get("sallenavire", {}))

        # On s'intéresse seulement aux obstacles qui ont un angle
        # dangereux, entre -45° et 45°
        dangereux = obstacles.copy()
        for angle in obstacles.keys():
            if angle < -45 or angle > 45:
                del dangereux[angle]

        # Si il n'y a aucun obstacle, ne continue pas
        if not dangereux:
            if self.n_x is not None or self.n_y is not None or \
                    self.n_vitesse is not None:
                self.warning("Il n'y a plus de danger sur la trajectoire")

            self.n_x = None
            self.n_y = None
            self.n_vitesse = None
            return

        # Peut-être qu'on peut atteindre l'objectif malgré tout
        position = navire.opt_position
        projetee = Vector(self.x, self.y, 0) - position
        if projetee.mag > 15:
            projetee.mag = 15
        projetee = position + projetee

        if not navire.controller_collision(projetee, collision=False):
            self.n_x = None
            self.n_y = None
            return

        # Maintenant on cherche la distance la plus courte
        min_angle = None
        min_distance = None
        for angle, (vecteur, point) in dangereux.items():
            if min_distance is None or vecteur.mag < min_distance:
                min_distance = vecteur.mag
                min_angle = angle

        # En fonction de la distance, modifie la vitesse
        if min_distance < 5:
            self.vitesse = 0
        elif min_distance < 15:
            self.vitesse = 0,2
        elif min_distance < 30:
            self.vitesse = 1
        else:
            # Les obstacles sont trop loin pour être inquiétants
            return

        # Cherche ensuite le meilleur cap
        # On cherche le meilleur cap possible (c'est-à-dire le plus long)
        distance = 30
        angles = [i * 5 for i in range(1, 18)]
        for i in range(1, 18):
            angles.insert((i - 1) * 2, i * -5)

        while distance > 0:
            for angle in angles:
                vecteur = navire.opt_direction
                vecteur.mag = distance
                vecteur.around_z(radians(angle))
                projetee = position + vecteur
                if not navire.controller_collision(projetee, collision=False):
                    self.warning("Obstacle en vue, nouveau cap vers " \
                            "{}° (x={}, y={}, distance={})".format(
                            angle, round(projetee.x), round(projetee.y),
                            distance))
                    self.n_x = projetee.x
                    self.n_y = projetee.y
                    return

            distance -= 5

        # Si on ne trouve aucun chemin, il serai bon de retourner

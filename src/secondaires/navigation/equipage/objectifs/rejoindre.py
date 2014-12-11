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
        self.ancienne_vitesse = vitesse
        self.vitesse_optimale = vitesse
        self.autre_direction = None

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
        d_x = self.x
        d_y = self.y
        distance = Vecteur(d_x - o_x, d_y - o_y, 0)
        return distance

    def transmettre_controles(self):
        """Donne les contrôles indiqués (vitesse et direction)."""
        equipage = self.equipage
        navire = self.navire
        distance = self.get_distance()
        if self.autre_direction:
            direction = round(self.autre_direction)
        else:
            direction = round(distance.direction)

        # Crée ou modifie les contrôles
        if equipage.controles.get("direction"):
            equipage.controles["direction"].direction = direction
        else:
            equipage.controler("direction", direction)

        vitesse = self.vitesse
        if equipage.controles.get("vitesse"):
            equipage.controles["vitesse"].vitesse = vitesse
            if self.ancienne_vitesse is not None and vitesse != \
                    self.ancienne_vitesse:
                equipage.controles["vitesse"].calculer_vitesse()
            self.ancienne_vitesse = vitesse
        else:
            equipage.controler("vitesse", self.vitesse)

    def trouver_cap(self):
        """Trouve le cap, tenant compte des obstacles."""
        equipage = self.equipage
        navire = self.navire

        # Si le navire est en train de virer, pour l'instant annule l'objectif
        if navire.orientation != 0:
            return

        # On examine les points listés par la vigie
        # Si il n'y a pas de vigie, pas le moyen de les éviter
        tries = equipage.vigie_tries

        # Si le dictionnaire est vide, ne fait rien
        if not tries:
            self.ancienne_vitesse = None
            self.autre_direction = None
            self.transmettre_controles()
            return

        # On n'examine que les obstacles
        obstacles = tries.get("obstacle", {}).copy()
        obstacles.update(tries.get("salle", {}))
        obstacles.update(tries.get("sallenavire", {}))

        # On s'intéresse seulement aux obstacles qui ont un angle
        # dangereux, entre -90° et 90°
        dangereux = obstacles.copy()
        for angle in obstacles.keys():
            if angle < -90 or angle > 90:
                del dangereux[angle]

        # Si il n'y a aucun obstacle, ne continue pas
        if not dangereux:
            self.ancienne_vitesse = None
            self.autre_direction = None
            self.transmettre_controles()
            return

        # Maintenant on cherche la distance la plus courte
        min_angle = None
        min_distance = None
        for angle, (vecteur, point) in dangereux.items():
            if min_distance is None or vecteur.mag < min_distance:
                min_distance = vecteur.mag
                min_angle = angle

        # En fonction de la distance, modifie la vitesse
        if min_distance < 8:
            self.vitesse = 0.2
        elif min_distance < 25:
            self.vitesse = 0.6

        # Cherche ensuite le meilleur cap
        # On cherche le meilleur cap possible (c'est-à-dire le plus long)
        distance = 30
        angles = [i * 5 for i in range(0, 18)]
        for i in range(1, 18):
            angles.append(i * -5)

        # Si on est pas exactement dans la bonne direction pour rejoindre
        # le point (x, y), on envisage de changer de cap
        o_distance = self.get_distance()
        relative = o_distance.direction - navire.direction.direction
        angles = sorted(angles, key=lambda a: fabs(a - relative))

        position = navire.opt_position
        while distance > 0:
            for angle in angles:
                vecteur = navire.opt_direction
                vecteur.mag = distance
                vecteur.around_z(radians(angle))
                if not navire.controller_collision(vecteur, collision=False,
                        marge=0.8):
                    if angle != 0:
                        self.info("Cap libre sur {}°".format(angle))

                    self.autre_direction = round((
                            navire.direction.direction + angle) % 360)
                    self.transmettre_controles()
                    return

            distance -= 5


        # On ne change pas de cap mais peut-être change-t-on de vitesse
        self.transmettre_controles()

    def creer(self):
        """L'objectif est créé.

        On crée les contrôles associéss pour atteindre l'objectif
        visé, à savoir, rejoindre le point (x, y), en essayant
        de trouver les obstacles corresondant et un cap de remplacement
        si nécessaire.

        """
        equipage = self.equipage
        commandant = self.commandant
        if commandant is None:
            return

        self.trouver_cap()

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

        if prioritaire:
            self.trouver_cap()

# -*-coding:Utf-8 -*
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


"""Ce fichier contient la classe Visible, détaillée plus bas."""

from math import sqrt, radians, pi

from vector import Vector, mag

from primaires.salle.salle import Salle
from primaires.vehicule.vecteur import *
from secondaires.navigation.constantes import CB_BRASSES

## Fonctions
def norme_angle(angle):
    """Normalise l'angle.

    Il doit être précis entre 0 et 360.
    Il faut le ramener entre -180 et 180.

    """
    if angle > 180:
        angle = -360 + angle

    return angle

def norme_inv_angle(angle):
    """Norme inverse de l'angle.

    On attend un angle entre -180 et 180.
    On retourne un angle entre 0 et 360.

    """
    if angle < 0:
        angle += 360

    return angle

## Classe Visible

class Visible:

    """Cette classe contient les éléments visibles depuis une positions.

    Ces éléments sont décrits par ligne en fonction de leur position par
    rapport au personnage, à la portée et à la précision. Les éléments peuvent
    être de différents types : par défaut, les obstacles et les navires sont
    considérés comme des points, mais ce dictionnaire peut être agrandi
    par d'autres modules. Le dictionnaire des points observables se trouve
    dans 'importeur.navigation.points_observables'.

    On n'utilise pas le constructeur pour générer cette classe, mais
    la méthode de classe observer.
    D'autres méthodes sont là pour afficher ou formatter les points trouvés.

    """

    def __init__(self, position):
        """Constructeur, à ne pas appeler directement."""
        self.position = position
        self.points = {}

    def entrer_point(self, angle, v_dist, point, nav_direction,
            precision, recursif=True, exceptions=None):
        """Entre un point dans le dictionnaire des points.

        On n'entre le point que si il n'y a pas de point plus proche.

        """
        exceptions = exceptions or {}

        # On élimite les points dans l'exception
        for cle, valeur in exceptions.items():
            if cle == "":
                if point is valeur:
                    return
            else:
                if getattr(point, cle, None) is valeur:
                    return

        position = self.position
        a_point = self.points.get(angle)
        if a_point is None or a_point[0].mag > v_dist.mag:
            self.points[angle] = (v_dist, point)

            if not recursif:
                # On s'arrête là
                return

            # Si on est assez prêt, un point peut être visible
            # dans plusieurs directions, sur 0°, mais sur 15 aussi
            # par exemple. La boucle ci-dessous vérifie qu'on voit
            # bien tous les points
            test = True
            t_vec = Vector(v_dist.x, v_dist.y, v_dist.z)
            c_angle = 0 # va changer au fur et à mesure que l'on tourne
            while test:
                t_vec.around_z(radians(precision))
                a_vec = position + t_vec
                c_angle += precision
                if (t_vec - v_dist).mag <= 0.6:
                    direction = get_direction(t_vec)
                    r_direction = (direction - nav_direction) % 360
                    t_angle = norme_angle(round(r_direction / \
                            precision) * precision)
                    self.entrer_point(t_angle, t_vec, point, nav_direction,
                            precision, recursif=False, exceptions=exceptions)
                else:
                    test = False
                if c_angle >= 180:
                    break

            test = True
            t_vec = Vector(v_dist.x, v_dist.y, v_dist.z)
            c_angle = 0
            while test:
                t_vec.around_z(radians(-precision))
                a_vec = position + t_vec
                c_angle += precision
                if (t_vec - v_dist).mag <= 0.6:
                    direction = get_direction(t_vec)
                    r_direction = (direction - nav_direction) % 360
                    t_angle = norme_angle(round(r_direction / \
                            precision) * precision)
                    self.entrer_point(t_angle, t_vec, point, nav_direction,
                            precision, recursif=False, exceptions=exceptions)
                else:
                    test = False
                if c_angle >= 180:
                    break

    def get_tries(self):
        """Retourne les points triés en classes.

        Au lieu d'avoir un seul dictionnaire {angle: (vecteur, point)},
        on a un dictionnaire contenant en clé le nom de l classe de
        l'obstacle et en valeur un dictionnaire contenant les obstacles.
        Par exemple, voilà ce qu'on pourrait obtenir :
            {
                "navire": {
                    5: (vecteur, autre_navire),
                },
                "obstacle": {
                    10, falaise,
                    15: ville,
                },
            }

        """
        tries = {}

        for angle, (vecteur, point) in self.points.items():
            nom = type(point).__name__.lower()
            dictionnaire = tries.get(nom, {})
            dictionnaire[angle] = (vecteur, point)
            tries[nom] = dictionnaire

        return tries

    @classmethod
    def observer(cls, personnage, portee, precision, exceptions=None):
        """Méthode de classe construisant une instance de classe.

        Les paramètres à préciser sont :
            Le personnage
            La portée à laquelle ce personnage doit voir
            La précision en degré à laquelle les détails seront arrondis.
            Les exceptions sous la forme d'un dicitonnaire.

        Les exceptions doivent être précisées sous la forme :
            {"attribut": valeur}

        Pour chaque point, on essaye de récupérer l'attribut (grâce à
        getattr). Si la valeur correspond, alors le point n'est pas ajouté.
        Consultez le code de la commande détail/detail pour un exemple
        concret.

        """
        position = Vector(*personnage.salle.coords.tuple())
        visible = cls(position)
        for methode in importeur.navigation.points_ovservables.values():
            methode(visible, personnage, portee, precision, exceptions)
        return visible

    @staticmethod
    def trouver_cotes(visible, personnage, portee, precision, exceptions=None):
        """Cherche les côtes de l'étendue."""
        navire = personnage.salle.navire
        etendue = navire.etendue
        altitude = etendue.altitude
        nav_direction = navire.direction.direction
        pos_coords = personnage.salle.coords.tuple()
        x, y, z = pos_coords
        position = Vector(x, y, altitude)

        # D'abord on cherche les côtes et obstacles
        proches = etendue.get_points_proches(x, y, portee)
        for t_coords, point in proches.items():
            t_x, t_y = t_coords
            # On cherche l'angle entre la position du navire et du point
            v_point = Vector(t_x, t_y, altitude)
            v_dist = v_point - position
            direction = get_direction(v_dist)
            r_direction = (direction - navire.direction.direction) % 360
            # On détermine l'angle minimum fonction de la précision
            angle = norme_angle(round(r_direction / precision) * precision)
            visible.entrer_point(angle, v_dist, point, nav_direction,
                    precision, exceptions=exceptions)

    @staticmethod
    def trouver_navires(visible, personnage, portee, precision, exceptions=None):
        """Cherche les navires autour du personnage."""
        exceptions = exceptions or {}
        navire = personnage.salle.navire
        etendue = navire.etendue
        altitude = etendue.altitude
        nav_direction = navire.direction.direction
        pos_coords = personnage.salle.coords.tuple()
        x, y, z = pos_coords
        position = Vector(x, y, altitude)
        navires = [n for n in importeur.navigation.navires.values() if \
                n.etendue and mag(n.position.x, n.position.y, altitude,
                position.x, position.y, altitude) - \
                n.get_max_distance_au_centre() <= portee]
        for t_navire in navires:
            # On détermine la salle la plus proche
            t_salles = [s for s in t_navire.salles.values() if \
                    s.coords.z == 0 and s.coords.valide]
            for t_salle in t_salles:
                # Calcul de la distance entre salle et t_salle
                t_coords = t_salle.coords.tuple()
                t_x, t_y, t_z = t_coords
                distance = mag(x, y, 0, t_x, t_y, 0)
                v_point = Vector(t_x, t_y, altitude)
                v_dist = v_point - position
                direction = get_direction(v_dist)
                r_direction = (direction - nav_direction) % 360

                # On détermine l'angle minimum fonction de la précision
                angle = norme_angle(round(r_direction / precision) * precision)

                if distance <= portee:
                    visible.entrer_point(angle, v_dist, t_navire,
                            nav_direction, precision, exceptions=exceptions)

    def filtrer(self, element):
        """Retire l'information du tableau des points.

        L'information est le point. Ce peut être un navire, une salle, un
        obstacle ou une information particulière ajoutée par un module.

        """
        for angle, point in tuple(self.points.items()):
            point = point[1]
            if point is element:
                del self.points[angle]

    def formatter(self, direction, limite):
        """On formatte les points.

        On attend :
            direction -- la direction en degré du regard
            limite -- la limite du regard.

        Plus la limite est grande, plus on voit autour. En absolu,
        si la limite est 180, on voit sur 180 gauche et 180 droite,
        c'est-à-dire tout autour.

        Cette méthode doit retourner une chaîne des points formattés.

        """
        # On commence par trier les points
        points = tuple(self.points.items())
        points = sorted(points, key=lambda couple: couple[0])
        if direction == 180:
            neg = list(reversed([(a, p) for a, p in points if a < 0]))
            arr = [(a, p) for a, p in points if a == 180]
            pos = list(reversed([(a, p) for a, p in points if 0 <= a < 180]))
            points = neg + arr + pos

        # On formatte les points obtenus
        msg = []
        limite_inf = norme_angle(direction - limite)
        limite_sup = norme_angle(direction + limite)
        if limite_inf < 0 and limite_sup > 0:
            r_limite_1 = range(limite_inf, 0)
            r_limite_2 = range(0, limite_sup + 1)
        elif limite_sup < 0 and limite_inf > 0:
            r_limite_1 = range(-180, limite_sup + 1)
            r_limite_2 = range(limite_inf, 181)
        elif limite_inf > limite_sup:
            r_limite_1 = r_limite_2 = range(limite_sup, limite_inf + 1)
        else:
            r_limite_1 = r_limite_2 = range(limite_inf, limite_sup + 1)

        for angle, point in points:
            vecteur, point = point
            if not (angle in r_limite_1 or angle in r_limite_2):
                continue

            if angle == 0:
                direction = "droit devant"
            elif angle == 180:
                direction = "droit à l'arrière"
            elif angle > 0:
                direction = "sur {:>3}° tribord".format(angle)
            else:
                direction = "sur {:>3}° bâbord".format(-angle)

            distance = round(vecteur.mag * CB_BRASSES)
            msg_dist = "à {nb:>3} brasse{s}"
            if distance < 1:
                msg_dist = "tout près"
            elif 1 <= distance <= 10:
                pass
            elif 10 < distance <= 20:
                distance = round(distance / 2) * 2
            elif 20 < distance <= 50:
                distance = round(distance / 5) * 5
            elif 50 < distance <= 100:
                distance = round(distance / 10) * 10
            elif 100 < distance <= 1000:
                distance = round(distance / 100) * 100
            elif 1000 < distance <= 2000:
                distance = round(distance / 500) * 500
            else:
                distance = round(distance / 1000) * 1000

            s = "s" if distance > 1 else ""
            msg_dist = msg_dist.format(nb=distance, s=s)
            terre = point.desc_survol.capitalize()
            symbole = importeur.navigation.get_symbole(point)

            msg.append(
                    "{:<2} {:<20} {:<15} {}".format(
                    symbole, direction, msg_dist, terre))

        return "\n".join(msg)

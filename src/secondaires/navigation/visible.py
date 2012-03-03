# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Ce fichier contient la classe Visible, détaillée plus bas.

Il contient également d'autres fonctions utiles à la classe.

"""

from math import sqrt

from primaires.salle.salle import Salle
from primaires.vehicule.vecteur import Vecteur
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

def entrer_point(dictionnaire, position, angle, v_dist, coords, point):
    """Entre un point dans le dictionnaire.
    
    Si le point est déjà présent on cherche à garder le bon (le plus proche
    souvent).
    
    """
    a_point = dictionnaire.get(angle)
    if a_point:
        # Détermine si le point est plus proche ou non
        x, y, p_vecteur, a_point = a_point
        if (position - p_vecteur).norme == v_dist.norme and isinstance(point,
                Salle):
            dictionnaire[angle] = (coords[0], coords[1], v_dist, point)
        elif (position - p_vecteur).norme > v_dist.norme:
            dictionnaire[angle] = (coords[0], coords[1], v_dist, point)
    else:
        dictionnaire[angle] = (coords[0], coords[1], v_dist, point)

## Classe Visible

class Visible:
    
    """Cette classe contient les éléments visibles depuis une positions.
    
    Ces éléments sont regroupés dans plusieurs dictionnaire dont la clé
    est l'angle par rapport à l'observateur et en valeur l'élément observé.
    
    On n'utilise pas le constructeur pour générer cette classe, mais
    la méthode de classe observer.
    D'autres méthodes sont là pour afficher ou formatter les points trouvés.
    
    """
    
    def __init__(self):
        """Constructeur, à ne pas appeler directement."""
        self.cotes = {}
        self.navires = []
    
    @classmethod
    def observer(cls, personnage, portee, precision):
        """Méthode de classe construisant une instance de classe.
        
        Les paramètres à préciser sont :
            Le personnage
            La portée à laquelle ce personnage doit voir
            La précision en degré à laquelle les détails seront arrondis.
        
        """
        visible = cls()
        navire = personnage.salle.navire
        etendue = navire.etendue
        altitude = etendue.altitude
        pos_coords = personnage.salle.coords.tuple()
        x, y, z = pos_coords
        position = Vecteur(x, y, altitude)
        
        # D'abord on cherche les côtes et obstacles
        for t_coords, point in etendue.points.items():
            t_x, t_y = t_coords
            t_distance = sqrt((x - t_x) ** 2 + (y - t_y) ** 2)
            if t_distance <= portee:
                # On cherche l'angle entre la position du navire et du point
                v_point = Vecteur(t_x, t_y, altitude)
                v_dist = v_point - position
                direction = v_dist.direction
                r_direction = (direction - navire.direction.direction) % 360
                # On détermine l'angle minimum fonction de la précision
                angle = norme_angle(round(r_direction / precision) * precision)
                entrer_point(visible.cotes, position, angle, v_dist, t_coords,
                        point)
                
                # Si on est assez prêt, un point peut être visible
                # dans plusieurs directions, sur 0°, mais sur 15 aussi
                # par exemple. La boucle ci-dessous vérifie qu'on voit
                # bien tous les points
                test = True
                t_vec = v_dist.copier()
                c_angle = 0 # va changer au fur et à mesure que l'on tourne
                while test:
                    a_vec = position + t_vec.tourner_autour_z(precision)
                    c_angle += precision
                    if round(a_vec.x) == t_x and round(a_vec.y) == t_y:
                        direction = t_vec.direction
                        r_direction = (direction - \
                                navire.direction.direction) % 360
                        t_angle = norme_angle(round(r_direction / \
                                precision) * precision)
                        entrer_point(visible.cotes, position, t_angle, t_vec,
                                t_coords, point)
                    else:
                        test = False
                    if c_angle >= 360:
                        break
                
                test = True
                t_vec = v_dist.copier()
                c_angle = 0
                while test:
                    a_vec = position + t_vec.tourner_autour_z(-precision)
                    c_angle += precision
                    if round(a_vec.x) == t_x and round(a_vec.y) == t_y:
                        direction = t_vec.direction
                        r_direction = (direction - \
                                navire.direction.direction) % 360
                        t_angle = norme_angle(round(r_direction / \
                                precision) * precision)
                        entrer_point(visible.cotes, position, t_angle, t_vec,
                                t_coords, point)
                    else:
                        test = False
                    if c_angle >= 360:
                        break
        
        # Ensuite on affiche les navires
        navires = [n for n in importeur.navigation.navires.values() if \
                n.etendue is etendue and n is not navire]
        for t_navire in navires:
            # On détermine la salle la plus proche
            t_salles = [s for s in t_navire.salles.values() if \
                    s.coords.z == altitude]
            
            distance = None
            d_salle = None
            t_x = t_y = None
            v_dist = None
            for t_salle in t_salles:
                # Calcul de la distance entre salle et t_salle
                t_coords = t_salle.coords.tuple()
                t_x, t_y, t_z = t_coords
                t_distance = sqrt((x - t_x) ** 2 + (y - t_y) ** 2)
                if distance is None or t_distance < distance:
                    distance = t_distance
                    d_salle = t_salle
                    t_x, t_y, t_z = t_salle.coords.tuple()
                else:
                    continue
            
            if t_x is None:
                continue
            
            v_point = Vecteur(t_x, t_y, altitude)
            v_dist = v_point - position
            direction = v_dist.direction
            r_direction = (direction - navire.direction.direction) % 360
            
            # On détermine l'angle minimum fonction de la précision
            angle = norme_angle(round(r_direction / precision) * precision)
            
            if distance <= portee:
                # N'y a-t-il pas de terre plus proche
                v_cote = visible.cotes.get(angle, (None, None, None, None))[2]
                if v_cote is None or v_cote.norme >= v_point.norme:
                    visible.navires.append((angle, (t_x, t_y, v_point,
                            t_navire)))
        
        return visible
    
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
        points = tuple(self.cotes.items()) + tuple(self.navires)
        neg = [(a,  p) for a, p in points if a < 0]
        pos = [(a, p) for a, p in points if a >= 0]
        if pos and min(a for a, p in pos) > 90 and neg:
            points_1 = sorted([(a, p) for a, p in neg], reverse=True)
            points_2 = sorted([(a, p) for a, p in pos], reverse=True)
            points = tuple(points_1) + tuple(points_2)
        else:
            points = sorted(points)
        
        # On formatte les points obtenus
        msg = []
        limite_inf = direction - limite
        limite_sup = direction + limite
        for angle, point in points:
            x, y, vecteur, point = point
            if angle < limite_inf or angle > limite_sup:
                continue
            
            if angle == 0:
                direction = "droit devant"
            elif angle == 180:
                direction = "droit à l'arrière"
            elif angle > 0:
                direction = "sur {:>3}° tribord".format(angle)
            else:
                direction = "sur {:>3}° bâbord".format(-angle)
            
            distance = round(vecteur.norme * CB_BRASSES)
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

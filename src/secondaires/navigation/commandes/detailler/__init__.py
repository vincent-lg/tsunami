# -*-coding:Utf-8 -*

# Copyright (c) 2010 LE GOFF Vincent
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


"""Package contenant la commande 'détailler'."""

from primaires.interpreteur.commande.commande import Commande
from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.uniligne import Uniligne
from primaires.vehicule.vecteur import Vecteur
from secondaires.navigation.constantes import CB_BRASSES

def entrer_point(observe, navire, position, angle, v_dist, coords, point):
    """Entre un point dans le dictionnaire."""
    a_point = observe.get(angle)
    if a_point:
        # Détermine si le point est plus proche ou non
        x, y, v, p = a_point
        if (position - v).norme > v_dist.norme:
            observe[angle] = (coords[0], coords[1], v_dist, point)
    else:
        observe[angle] = (coords[0], coords[1], v_dist, point)

def get_points(personnage, navire, distance, precision):
    """Retourne les points les plus près du navire.
    
    En clé se trouve l'angle, en valeur le point le plus proche observé.
    
    """
    etendue = navire.etendue
    alt = etendue.altitude
    pos_coords = personnage.salle.coords.tuple()
    position = Vecteur(pos_coords[0], pos_coords[1], alt)
    observe = {}
    
    # On explore tous les points non débarcables
    for coords, point in etendue.points.items():
        vec = Vecteur(coords[0], coords[1], alt)
        x, y = coords
        v_dist = vec - position
        if v_dist.norme <= distance:
            # On cherche l'angle entre la position du navire et du point
            direction = v_dist.direction
            r_direction = direction - navire.direction.direction
            # On détermine l'angle minimum fonction de la précision
            angle = round(r_direction / precision) * precision
            entrer_point(observe, navire, position, angle, v_dist, coords, point)
            test = True
            t_vec = v_dist.copier()
            c_angle = 0
            while test:
                t_vec.tourner_autour_z(precision)
                c_angle += precision
                if int(t_vec.x) == x and int(t_vec.y) == y:
                    direction = t_vec.direction
                    r_direction = direction - navire.direction.direction
                    t_angle = round(r_direction / precision) * precision
                    entrer_point(observe, navire, position, t_angle, t_vec,
                            coords, point)
                else:
                    test = False
                if c_angle >= 360:
                    break
            
            test = True
            t_vec = v_dist.copier()
            c_angle = 0
            while test:
                t_vec.tourner_autour_z(-precision)
                c_angle += precision
                if int(t_vec.x) == x and int(t_vec.y) == y:
                    direction = t_vec.direction
                    r_direction = direction - navire.direction.direction
                    t_angle = round(r_direction / precision) * precision
                    entrer_point(observe, navire, position, t_angle, t_vec,
                            coords, point)
                else:
                    test = False
                if c_angle >= 360:
                    break
    
    return observe

def formatter_points(points, dir, limite=90):
    """Formatte les points et retourne une chaîne envoyable au joueur."""
    msg = []
    for angle, point in sorted(points.items()):
        x, y, vecteur, point = point
        if angle < dir - limite or angle > dir + limite:
            continue
        
        if angle == 0:
            direction = "droit devant"
        elif angle == 180:
            direction = "droit à l'arrière"
        elif angle > 0:
            direction = "sur {}° tribord".format(angle)
        else:
            direction = "sur {}° bâbord".format(-angle)
        
        distance = round(vecteur.norme * CB_BRASSES)
        unite = "brasse"
        msg_dist = "à environ {nb} {unite}{s}"
        if 0 <= distance < 1:
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
            distance = round(distance / 100)
            unite = "encablure"
        elif 1000 < distance <= 2000:
            distance = round(distance / 500) * 5
            unite = "encablure"
        else:
            distance = round(distance / 1000)
            unite = "mille"
        
        s = "s" if distance > 1 else ""
        msg_dist = msg_dist.format(nb=distance, unite=unite, s=s)
        
        terre = "Une terre"
        if point:
            terre = point.terrain.desc_survol.capitalize()
        
        msg.append(terre + " " + msg_dist + " " + direction)
    
    return msg
        
class CmdDetailler(Commande):
    
    """Commande 'détailler'"""
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "détailler", "detail")
        self.schema = "(<nombre>)"
        self.aide_courte = "affiche les détails de l'étendue d'eau"
        self.aide_longue = \
            "Cette commande permet à un navigateur de connaître les " \
            "détails qui l'entourent. Sans paramètre, cette commande " \
            "affiche les côtes, ports, navires visibles sur l'étendue. " \
            "Vous pouvez préciser en paramètre un point à détailler " \
            "plus particulièrement sous la forme d'un angle. Pour regarder " \
            "plus précisément, entrer 90. Si vous voulez regarder à " \
            "bâbord, entrez -90. Vous pouvez entrer 180 pour regarder " \
            "droit à l'arrière du navire."
    
    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        nombre = self.noeud.get_masque("nombre")
        nombre.proprietes["limite_inf"] = "-180"
        nombre.proprietes["limite_sup"] = "180"
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        salle = personnage.salle
        if not hasattr(salle, "navire") or salle.navire is None:
            personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
            return
        
        navire = salle.navire
        etendue = navire.etendue
        alt = etendue.altitude
        hauteur = salle.coords.z - alt
        if salle.interieur:
            personnage << "|err|Vous ne pouvez rien voir d'ici.|ff|"
            return
        
        portee = 50
        if hauteur > 0:
            portee = 50 * hauteur
        
        nombre = dic_masques["nombre"]
        print(nombre, bool(nombre))
        if nombre:
            direction = nombre.nombre
            direction = round(direction / 5) * 5
            limite = 45
            precision = 5
        else:
            direction = 0
            limite = 90
            precision = 15
        
        # On récupère les points
        points = get_points(personnage, navire, portee, precision)
        msg = formatter_points(points, direction, limite)
        if msg:
            personnage << "\n".join(msg)
        else:
            personnage << "Rien n'est en vue auprès de vous."

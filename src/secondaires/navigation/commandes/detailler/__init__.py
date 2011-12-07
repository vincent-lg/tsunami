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

def get_points(navire, distance, precision):
    """Retourne les points les plus près du navire.
    
    En clé se trouve l'angle, en valeur le point le plus proche observé.
    
    """
    etendue = navire.etendue
    alt = etendue.altitude
    position = navire.position
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
            while test:
                t_vec.tourner_autour_z(precision)
                if int(t_vec.x) == x and int(t_vec.y) == y:
                    direction = t_vec.direction
                    r_direction = direction - navire.direction.direction
                    angle = round(r_direction / precision) * precision
                    entrer_point(observe, navire, position, angle, t_vec, coords, point)
                else:
                    test = False
            
            test = True
            t_vec = v_dist.copier()
            while test:
                t_vec.tourner_autour_z(-precision)
                if int(t_vec.x) == x and int(t_vec.y) == y:
                    direction = t_vec.direction
                    r_direction = direction - navire.direction.direction
                    angle = round(r_direction / precision) * precision
                    entrer_point(observe, navire, position, angle, t_vec, coords, point)
                else:
                    test = False
                
    
    return observe

def formatter_points(points, limite=90):
    """Formatte les points et retourne une chaîne envoyable au joueur."""
    msg = []
    for angle, point in sorted(points.items()):
        x, y, vecteur, point = point
        if angle > 180 + limite or limite < angle < 180:
            continue
        
        if angle == 0:
            direction = "droit devant"
        elif angle == 180:
            direction = "droit à l'arrière"
        elif angle > 0:
            direction = "sur {}° tribord".format(angle)
        else:
            direction = "sur {}° bâbord".format(-angle)
        
        distance = round(vecteur.norme * 3.2)
        unite = "brasse"
        msg_dist = "à environ {nb} {unite}{s}"
        if 0 <= distance < 1:
            msg_dist = "tout près"
        elif 1 <= distance < 10:
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
        
        msg.append("une terre " + msg_dist + " " + direction)
    
    return msg
        
class CmdDetailler(Commande):
    
    """Commande 'détailler'"""
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "détailler", "detail")
        self.schema = ""
        self.aide_courte = "affiche les détails de l'étendue d'eau"
        self.aide_longue = \
            "Cette commande permet à un navigateur de connaître les " \
            "détails qui l'entourent. Sans paramètre, cette commande " \
            "affiche les côtes, ports, navires visibles sur l'étendue. " \
            "Vous pouvez préciser en paramètre un point à détailler " \
            "plus particulièrement."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        salle = personnage.salle
        if not hasattr(salle, "navire") or salle.navire is None:
            personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
            return
        
        navire = salle.navire
        # On récupère les points
        points = get_points(navire, 30, 15)
        msg = formatter_points(points)
        personnage << "\n".join(msg)

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


"""Fichier contenant la classe Chemins, détaillée plus bas."""

from math import cos, sin, tan, radians, sqrt

from abstraits.obase import BaseObj
from primaires.vehicule.vecteur import Vecteur
from .chemin import Chemin

class Chemins(BaseObj):
    
    """Classe représentant une liste de chemins."""
    
    def __init__(self):
        """Constructeur des chemins."""
        self.chemins = []
    
    def __repr__(self):
        """Affichage des chemins."""
        chemins = [str(c) for c in self.chemins]
        return "<chemins [" + ", ".join(chemins) + "]>"
    
    def get(self, salle):
        """Retourne si trouvée le chemin dont la destination est salle.
        
        Si non trouvé retourne None.
        
        """
        for chemin in self.chemins:
            if chemin.destination is salle:
                return chemin
        
        return None
    
    @classmethod
    def salles_autour(cls, salle, rayon=15):
        """Retourne les chemins autour de salle dans un rayon donné."""
        o_chemins = cls()
        salles = {} # salle: chemin}
        
        # Fonction explorant une salle et retournant ses sorties récursivement
        def get_sorties_rec(salle, rayon=0, max=15, salles=None):
            salles = salles or {}
            chemin = salles.get(salle)
            if chemin:
                sorties = list(chemin.sorties)
            else:
                sorties = []
            for sortie in salle.sorties:
                t_salle = sortie.salle_dest
                n_chemin = Chemin()
                n_chemin.sorties.extend(sorties + [sortie])
                a_chemin = salles.get(t_salle)
                if a_chemin:
                    if a_chemin.longueur > n_chemin.longueur:
                        salles[t_salle] = n_chemin
                else:
                    salles[t_salle] = n_chemin
            
            if rayon < max:
                for sortie in salle.sorties:
                    t_salle = sortie.salle_dest
                    get_sorties_rec(t_salle, rayon + 1, max, salles)
            
            return salles
        
        sorties = get_sorties_rec(salle, max=rayon)
        for salle, chemin in sorties.items():
            # Constitution du chemin
            if chemin.origine is not chemin.destination:
                salles[salle] = chemin
        
        # Enfin, on retourne la liste obtenue
        o_chemins.chemins.extend(list(salles.values()))
        return o_chemins
    
    @classmethod
    def get_salles_entre(cls, origine, destination, D3=True):
        """Retourne une liste de salles entre origine et destination.
        
        Les paramètres origine et destination doivent être des salles.
        Sont retournées toutes les salles dont la distance par rapport
        à l'une et à l'autre est inférieure à la distance entre
        origine et destination.
        
        Par exemple, si origine est (0, 2, 0) et destination est (2, 2, 0),
        la distance entre origine et destination est de 2 (nrome du vecteur).
        Seront retournées toutes les salles ayant une distance maximum de 2
        par rapport à origine ou destination.
        
        Le paramètre d3 (3D) (à True par défaut) permet de tenir compte
        de l'information Z d'une coordonnée (l'altitude de la salle).
        Si ce paramètre est à False, on ne tient pas compte de l'altitude.
        
        Enfin, notez que la liste retournée par cette méthode n'est pas triée.
        
        """
        o_coords = origine.coords.tuple()
        d_coords = destination.coords.tuple()
        if not D3:
            o_coords = o_coords[:1] + (0, )
            d_coords = d_coords[:1] + (0, )
        
        vecteur = Vecteur(*d_coords) - Vecteur(*o_coords)
        distance_max = vecteur.norme
        o_x, o_y, o_z = o_coords
        d_x, d_y, d_z = d_coords
        salles = []
        for coords, salle in importeur.salle._coords.items():
            x, y, z = coords
            if not D3:
                z = 0
            
            d1 = sqrt((x - o_x) ** 2 + (y - o_y) ** 2 + (z - o_z) ** 2)
            d2 = sqrt((x - d_x) ** 2 + (y - d_y) ** 2 + (z - d_z) ** 2)
            if d1 < distance_max or d2 < distance_max:
                salles.append(salle)
        
        # On parcourt les salles qui restent
        v_o = v_c = Vecteur(o_x, o_y, o_z)
        v_d = Vecteur(d_z, d_y, d_z)
        v_distance = v_d - v_o
        trajectoires = []
        for salle in salles:
            v_a = Vecteur(*salle.coords.tuple())
            if not D3:
                v_a.z = 0
            
            v_ac = v_a - v_c
            ac = v_ac.norme
            gamma = (v_c - v_ac).direction % 90
            alpha = 90 - gamma
            beta = 90
            #if alpha == 0:
            #    trajectoires.append(salle)
            #    continue
            
            bc = sin(radians(alpha)) *  ac
            if bc == 0:
                continue
            
            v_bc = v_ac.copier().tourner_autour_z((
                    v_ac.direction - v_distance.direction) % 360) * \
                    (v_ac.norme / bc)
            
            v_b = v_c + v_bc
            v_ab = v_b - v_a
            print("v_b", v_b, salle.ident, salle.coords)
            if v_b.norme <= 0.5:
                trajectoires.append(salle)
        
        return trajectoires


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


"""Fichier contenant la fonction autour."""

from math import sqrt

from primaires.scripting.fonction import Fonction

class ClasseFonction(Fonction):
    
    """Retourne les salles autour d'une salle dans un rayon spécifié."""
    
    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.autour_salle, "Salle", "Fraction")
    
    @staticmethod
    def autour_salle(salle, rayon):
        """Retourne toutes les salles autour de la salle indiquae.
        
        La salle passée en paramètre fait toujours parti des salles
        retournées. Le rayon est donné en salle (un rayon de 1 veut dire
        "la salle passée en paramètre et ses voisines immédiates".
        
        Si la salle a des coordonnées invalide, un rayon maximum de 4 est
        donné pour des raisons de calcul.
        
        """
        rayon = int(rayon)
        if salle.coords.invalide:
            rayon = rayon if rayon <= 4 else 4
            salles = []
            chemins = salle.salles_autour(rayon)
            if chemins:
                salles = [chemin.destination for chemin in chemins.chemins]
            
            salles.append(salle)
        else:
            o_coords = salle.coords.tuple()
            salles = []
            o_x, o_y, o_z = o_coords
            for coords, salle in importeur.salle._coords.items():
                x, y, z = coords
                distance = sqrt((x - o_x) ** 2 + (o_y - y) ** 2 + (o_z - \
                        z) ** 2)
                if distance <= rayon:
                    salles.append(salle)
        
        return salles

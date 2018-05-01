# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 DAVY Guillaume
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


"""Fichier contenant la classe Direction, détaillée plus bas."""

from abstraits.obase import *
from primaires.salle.coordonnees import Coordonnees
from math import radians, degrees
from .vecteur import Vecteur

class Direction(Vecteur):
    
    """Classe représentant la direction d'un véhicule.
    
    Elle gère les mêmes opérations qu'un vecteur mais possède quelques
    méthodes supplémentaire qui servent de raccourcie à ceux de la classe
    Vecteur quand on l'utilise il faut utiliser des angles en degré.
    Mais surtout elle applique les changements au navires quand on la modifie.
    
    """
    
    def __init__(self, vehicule, x=0, y=0, z=0):
        """Constructeur du vecteur"""
        Vecteur.__init__(self, x, y, z, vehicule)
        self.vehicule = vehicule
    
    def __getnewargs__(self):
        return (None, )
    
    def __repr__(self):
        """Affichage des coordonnées dans un cas de debug"""
        return "Direction(x={}, y={}, z={})".format(self.x, self.y, self.z)
    
    def tourner(self, angle):
        """Fait tourner / virer le véhicule autour de l'âxe Z."""
        self.tourner_autour_z(angle)
    
    def incliner(self, angle):
        """Incline le véhicule."""
        self.incliner(angle)

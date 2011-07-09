# -*-coding:Utf-8 -*

# Copyright (c) 2010 DAVY Guillaume
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


"""Fichier contenant la classe Vecteur, détaillée plus bas."""

from math import sqrt, cos, sin, radians, atan, degrees

from abstraits.obase import *
from primaires.salle.coordonnees import Coordonnees

class Vecteur(BaseObj):
    
    """Classe représentant un vecteur, gère les opérations usuelles dessus,
    ainsi que leur rotation autour d'un axe du repère.
    
    """
    
    def __init__(self, x=0, y=0, z=0):
        """Constructeur du vecteur"""
        BaseObj.__init__(self)
        self.x = x
        self.y = y
        self.z = z
    
    def __getnewargs__(self):
        return ()
    
    def __str__(self):
        """Affiche le vecteur plus proprement"""
        return "({}, {}, {})".format(self.x, self.y, self.z)
    
    def __repr__(self):
        """Affichage des coordonnées dans un cas de debug"""
        return "Vecteur(x={}, y={}, z={}})".format(self.x, self.y, self.z)
    
    @property
    def coordonnees(self):
        return Coordonnees(int(self.x), int(self.y), int(self.z))
    
    @property
    def tuple(self):
        """Retourne le tuple (x, y, z)"""
        return (self.x, self.y, self.z)
    
    def get_copie(self):
        """Retourne une copie de self"""
        return Vecteur(self.x, self.y, self.z)
    
    def tourner_autour_x(self, angle):
        r = radians(angle)
        x, y, z = self.x, self.y, self.z
        self.x = x * 1 + y * 0 + z * 0
        self.y = x * 0 + y * cos(r) - z * sin(r)
        self.z = x * 0 + y * sin(r) + z * cos(r)
    
    def tourner_autour_y(self, angle):
        r = radians(angle)
        x, y, z = self.x, self.y, self.z
        self.x = x * cos(r) - y * 0 + z * sin(r)
        self.y = x * 0 + y * 1 + z * 0
        self.z = x * sin(r) + y * 0 + z * cos(r)
    
    def tourner_autour_z(self, angle):
        r = radians(angle)
        x, y, z = self.x, self.y, self.z
        self.x = x * cos(r) - y * sin(r) + z * 0
        self.y = x * sin(r) + y * cos(r) + z * 0
        self.z = x * 0 + y * 0 + z * 1
    
    def incliner(self, angle):
        r = radians(angle)
        x, y, z = self.x, self.y, self.z
        n = sqrt(x*x+y*y)
        if n==0:
            raise(ValueError("impossible d'incliner un vecteur vertical"))
        self.x = x * cos(r) - z * x * sin(r) / n
        self.y = y * cos(r) - z * y * sin(r) / n
        self.z = z * cos(r) + sin(r) * n
    
    def direction(self):
        return - self.argument()
    
    def argument(self):
        x, y = self.x, self.y
        if x > 0:
            return degrees(atan(y/x))
        elif x < 0:
            return 180 - ( degrees(atan(y/x)) % 360 )
        elif y > 0:
            return 90
        elif y < 0:
            return -90
        else:
            return 0
    
    def norme(self):
        return sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
    
    def normalise(self):
        norme = self.norme()
        return Vecteur(self.x / norme, self.y / norme, self.z / norme)
    
    # Méthodes spéciales mathématiques
    def __neg__(self):
        """Retourne le vecteur négatif"""
        return Vecteur(-self.x, -self.y, -self.z)
    
    def __add__(self, autre):
        """Additionne deux vecteur"""
        return Vecteur(self.x + autre.x, self.y + autre.y, self.z + autre.z)
    
    def __sub__(self, autre):
        """Soustrait autre à self"""
        return Vecteur(self.x - autre.x, self.y - autre.y, self.z - autre.z)
    
    def __rmul__(self, valeur):
        """Multiplie le vecteur par valeur"""
        return Vecteur(self.x * valeur, self.y * valeur, self.z * valeur)

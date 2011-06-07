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


"""Fichier contenant la classe Coordonnees, détaillée plus bas."""

from abstraits.obase import *
from math import sqrt, cos, sin, radians
from primaires.salle.coordonnees import Coordonnees

class Vecteur(BaseObj):
    
    """Classe représentant un vecteur, gère les opérations usuelles dessus,
        ainsi que leur rotation autours d'un axe du repère
    """
    
    def __init__(self, x=0, y=0, z=0):
        """Constructeur du vecteur"""
        BaseObj.__init__(self)
        self.x = x
        self.y = y
        self.z = z
    
    def coordonnees(self):
        return Coordonnees(self.x, self.y, self.z)
    
    def __getnewargs__(self):
        return ()
    
    def __str__(self):
        """Affiche le vecteur plus proprement"""
        return "({}, {}, {})".format(self.x, self.y, self.z)
    
    def __repr__(self):
        """Affichage des coordonnées dans un cas de debug"""
        return "Vecteur(x={}, y={}, z={}})".format(self.x, self.y, self.z)
    
    def tuple(self):
        """Retourne le tuple (x, y, z)"""
        return (self.x, self.y, self.z)
    
    def get_copie(self):
        """Retourne une copie de self, non liée à parent"""
        return Vecteur(self.x, self.y, self.z)
    
    def tourner_autours_x(self, angle):
        r = radians(angle)
        x, y, z = self.x, self.y, self.z
        self.x =   x * 1      + y * 0      + z * 0
        self.y =   x * 0      + y * cos(r) + z * sin(r)
        self.z = - x * 0      + y * sin(r) + z * cos(r)
    
    def tourner_autours_y(self, angle):
        r = radians(angle)
        x, y, z = self.x, self.y, self.z
        self.x =   x * cos(r) + y * 0      + z * sin(r)
        self.y =   x * 0      + y * 1      + z * 0
        self.z = - x * sin(r) + y * 0      + z * cos(r)
    
    def tourner_autours_z(self, angle):
        r = radians(angle)
        x, y, z = self.x, self.y, self.z
        self.x =   x * cos(r) + y * sin(r) + z * 0
        self.y = - x * sin(r) + y * cos(r) + z * 0
        self.z =   x * 0      + y * 0      + z * 1
    
    def norme(self):
        return sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
    
    def normalise(self):
        norme = self.norme()
        return Vecteur(self.x / norme, self.y / norme, self.z / norme)
    
    #Opérateur mathématique
    
    def __neg__(self):
        """Additionne deux vecteur"""
        return Vecteur(- self.x, - self.y, - self.z)
    
    def __add__(self, other):
        """Additionne deux vecteur"""
        return Vecteur(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        """Additionne deux vecteur"""
        return Vecteur(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __rmul__(self, other):
        """Additionne deux vecteur"""
        return Vecteur(self.x * other, self.y * other, self.z * other)
    
    

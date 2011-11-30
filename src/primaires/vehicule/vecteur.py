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

from math import sqrt, cos, sin, radians, degrees, atan

from abstraits.obase import *
from primaires.salle.coordonnees import Coordonnees

# Constantes
NPRECISION = 5

class Vecteur(BaseObj):
    
    """Classe représentant un vecteur en trois dimensions.
    
    Elle gère les opérations usuelles dessus, ainsi que leur rotation
    autour d'un axe du repère.
    
    """
    
    def __init__(self, x=0, y=0, z=0):
        """Constructeur du vecteur"""
        BaseObj.__init__(self)
        self._x = x
        self._y = y
        self._z = z
    
    def __getnewargs__(self):
        return ()
    
    def __str__(self):
        """Affiche le vecteur plus proprement"""
        return "({}, {}, {})".format(self.x, self.y, self.z)
    
    def __repr__(self):
        """Affichage des coordonnées dans un cas de debug"""
        return "Vecteur(x={}, y={}, z={})".format(self.x, self.y, self.z)
    
    @property
    def coordonnees(self):
        return Coordonnees(self.x, self.y, self.z)
    
    @property
    def tuple(self):
        """Retourne le tuple (x, y, z)"""
        return (self.x, self.y, self.z)
    
    @property
    def norme(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
    
    @property
    def direction(self):
        """Retourne un angle en degré représentant la direction.
        
              0 => est
             45 => sud-est
             90 => sud
            135 => sud-ouest
            180 => ouest
            225 => nord-ouest
            270 => nord
            315 => nord-est
        
        """
        return -self.argument() % 360
    
    @property
    def inclinaison(self):
        """Retourne l'angle d'inclinaison en degré."""
        x, y, z = self.x, self.y, self.z
        n = sqrt(x ** 2 + y ** 2)
        if n == 0:
            if z == 0:
                return 0
            else:
                return 90
            
        return degrees(atan(z/n))
    
    @property
    def nom_direction(self):
        """Retourne le nom de la direction.
        
          0 => "est"
         45 => "sud-est"
        ...
        
        """
        direction = self.direction
        if direction < 22.5:
            return "est"
        elif direction < 67.5:
            return "sud-est"
        elif direction < 112.5:
            return "sud"
        elif direction < 157.5:
            return "sud-ouest"
        elif direction < 202.5:
            return "ouest"
        elif direction < 247.5:
            return "nord-ouest"
        elif direction < 292.5:
            return "nord"
        elif direction < 337.5:
            return "nord-est"
        else:
            return "est"
    
    def _get_x(self):
        return self._x
    def _set_x(self, x):
        self._x = round(x, NPRECISION)
    x = property(_get_x, _set_x)
    
    def _get_y(self):
        return self._y
    def _set_y(self, y):
        self._y = round(y, NPRECISION)
    y = property(_get_y, _set_y)
    
    def _get_z(self):
        return self._z
    def _set_z(self, z):
        self._z = round(z, NPRECISION)
    z = property(_get_z, _set_z)
    
    def copier(self):
        """Retourne une copie de self"""
        return Vecteur(self.x, self.y, self.z)
    
    def tourner_autour_x(self, angle):
        """Tourne autour de l'âxe X.
        
        L'angle doit être en degré.
        
        """
        r = radians(angle)
        x, y, z = self.x, self.y, self.z
        self.x = x * 1 + y * 0 + z * 0
        self.y = x * 0 + y * cos(r) - z * sin(r)
        self.z = x * 0 + y * sin(r) + z * cos(r)
        return self
    
    def tourner_autour_y(self, angle):
        """Tourne autour de l'âxe Y.
        
        L'angle doit être en degré.
        
        """
        r = radians(angle)
        x, y, z = self.x, self.y, self.z
        self.x = x * cos(r) - y * 0 + z * sin(r)
        self.y = x * 0 + y * 1 + z * 0
        self.z = x * sin(r) + y * 0 + z * cos(r)
        return self
    
    def tourner_autour_z(self, angle):
        """Tourne autour de l'âxe Z.
        
        L'angle doit être en degré.
        
        """
        r = radians(angle)
        x, y, z = self.x, self.y, self.z
        self.x = x * cos(r) - -1 * y * sin(r) + z * 0
        self.y = -1 * x * sin(r) + y * cos(r) + z * 0
        self.z = x * 0 + y * 0 + z * 1
        return self
    
    def incliner(self, angle):
        """Incline le véhicule.
        
        L'angle doit être en degré.
        
        """
        r = radians(angle)
        x, y, z = self.x, self.y, self.z
        n = sqrt(x * x + y * y)
        if n == 0:
            if z == 0 or sin(r) == 0 or (x == 0 and y == 0):
                self.x = 0
                self.y = 0
                self.z = z * cos(r)
            else:
                raise ValueError("impossible d'incliner un vecteur vertical")
        else:
            self.x = x * cos(r) - z * x * sin(r) / n
            self.y = y * cos(r) - z * y * sin(r) / n
            self.z = z * cos(r) + sin(r) * n
        
        return self
    
    def argument(self):
        x, y = self.x, self.y
        if x > 0:
            return degrees(atan(y / x))
        elif x < 0:
            return (180 + degrees(atan(y / x))) % 360
        elif y > 0:
            return 90
        elif y < 0:
            return -90
        else:
            return 0
    
    def normalise(self):
        norme = self.norme
        if norme == 0:
            raise ValueError("impossible de normaliser nul")
        
        return Vecteur(self.x / norme, self.y / norme, self.z / norme)
    
    def orienter(self, angle):
        """Oriente le vecteur horizontalement.
        
        L'angle doit être indiqué en degré.
        
        A la différence de tourner_autour_z, l'angle précisé est absolu.
        Après l'appelle à la méthode vecteur.orienter(180) par exemple,
        vecteur.direction doit être 180.
        
        """
        direction = self.direction
        angle -= direction
        self.tourner_autour_z(angle)
    
    # Méthodes spéciales mathématiques
    def __neg__(self):
        """Retourne le vecteur négatif."""
        return Vecteur(-self.x, -self.y, -self.z)
    
    def __add__(self, autre):
        """Additionne deux vecteurs."""
        return Vecteur(self.x + autre.x, self.y + autre.y, self.z + autre.z)
    
    def __sub__(self, autre):
        """Soustrait deux vecteurs."""
        return Vecteur(self.x - autre.x, self.y - autre.y, self.z - autre.z)
    
    def __rmul__(self, valeur):
        """Multiplie le vecteur par un nombre."""
        return Vecteur(self.x * valeur, self.y * valeur, self.z * valeur)

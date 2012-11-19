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


"""Ce fichier contient la classe Stat, détaillée plus bas."""

from abstraits.obase import BaseObj
from primaires.perso.exceptions.stat import *

# Flags :
NX = 0 # aucune exception ne sera levée
I0 = 1 # lève une exception si strictement inférieure à 0
IE0 = 2 # lève une exception si inférieure ou égale à 0
SM = 4 # lève une exception si strictement supérieure au MAX
SEM = 8 # lève une exception si supérieure ou égale au MAX

class Stat(BaseObj):
    
    """Cette classe définit une stat (ou caractéristique).
    
    Les attributs d'une stat sont :
    nom -- son nom
    symbole -- son symbole (utile pour le prompt)
    defaut -- sa valeur par défaut, celle donnée à un joueur à sa création
    marge -- la marge maximale
    max -- une chaîne de caractère représentant une autre stat
    flags -- les flags indiquant quand une exception doit être levée
    parent -- le parent hébergeant les stats
    
    """
    
    _nom = "stat"
    _version = 1
    def __init__(self, nom, symbole, defaut, marge, max, flags=I0, parent=None):
        """Constructeur d'une stat.
        Elle prend les mêmes paramètres que ceux passés dans l'ordre, dans
        la configuration.
        
        Voir : ./cfg_stats.py
        
        """
        BaseObj.__init__(self)
        self.nom = nom
        self.symbole = symbole
        self.defaut = defaut
        self.marge_min = 0
        self.marge_max = marge
        self.nom_max = max
        self.flags = flags
        self.parent = parent
        
        # Valeurs
        self.__base = self.defaut
        self.__variable = 0
        self.__max = None
        if self.parent and max:
            self.__max = getattr(self.parent, "_{}".format(max))
        
        self._construire()
    
    def __getnewargs__(self):
        return ("", "", "", 0, "")
    
    def __repr__(self):
        return "<stat {}={}>".format(self.nom, self.courante)
    
    def __str__(self):
        return "{}={} (base={}, variable={}, max={})".format(
                self.nom, self.courante, self.base, self.variable, self.max)
    
    @property
    def base(self):
        return self.__base
    
    @property
    def variable(self):
        return self.__variable
    
    @property
    def max(self):
        max = self.__max
        if max:
            max = max.courante
        
        return max
    
    def _get_courante(self):
        return self.__base + self.__variable
    def _set_courante(self, courante):
        """C'est dans cette propriété qu'on change la valeur courante
        de la stat.
        On passe par une méthode 'set' qui fait le travail.
        
        """
        self.set(courante, self.flags)
    
    courante = property(_get_courante, _set_courante)
    
    def set(self, courante, flags):
        """Modifie la stat courante.
        
        C'est dans cette méthode qu'on lève des exceptions en fonction des
        valeurs modifiées.
        
        NOTE IMPORTANTE: la valeur est modifiée quelque soit l'exception
        levée. L'exception est levée pour réagir à un certain comportement
        (par exemple, le joueur n'a plus de vitalité) mais elle n'empêchera
        pas la stat d'être modifiée.
        
        En revanche, on test bel et bien que la stat de base ne dépasse ni
        le max ni la marge.
        
        """
        base = courante - self.__variable
        if not self.parent.parent.est_immortel():
            # Levée d'exceptions
            if base < 0 and flags & I0:
                self.__base = 0
                raise StatI0
            if base <= 0 and flags & IE0:
                self.__base = 0
                raise StatIE0
            if self.max and flags & SM and base > self.max:
                raise StatSM
            if self.max and flags & SEM and base >= self.max:
                raise StatSEM
        
        if base > self.marge_max:
            base = self.marge_max
        if base < self.marge_min:
            base = self.marge_min
        
        if self.max and base > self.max:
            base = self.max
        if self.parent.parent.est_immortel() and self.max:
            base = self.max
        
        self.__base = base
    
    def __setattr__(self, nom, val):
        BaseObj.__setattr__(self, nom, val)

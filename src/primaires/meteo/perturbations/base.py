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


"""Ce fichier contient la classe BasePertu, détaillée plus bas."""

from math import sqrt, pow, ceil
from random import randint

from abstraits.id import ObjetID
from . import MetaPertu
from primaires.salle.coordonnees import Coordonnees

class BasePertu(ObjetID, metaclass=MetaPertu):
    
    """Classe abstraite représentant la base d'une perturbation météo.
    Cette classe contient tout ce qui est commun à toutes les perturbations
    météorologiques.
    
    """
    
    groupe = "perturbations"
    sous_rep = "meteo/perturbations"
    nom_pertu = ""
    rayon_max = 0 # à redéfinir selon la perturbation
    
    def __init__(self):
        """Constructeur d'un type"""
        ObjetId.__init__(self)
        self.centre = Coordonnees()
        self.rayon = randint(self.rayon_max / 2, self.rayon_max)
        self._age = 0
        self.duree = 10
        self.direction = "est"
        self.message = "Une perturbation roule au-dessus de votre tête."
    
    def __getnewargs__(self):
        return ()
    
    @property
    def age(self):
        return self._age
    
    def distance_au_centre(self, salle):
        """Retourne la distance de salle au centre de la perturbation"""
        x1 = salle.coords.x
        x2 = self.centre.x
        y1 = salle.coords.y
        y2 = self.centre.y
        return ceil(sqrt(pow(x1 - x2) + pow(y1 - y2)))
    
    def est_sur(self, salle):
        """Retourne True si salle est au-dessous de la perturbation"""
        return self.distance_au_centre(salle) <= self.rayon

ObjetID.ajouter_groupe(BasePertu)

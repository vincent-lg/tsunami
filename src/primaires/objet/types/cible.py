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


"""Fichier contenant le type cible."""

from abstraits.obase import BaseObj
from primaires.format.fonctions import supprimer_accents
from .base import BaseType

class Cible(BaseType):
    
    """Type d'objet: cible.
    
    """
    
    nom_type = "cible"
    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        BaseType.__init__(self, cle)
        self.elements = []
    
    def get_element(self, nom):
        """Retourne l'élément du nom indiqué.
        
        Si l'élément ne peut être trouvé, lève une exception ValueError.
        
        """
        nom = supprimer_accents(nom).lower()
        for element in self.elements:
            if supprimer_accents(element.nom).lower() == nom:
                return element
        
        raise ValueError("l'élément {} ne peut être trouvé".format(nom))
    
    def est_element(self, nom):
        """Retourne True si l'élément du nom indiqué est trouvé."""
        try:
            elt = self.get_element(nom)
        except ValueError:
            return False
        else:
            return True
    
    def ajouter_element(self, nom, *args, **kwargs):
        """Ajoute un élément.
        
        Le paramètre obligatoire est le nom de l'élément.
        Les paramètres supplémentaires (obligatoires ou non) sont transmis
        au constructeur de Element (voire la classe plus bas).
        
        Si le nom de l'élément est déjà utilisé, lève une exception ValueError.
        
        """
        if self.est_element(nom):
            raise ValueError("l'élément {} est déjà utilisé".format(nom))
        
        element = Element(nom, *args, **kwargs)
        self.elements.append(element)
        return element
    
    def supprimer_element(self, nom):
        """Supprime l'élément du nom indiqué."""
        nom = supprimer_accents(nom).lower()
        for i, element in enumerate(self.elements):
            if supprimer_accents(element.nom).lower == nom:
                del self.elements[i]
                return
        
        raise ValueError("l'élément {} ne peut être trouvé".format(nom))

class Element(BaseObj):
    
    """Classe représentant un élément de la cible.
    
    Il contient :
            nom -- le nom d'élément
            probabilite -- la probabilité de le toucher [1]
            points -- le nombre de points de l'élément
    
    [1] La probabilité totale n'est pas 100 mais la somme des probabilités
        de tous les éléments de la cible.
    
    """
    
    def __init__(self, nom, probabilite=1, points=1):
        """Constructeur de l'élément."""
        BaseObj.__init__(self)
        self.nom = nom
        self.probabilite = probabilite
        self.points = points
    
    def __getnewargs__(self):
        return ("inconnu", )
    
    def __repr__(self):
        return "<élément de cible {}>".format(self.nom)
    
    @property
    def msg_points(self):
        """Retourne une chaîne représentant le nombre de points."""
        points = self.points
        if points > 1:
            return "{} points".format(points)
        else:
            return "{} point".format(points)

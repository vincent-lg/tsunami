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


"""Fichier définissant les combinaisons possibles."""

from abstraits.obase import BaseObj

class Combinaison(BaseObj):
    
    """Classe représentant une combinaison abstraite."""
    
    points = None
    nom = None
    
    def __init__(self, combinaison, exterieures):
        """Constructeur de la combinaison.
        
        Les cartes contenues dans la liste combinaison sont celles formant
        la combinaison. Les autres sont contenues dans exterieures.
        
        """
        BaseObj.__init__(self)
        self.combinaison = combinaison
        self.exterieures = exterieures
        self._construire()
    
    def __getnewargs__(self):
        return (None, None)
    
    @property
    def nom(self):
        """Retourne le nom de la combinaison."""
        return "rien"
    
    @classmethod
    def forme(cls, pieces):
        """Retourne True si les pièces forment une combinaison.
        
        Les pièces doivent être transmises sous la forme d'une liste de listes. Les pièces de même valeur doivent être regroupées dans une liste et les pièces de plus grande valeur doivent apparaître en premier.
        
        Exemple s'inspirant, au lieu de pièces, des cartes standards :
            On a : 7 de coeur, as de coeur, 3 de carreau, 3 de trèffle...
            On doit recevoir : [[as coeur], [7 coeur], [3 carreau, 3 trèffle]]
        
        """
        return False

combinaisons = []
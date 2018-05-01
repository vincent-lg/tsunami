# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
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


"""Ce fichier contient la classe Element, détaillée plus bas."""

from abstraits.obase import BaseObj

class Element(BaseObj):
    
    """Classe décrivant un élément récoltable.
    
    Un élément récoltable est propre à une plante à une période donnée.
    Ce peut être un fruit, une feuille, une fleur, de l'écorce ou tout autre.
    Il s'agit simplement de l'association :
        objet -- d'un objet de n'importe quel type
        quantite -- d'une quantité maximum
    
    """
    
    def __init__(self, plante, periode, nom, objet, quantite):
        """Constructeur de la période."""
        BaseObj.__init__(self)
        self.plante = plante
        self.periode = periode
        self.nom = nom
        self.objet = objet
        self.quantite = quantite
    
    def __getnewargs__(self):
        return (None, None, "", None, 1)
    
    def __repr__(self):
        return "<élément {}: {} en quantité {}>".format(self.nom, 
                str(self), self.quantite)
    
    def __str__(self):
        return self.objet and self.objet.cle or "aucun"

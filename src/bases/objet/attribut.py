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


"""Fichier contenant la classe Attribut, définie plus bas."""

class Attribut:
    
    """Définition d'une classe attribut.
    Elle prend en paramètre :
    -   un constructeur
    -   une liste de taille inconnue de paramètres à passer au
        constructeur de l'attribut
    
    Elle possède une méthode 'construire' qui retourne l'attribut construit.
    
    """
    
    def __init__(self, constructeur, internes=(), l_externes=(),
            d_externes={}):
        """Constructeur d'un attribut"""
        self.constructeur = constructeur
        self.internes = inernes
        self.l_externes = l_externes
        self.d_externes = d_externes
    
    def construire(self, objet=None):
        """On construit et retourne l'attribut.
        Les paramètres internes sont rattachés à 'objet' passé en paramètre.
        Par exemple, si dans 'internes' se trouve le paramètre
        'description', on récupérera l'attribut 'description' de
        l'objet passé en paramètre.
        
        """
        l_attributs = []
        for attr in self.internes:
            if attr:
                l_attributs.append(getattr(objet, attr))
            else:
                l_attributs.append(objet)
        
        l_attributs.extend(self.l_externes)
        
        return self.constructeur(*l_attributs, **self.d_externes)

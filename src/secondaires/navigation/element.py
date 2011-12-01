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


"""Ce fichier contient la classe Element, détaillée plus bas."""

from abstraits.obase import BaseObj

class Element(BaseObj):
    
    """Cette classe contient un élément construit sur un type d'élément.
    
    Petite subtilité : la méthode __getattr__ a été redéfinie pour qu'il
    ne soit pas nécessaire de faire :
    >>> self.prototype.nom
    pour accéder au nom de l'élément.
    >>> self.nom
    suffit. La méthode va automatiquement chercher l'attribut dans
    'self.prototype' si l'attribut n'existe pas. Cela veut dire que si
    vous faites :
    >>> self.nom = "un autre nom"
    vous modifiez le nom de l'élément, sans modifier le prototype
    (le prototype ne doit pas être modifié depuis l'élément). Le nom de
    l'élément changera donc et sera différent de celui du prototype, le
    temps de la durée de vie de l'élément. Pour que :
    >>> self.nom
    fasse de nouveau référence au nom du prototype, il est conseillé de
    supprimer le nom de l'élément :
    >>> del self.nom
    
    """
    
    def __init__(self, prototype):
        """Constructeur de l'élément"""
        BaseObj.__init__(self)
        self.prototype = prototype
        if prototype:
            # On copie les attributs propres à l'element
            # Ils sont disponibles dans le prototype, dans la variable
            # _attributs
            # C'est un dictionnaire contenant en clé le nom de l'attribut
            # et en valeur le constructeur de l'objet
            for nom, val in prototype._attributs.items():
                val = val.construire(self)
                setattr(self, nom, val)
        
        self._construire()
    
    def __getnewargs__(self):
        return (None, )
    
    def __getattr__(self, nom_attr):
        """Si le nom d'attribut n'est pas trouvé, le chercher
        dans le prototype
        
        """
        return getattr(self.prototype, nom_attr)
    
    def __str__(self):
        return self.nom

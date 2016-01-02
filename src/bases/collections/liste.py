# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 LE GOFF Vincent
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


"""Fichier contenant la classe Liste détaillée plus bas."""

import copy

class Liste:
    
    """Classe représentant une liste, très semblable aux listes builtins.
    
    La grande différence est que cette liste est susceptible de contenir
    des objets prévus pour être enregistrés. Ces objets contiennent
    simplement un attribut e_existe qui doit être à True. Si il est à
    False, l'objet est ignoré (c'est-à-dire supprimé de la liste).
    
    A chaque action sur la liste, on la nettoie.
    
    """
    
    def __init__(self, *args):
        """Constructeur de la liste."""
        self.liste = list(*args)
        self.a_nettoyer = True
    
    def __getattr__(self, attr):
        return getattr(self.liste, attr)
    
    def __getstate__(self):
        return self.__dict__.copy()
    
    def __setstate__(self, dico_attr):
        self.__dict__.update(dico_attr)
    
    def __getitem__(self, item):
        return self.liste[item]
    
    def __setitem__(self, item, valeur):
        self.liste[item] = valeur
    
    def __delitem__(self, item):
        del self.liste[item]
    
    def __repr__(self):
        return repr(self.liste)
    
    def __str__(self):
        return str(self.liste)
    
    def __iter__(self):
        return iter(self.liste)
    
    def __len__(self):
        return len(self.liste)
    
    def __deepcopy__(self, memo):
        """Méthode surchargée pour permettre la copie de ces listes."""
        liste = copy.deepcopy(object.__getattribute__(self, "liste"), memo)
        return liste
    
    def __eq__(self, autre):
        return self.liste == autre
    
    def __ne__(self, autre):
        return self.liste != autre
    
    def nettoyer(self):
        """Nettoie la liste."""
        liste = []
        for elt in self.liste:
            if hasattr(elt, "e_existe"):
                if elt.e_existe:
                    liste.append(elt)
            else:
                liste.append(elt)
        
        self.liste[:] = liste

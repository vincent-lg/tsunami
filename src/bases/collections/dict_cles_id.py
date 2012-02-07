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


"""Ce fichier contient la classe DictClesID, détaillée plus bas."""

from .enr_dict import EnrDict

class DictClesID(EnrDict):
    
    """Dictionnaire contenant en clé des ObjetID.
    
    Le système d'écriture, en particulier, est différent. A chaque fois
    qu'on écrit une clé dans le dictionnaire, c'est son ID qui est écrite.
    Lors de la lecture, on récupère l'objet ID correspondant à l'ID.
    
    """
    
    def __delitem__(self, cle):
        """Retire l'élément."""
        del self.__dict[cle.id]
    
    def __getitem__(self, nom_elt):
        return self.__dict[nom_elt.id]
    
    def __setitem__(self, nom_elt, val_elt):
        """Modifie la valeur d'un dictionnaire."""
        EnrDict.__setitem__(self, nom_elt.id, val_elt)
    
    @property
    def __dict(self):
        return self._EnrDict__dict
    
    @property
    def to_dict(self):
        """Retourne un dictionnaire dont les clés sont les objets.
        
        Les valeurs restent identiques. Les clés du dictionnaire sont
        les objets correspondant à l'ID, pas l'ID elle-même.
        
        """
        c_dict = {}
        for cle, valeur in self.__dict.items():
            c_dict[cle.get_objet()] = valeur
        
        return c_dict
    
    def items(self):
        """Retourne les paires clé, valeur du dictionnaire."""
        return self.to_dict.items()
    
    def keys(self):
        return self.to_dict.keys()
    
    def values(self):
        """Retourne les valeurs du dictionnaire."""
        return self.to_dict.values()
    
    def __repr__(self):
        return repr(self.to_dict)
    
    def __str__(self):
        return str(self.to_dict)
    
    def get(self, item, ret=None):
        return self.to_dict.get(item, ret)

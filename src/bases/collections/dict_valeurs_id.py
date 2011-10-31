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


"""Ce fichier contient la classe DictValuersID, détaillée plus bas."""

from .enr_dict import EnrDict

class DictValeursID(EnrDict):
    
    """Dictionnaire contenant en valeur des ObjetID.
    
    Le système d'écriture, en particulier, est différent. A chaque fois
    qu'on écrit une valeur dans le dictionnaire, c'est son ID qui est écrite.
    Lors de la lecture, on récupère l'objet ID correspondant à l'ID.
    
    """
    
    def __getitem__(self, nom_elt):
        return self.__dict[nom_elt].get_objet()
    
    def __setitem__(self, nom_elt, val_elt):
        """Modifie la valeur d'un dictionnaire."""
        EnrDict.__setitem__(self, nom_elt, val_elt.id)
    
    @property
    def __dict(self):
        return self._EnrDict__dict
    
    @property
    def to_dict(self):
        """Retourne un dictionnaire dont les valeurs sont les objets.
        
        Les clés restent identiques. Les valeurs du dictionnaire sont
        les objets correspondant à l'ID, pas l'ID elle-même.
        
        """
        c_dict = {}
        for cle, valeur in self.__dict.items():
            c_dict[cle] = valeur.get_objet()
        
        return c_dict
    
    def items(self):
        """Retourne les paires clé, valeur du dictionnaire."""
        return self.to_dict.items()
    
    def values(self):
        """Retourne les valeurs du dictionnaire."""
        return self.to_dict.values()
    
    def __repr__(self):
        return repr(self.to_dict)
    
    def __str__(self):
        return str(self.to_dict)

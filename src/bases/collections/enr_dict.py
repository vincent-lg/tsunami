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


"""Ce fichier contient la classe EnrDict, détaillée plus bas."""

from abstraits.obase import *

class EnrDict(BaseObj):
    
    """Dictionnaire conçu pour s'enregistrer automatiquement quand ses
    valeurs sont modifiées.
    
    """
    
    def __init__(self, parent):
        """Construction du dictionnaire."""
        BaseObj.__init__(self)
        self.__dict = {}
        self.parent = parent
    
    def __getnewargs__(self):
        return (None, )
    
    def __contains__(self, item):
        return item in self.__dict
    
    def __getitem__(self, nom_elt):
        return self.__dict[nom_elt]
    
    def __setitem__(self, nom_elt, val_elt):
        """Modifie la valeur d'un dictionnaire."""
        self.__dict[nom_elt] = val_elt
        self.parent.enregistrer()
    
    def __delitem__(self, nom_elt):
        """Supprime l'élément."""
        del self.__dict[nom_elt]
        self.parent.enregistrer()
    
    def __repr__(self):
        return repr(self.__dict)
    
    def __str__(self):
        return str(self.__dict)
    
    def get(self, item, ret=None):
        return self.__dict.get(item, ret)
    
    def items(self):
        return self.__dict.items()
    
    def keys(self):
        return self.__dict.keys()
    
    def values(self):
        return self.__dict.values()


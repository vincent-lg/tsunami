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


"""Ce fichier définit la classe ID détaillée plus bas;"""

class ID:
    
    """Cette classe représente un identifiant unique d'un objet quelconque.
    Elle est utilisée par abstraits.id.ObjetID et ne doit pas être
    instanciée ailleurs.
    
    Voir : abstraits/id/__init__.py pour plus d'informations.
    
    Un identifiant se compose :
    -   d'un nom de groupe (str)
    -   d'un identifiant (int)
    
    """
    
    importeur = None
    
    def __init__(self, groupe, n_id):
        """Constructeur de la classe ID."""
        self.groupe = groupe
        self.id = n_id
    
    def __repr__(self):
        """On affiche l'ID ainsi : groupe:id"""
        return "{grp}:{id}".format(grp=self.groupe, id=self.id)
    
    def __str__(self):
        """On redirige sur repr"""
        return repr(self)
    
    def __hash__(self):
        return hash(str(self))
    
    def __eq__(self, autre):
        return hash(self) == hash(autre)
    
    def _objetid_(self):
        return True
    
    def get_objet(self):
        """Grâce à l'ID, on récupère l'objet correspondant.
        Pour savoir quel objet correspond à l'ID self, on demande à parid.
        Si l'objet n'existe pas, on retourne None.
        
        """
        return type(self).importeur.parid.get_objet(self)

# Fonctions

def est_id(objet):
    """Retourne True si l'objet est une id."""
    return isinstance(objet, ID)

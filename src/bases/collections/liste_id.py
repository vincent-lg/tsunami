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


"""Ce fichier contient la classe ListeID, détaillée plus bas."""

class ListeID(list):
    
    """Une version de liste destinée à contenir des objets IDs."""
    
    def __getitem__(self, item):
        """Retourne l'objet correspondant à l'ID."""
        return list.__getitem__(self, item).get_objet()
    
    def __setitem__(self, item, objet):
        """Ecrit l'ID de l'objet au lieu de l'objet lui-même"""
        list.__setitem__(self, item, objet.id)
    
    def __contains__(self, objet):
        """Retourne True si objet.id est dans la liste"""
        return list.__contains__(self, objet.id)
    
    def __iter__(self):
        """Parcourt (on veille à parcourir les objets, pas les IDs)"""
        return IterateurListeID(self)
    
    def append(self, objet):
        """Ajoute objet à la fin de la liste"""
        list.append(self, objet.id)
    
    def insert(self, indice, objet):
        """Ajoute objet.id à la position demandée"""
        list.insert(self, indice, objet.id)
    
    def remove(self, objet):
        """Retire l'objet passé en paramètre"""
        list.remove(self, objet.id)

class IterateurListeID:
    """Itérateur de la ListeID"""
    
    def __init__(self, liste):
        """Constructeur de l'itérateur"""
        self.liste = liste
        self.pos = 0
    
    def __next__(self):
        """Retourne l'élément suivant"""
        if self.pos < len(self.liste):
            objet = self.liste[self.pos]
            self.pos += 1
        else:
            raise StopIteration
        
        return objet

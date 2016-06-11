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


"""Ce fichier contient les classes utiles au combat à distance.

Clases définies :
    Cibles -- définie la liste des cibles (personnage -> personnage)
    choix -- liste les choix de cibles possibles pour chaque personnage

"""

from abstraits.unique import Unique

class Cibles(Unique):

    """Classe conteneur des cibles.
    
    On stock les cibles sous la forme d'un dictionnaire {personnage: cible}.
    
    """
    
    def __init__(self):
        """Constructeur du conteneur"""
        Unique.__init__(self, "combat", "cibles")
        self._cibles = {}
    
    def __getnewargs__(self):
        return ()
    
    def a_cible(self, personnage):
        """Retourne True si le personnage a une cible, False sinon."""
        return personnage.id in self._cibles.keys()
    
    def get_cible(self, personnage):
        """Retourne la cible si présente dans le dictionnaire ou None."""
        cible = self._cibles.get(personnage.id)
        if cible:
            cible = cible.get_objet()
        
        return cible
    
    def ajouter_cible(self, personnage, cible):
        """Ajoute une cible."""
        self._cibles[personnage.id] = cible.id
    
    def retirer_cible(self, personnage):
        """Retire la cible."""
        if personnage.id in self._cibles.keys():
            del self._cibles[personnage.id]

class Choix(Unique):

    """Classe conteneur des cibles possibles.
    
    On stock les cibles possibles sous la forme d'un dictionnaire
    {personnage: (cibles)}.
    
    """
    
    def __init__(self):
        """Constructeur du conteneur"""
        Unique.__init__(self, "combat", "choix")
        self._choix = {}
    
    def __getnewargs__(self):
        return ()
    
    def a_choix(self, personnage):
        """Retourne True si le personnage a un choix défini, False sinon."""
        return personnage.id in self._choix.keys()
    
    def get_choix(self, personnage):
        """Retourne les choix si présents dans le dictionnaire ou None."""
        cibles = self._cibles.get(personnage.id)
        if cibles:
            cibles = tuple(c.get_objet() for c in cibles)
        
        return cibles
    
    def ajouter_cible(self, personnage, cible):
        """Ajoute une cible."""
        self._cibles[personnage.id] = cible.id
    
    def retirer_cible(self, personnage):
        """Retire la cible."""
        if personnage.id in self._cibles.keys():
            del self._cibles[personnage.id]

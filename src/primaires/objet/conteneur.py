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


"""Ce fichier contient la classe ConteneurObjet, détaillée plus bas."""

from abstraits.obase import BaseObj
from bases.collections.liste_id import ListeID

class ConteneurObjet(BaseObj):
    
    """Conteneur standard d'objet.
    Cette classe peut être héritée (le sol d'une salle par exemple est un conteneur d'objet hérité) ou utilisée telle qu'elle.
    
    """
    
    def __init__(self, parent=None):
        """Constructeur du conteneur"""
        BaseObj.__init__(self)
        self._objets = []
        self.parent = parent
    
    def __getinitargs__(self):
        return ()
    
    def __iter__(self):
        """Itérateur"""
        return iter(self._objets)
    
    def ajouter_objet(self, objet):
        """On ajoute l'objet dans le conteneur"""
        if objet not in self._objets:
            self._objets.append(objet)
        else:
            raise ValueError("le conteneur {} contient déjà l'objet " \
                    "{}".format(self, objet))
        
        if self.parent:
            print("On enregistre la salle")
            self.parent.enregistrer()
    
    def retirer_objet(self, objet):
        """On retire l'objet du conteneur"""
        if objet in self._objets:
            self._objets.remove(objet)
        else:
            raise ValueError("le conteneur {} ne contient pas l'objet " \
                    "{}".format(self, objet))
        
        if self.parent:
            print("On enregistre la salle")
            self.parent.enregistrer()

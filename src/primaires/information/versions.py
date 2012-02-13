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


"""Ce fichier contient la classe Versions détaillée plus bas."""

from textwrap import wrap

from abstraits.obase import BaseObj

class Versions(BaseObj):

    """Classe conteneur des versions.
    Cette classe liste les modifications de version du logiciel
    (implémentations...).
    
    """
    
    def __init__(self):
        """Constructeur du conteneur"""
        BaseObj.__init__(self)
        self.__modifications = []
        self._lus = {}
    
    def __getnewargs__(self):
        return ()
    
    def __len__(self):
        return len(self.__modifications)
    
    def __getitem__(self, id):
        """Retourne une modification par son index."""
        return self.__modifications[id]
    
    def __setitem__(self, id, modif):
        """Edite une modification enregistrée."""
        self.__modifications[id] = modif
    
    def __delitem__(self, id):
        """Supprime une modification en fonction de son index."""
        del self.__modifications[id]
    
    def append(self, texte):
        """Ajoute une modification à la liste."""
        self.__modifications.append(texte)
    
    def afficher(self, offset=0):
        """Retourne les dernières modifications jusqu'à l'offset."""
        modifs = self.__modifications
        if offset > 0:
            modifs = modifs[-offset:]
        if len(modifs) > 0:
            for i in range(len(modifs)):
                id = "[|rgc|" + str(self.__modifications.index(modifs[i]) + 1)
                id += "|ff|] "
                indent = "\n" + (len(id) - 9) * " "
                modifs[i] = id + indent.join(wrap(modifs[i], 75))
            return "\n".join(modifs)
        else:
            return ""
    
    def afficher_dernieres_pour(self, personnage, lire=True):
        """Affiche les dernières modifications nons lues par 'personnage'."""
        ret = ""
        derniere = 0
        if personnage in self._lus:
            derniere = self._lus[personnage]
        if len(self) - derniere > 0:
            ret = self.afficher(len(self) - derniere)
        if lire:
            self._lus[personnage] = len(self)
        return ret

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


from fractions import Fraction

from abstraits.obase import BaseObj
from .parser import expressions

"""Fichier contenant la classe Fonction, détaillée plus bas."""

class Fonction(BaseObj):
    
    """Classe définissant une fonction.
    
    Une fonction est un composant d'une instruction prenant plusieurs paramètres et en retournant.
    Une fonction n'a d'intérêt que si elle retourne quelque chose.
    
    Ainsi, ce sont les grandes différences avec une action :
    *   une action est une instruction, une fonction n'en est qu'une composante
    *   une fonction retourne quelque chose, une action non
    *   une action modifie, une fonction consulte (principalement)
    
    """
    
    _parametres_possibles = None
    def __init__(self, fonction):
        """Construction d'une fonction."""
        BaseObj.__init__(self)
        type(self)._parametres_possibles = {}
        self.fonction = fonction
    
    def __getnewargs__(self):
        return (None, )
    
    def __str__(self):
        return str(self.fonction)
    
    def __call__(self, evenement):
        """Exécute l'action selon l'évènement."""
        parametres = self.convertir_parametres(evenement,
                self.fonction.parametres)
        fonction = self.quelle_fonction(parametres)
        return fonction(*parametres)
    
    def ajouter_types(self, methode, *parametres):
        """Ajoute une interprétation possible de la fonction.
        
        Les focntions peuvent avoir plusieurs interprétations possibles
        en fonction du type de leur paramètre.
        
        Les paramètres suplémentaires sont les types.
        Ce doivent tous être des chaînes de caractères.
        
        """
        if tuple((p for p in parametres if not isinstance(p, str))):
            raise TypeError("les types doivent être des type 'str'")
        
        if parametres in self._parametres_possibles:
            raise ValueError("les paramètres {} existent déjà pour " \
                    "cette fonction".format(parametres))
        
        self._parametres_possibles[parametres] = methode
    
    def quelle_fonction(self, parametres):
        """Retourne la fonction correspondant aux paramètres.
        
        Les paramètres se trouvent dans parametres.
        En fonction de leur type on doit savoir quelle fonction appeler.
        
        Si aucune interprétation des types n'est possible, on lève
        une exception ValueError.
        
        """
        # On forme un tuple des types des paramètres
        types = tuple(type(p).__name__ for p in parametres)
        
        if not types in self._parametres_possibles:
            raise ValueError("aucune interprétation de la fonction {} " \
                    "avec les paramètres {} n'est possible (types {})".format(
                    self.fonction.nom, self.fonction.parametres, types))
        
        return self._parametres_possibles[types]
    
    @classmethod
    def convertir_parametres(self, evt, parametres):
        """Convertit les paramètres passés, sous la forme de chaînes."""
        parametres = list(parametres)
        for i, p in enumerate(parametres):
            parametres[i] = parametres[i].get_valeur(evt)
        
        return parametres

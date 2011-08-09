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


import shlex

from .instruction import Instruction

"""Fichier contenant la classe Action, détaillée plus bas."""

actions = {} # dictionnaire des actions répertoriées

class Action(Instruction):
    
    """Classe définissant une action.
    
    Une action est une instruction effectuant une action précise (dire
    à un joueur, faire apparaître un objet, créer une tempête...).
    
    """
    
    _parametres_possibles = None
    def __init__(self):
        """Construction d'une action.
        
        """
        Instruction.__init__(self)
        self.parametres = ()
    
    def __str__(self):
        return self.nom + " " + " ".join(self.parametres)
    
    def __call__(self):
        """Exécute l'action"""
        return self.interpreter(*self.parametres)
    
    def verifier_type_parametres(self):
        """Cette méthode vérifie le type des paramètres passés.
        
        Elle se base sur le dictionnaire des paramètres possibles.
        
        Si une erreur survient, elle lève l'exception ValueError.
        Le message levé par cet exception est censé être transmis
        à l'immortel éditant le script.
        
        """
        params = self.parametres
        if not any(len(args) == len(params) for args in \
                self._parametres_possibles.keys()):
            raise ValueError("l'action {} ne peut s'exécuter avec {} " \
                    "paramètres".format(self.nom,
                    len(self._parametres_possibles), len(params)))
    
    @classmethod
    def peut_interpreter(cls, chaine):
        """La chaîne peut-elle être interprétée par la classe Action ?"""
        return True
    
    @classmethod
    def construire(cls, chaine):
        """Construit l'instruction.
        
        L'instruction est sous la forme :
            action parametre1 parametre2 parametre3 ...
        
        Le premier mot est donc le nom de l'action.  Ceux suivant
        sont ses paramètres.
        
        """
        parametres = shlex.split(chaine, posix=False)
        if not parametres:
            raise ValueError("Entrez au moins un nom d'action")
        
        nom_action = parametres[0]
        parametres = tuple(parametres[1:])
        
        # On cherche l'action
        try:
            action = actions[nom_action]()
        except KeyError:
            raise ValueError("l'action {} n'existe pas".format(nom_action))
        
        action.parametres = parametres
        action.verifier_type_parametres()
        
        return action

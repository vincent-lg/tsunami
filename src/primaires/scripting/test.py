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


"""Fichier contenant la classe Test détaillée plus bas."""

from abstraits.obase import *
from primaires.scripting.constantes.operateurs import OPERATEURS
from primaires.scripting.constantes.connecteurs import CONNECTEURS

class Test(BaseObj):
    
    """Classe contenant un test.
    
    Un test est constitué :
        variable -- d'une variable
        operateur -- d'un opérateur
        valeur -- d'une valeur que l'on compare à la variable
    
    Note : ces tests ne sont pas utilisables directement en condition où ils
    sont plus complexes.
    
    """
    
    def __init__(self, tests, variable, operateur, valeur):
        """Constructeur du test."""
        BaseObj.__init__(self)
        self.tests = tests
        self.variable = variable
        self.operateur = operateur
        self.valeur = valeur
        self._construire()
        
        # On fait maintenant quelques vérifications
        if tests is not None:
            evenement = tests.evenement
            if variable not in evenement.variables.keys():
                raise ValueError("la variable {} n'existe pas dans " \
                        "l'évènement {}".format(variable, evenement))
            
            if operateur not in OPERATEURS.keys():
                raise ValueError("l'opérateur {} n'existe pas".format(
                        operateur))
            
            v_type = evenement.variables[variable].type
    
    def __getnewargs__(self):
        return (None, "", "", "")
    
    def __bool__(self):
        """Retourne True si le test est vrai, False sinon"""
        # On convertit le test en code Python
        variable = self.tests.evenement.espaces.variables[self.variable]
        test_py = variable + " " + self.operateur + " " + self.valeur
        return eval(test_py)
    
    def __str__(self):
        return "{} {} {}".format(self.variable, self.operateur, self.valeur)

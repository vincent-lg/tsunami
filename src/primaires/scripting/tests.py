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


"""Fichier contenant la classe Tests détaillée plus bas."""

from abstraits.obase import *
from primaires.scripting.constantes.connecteurs import connecteurs

class Tests(BaseObj):
    
    """Classe contenant un ensemble de tests.
    
    Chaque test est relié par un connecteur (et / ou).
    
    Un ensemble de tests peut être évalué comme vrai ou faux.
    
    """
    
    def __init__(self, evenement):
        """Constructeur d'une suite de tests.
        
        Elle prend en paramètre :
            evenement -- l'évènement qui possède le test
        
        """
        BaseObj.__init__(self)
        self.__evenement = evenement
        self.__tests = []
        self.__liaisons = []
        self._construire()
    
    @property
    def evenement(self):
        return self.__evenement
    
    def ajouter_test(self, test, liaison="et"):
        """Ajoute un test à la suite.
        
        Le test est donné sous la forme d'un tuple :
            (variable, opérateur, valeur)
        
        On peut préciser une liaison qui sera "et" par défaut.
        
        """
        try:
            variable, operateur, valeur = test
        except ValueError:
            raise RuntimeError("erreur de syntaxe poru la construction " \
                    d'un test")
        
        test = Test(variable, operateur, valeur)
        self.__test.append(test)
        if len(self.__tests) > 0:
            self.__liaisons.append(liaison)
        self.evenement.parent.enregistrer()
    
    def __bool__(self):
        """Retourne True si les tests sont vrais, False sinon."""
        tests = [str(bool(test)) for test in self.__tests]
        py_test = tests[0]
        # On intercale un test, un connecteur
        for test, connecteur in zip(tests[1:], self.liaisons):
            py_connecteur = connecteurs[connecteur]
            py_test += " {} ".format(py_connecteur)
            py_test += test
        
        return eval(py_test)

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


"""Fichier contenant la classe Tests, détaillée plus bas."""

from .expression import Expression
from . import expressions

class Tests(Expression):
    
    """Expression tests."""
    
    nom = "tests"
    def __init__(self):
        """Constructeur de l'expression."""
        Expression.__init__(self)
        self.nom = None
        self.expressions = ()
    
    @classmethod
    def parsable(cls, chaine):
        """Retourne True si la chaîne est parsable, False sinon."""
        return True
     
    @classmethod
    def parser(cls, expressions):
        """Parse la chaîne.
        
        Retourne l'objet créé et la partie non interprétée de la chaîne.
        
        """
        objet = cls()
        
        # Parsage des expressions
        types = ("variable", "nombre", "chaine", "fonction", "operateur", "connecteur")
        types = tuple([expressions[nom] for nom in types])
        expressions = []
        while chaine.strip():
            types_app = [type for type in types if type.parsable(chaine)]
            if not types_app:
                raise ValueError("impossible de parser {}".format(expressions))
            elif len(types_app) > 1:
                raise ValueError("les tests {} peuvent être différemment interprétée".format(expression))
            
            type = types_app[0]
            arg, chaine = type.parser(chaine)
            print("reste", chaine)
        
        objet.expressions = tuple(expressions)
        
        return objet, chaine
    
    def get_valeur(self, evt):
        """Retourne la valeur du test (True ou False).
        
        Pour évaluer un test, on va laisser Python se débrouiller.
        On convertit chaque expression du test en son équivalent en code
        Python et on l'évalue ensuite.
        
        """
        py_tests = [t.code_python for t in self.arguments]
        code = " ".join(tests)
        return eval(code)
    
    def __repr__(self):
        return str(self.expresions)

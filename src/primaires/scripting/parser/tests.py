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
from .variable import RE_VARIABLE

class Tests(Expression):
    
    """Expression tests."""
    
    nom = "tests"
    def __init__(self):
        """Constructeur de l'expression."""
        Expression.__init__(self)
        self.nom = None
        self.parametres = ()
    
    @classmethod
    def parsable(cls, chaine):
        """Retourne True si la chaîne est parsable, False sinon."""
        fin_nom = chaine.find("(")
        nom = chaine[:fin_nom]
        chaine = chaine[:fin_nom + 1]
        return fin_nom >= 0  and RE_VARIABLE.search(nom)
    
    @classmethod
    def parser(cls, tests):
        """Parse la chaîne.
        
        Retourne l'objet créé et la partie non interprétée de la chaîne.
        
        """
        objet = cls()
        fin_nom = tests.find("(")
        nom = tests[:fin_nom]
        chaine = tests[fin_nom + 1:]
        objet.nom = nom
        
        # Parsage des paramètres
        types = ("variable", "nombre", "chaine", "tests")
        types = tuple([expressions[nom] for nom in types])
        parametres = []
        while True:
            chaine = chaine.lstrip(" ")
            if chaine.startswith(")"):
                chaine = chaine[1:]
                break
            
            types_app = [type for type in types if type.parsable(chaine)]
            if not types_app:
                raise ValueError("impossible de parser {}".format(tests))
            elif len(types_app) > 1:
                raise ValueError("la tests {] peut être différemment interprétée".format(tests))
            
            type = types_app[0]
            arg, chaine = type.parser(chaine)
            parametres.append(arg)
            print("reste", chaine)
            
            chaine.lstrip(" ")
            if chaine.startswith(","):
                chaine = chaine[1:]
            elif chaine.startswith(")"):
                chaine = chaine[1:]
                break
            else:
                raise ValueError("erreur de syntaxe dans la tests " \
                        "{}".format(tests))
        
        objet.parametres = tuple(parametres)
        
        return objet, chaine
    
    def get_valeur(self, evt):
        """Retourne la valeur de retour de la tests."""
        testss = type(self).importeur.scripting.testss
        if self.nom not in testss:
            raise ValueError("la tests {} est introuvable".format(self.nom))
        
        tests = testss[self.nom](self)
        
        return tests(evt)
    
    def __repr__(self):
        return self.nom + str(self.parametres)

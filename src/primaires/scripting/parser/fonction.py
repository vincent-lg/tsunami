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


"""Fichier contenant la classe Fonction, détaillée plus bas."""

from .expression import Expression
from . import expressions
from .variable import RE_VARIABLE

class Fonction(Expression):
    
    """Expression fonction."""
    
    nom = "fonction"
    def __init__(self):
        """Constructeur de l'expression."""
        Expression.__init__(self)
        self.nom = None
        self.parametres = ()
    
    def __repr__(self):
        params = [str(p) for p in self.parametres]
        return self.nom + "(" + ", ".join(params) + ")"
    
    @classmethod
    def parsable(cls, chaine):
        """Retourne True si la chaîne est parsable, False sinon."""
        chaine = chaine.lstrip()
        fin_nom = chaine.find("(")
        nom = chaine[:fin_nom]
        chaine = chaine[:fin_nom + 1]
        return fin_nom >= 0 and RE_VARIABLE.search(nom)
    
    @classmethod
    def parser(cls, fonction):
        """Parse la chaîne.
        
        Retourne l'objet créé et la partie non interprétée de la chaîne.
        
        """
        objet = cls()
        fin_nom = fonction.find("(")
        nom = fonction[:fin_nom]
        chaine = fonction[fin_nom + 1:].lstrip(" ")
        objet.nom = nom
        
        # Parsage des paramètres
        types = ("variable", "nombre", "chaine", "fonction", "calcul")
        types = tuple([expressions[nom] for nom in types])
        parametres = []
        while True:
            chaine = chaine.lstrip(" ")
            if chaine.startswith(")"):
                chaine = chaine[1:]
                break
            
            types_app = [type for type in types if type.parsable(chaine)]
            if not types_app:
                raise ValueError("impossible de parser {}".format(fonction))
            elif len(types_app) > 1:
                raise ValueError("la fonction {] peut être différemment " \
                        "interprétée".format(fonction))
            
            type = types_app[0]
            arg, chaine = type.parser(chaine)
            parametres.append(arg)
            
            chaine = chaine.lstrip(" ")
            if chaine.startswith(","):
                chaine = chaine[1:]
            elif chaine.startswith(")"):
                chaine = chaine[1:]
                break
            else:
                raise ValueError("erreur de syntaxe dans la fonction " \
                        "{}".format(fonction))
        
        objet.parametres = tuple(parametres)
        
        return objet, chaine
    
    def get_valeur(self, evt):
        """Retourne la valeur de retour de la fonction."""
        fonctions = type(self).importeur.scripting.fonctions
        if self.nom not in fonctions:
            raise ValueError("la fonction {} est introuvable".format(self.nom))
        
        fonction = fonctions[self.nom](self)
        
        return fonction(evt)
    
    @property
    def code_python(self):
        """Retourne le code Python associé à la fonction."""
        py_code = "fonctions['" + self.nom + "']"
        py_args = ["evt"] + [a.code_python for a in self.parametres]
        py_code += ".executer(" + ", ".join(py_args) + ")"
        return py_code

# -*-coding:Utf-8 -*

# Copyright (c) 2012 NOEL-BARON Léo
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


"""Ce fichier contient la classe Filtre, définie plus bas.

"""

import re

from abstraits.obase import BaseObj

class Filtre:
    
    """Classe de filtre.
    
    Cette classe modélise un filtre de recherche et permet de tester
    une valeur.
    
    """
    
    def __init__(self, opt_courte, opt_longue, test, type):
        """Constructeur de la classe"""
        self.opt_courte = opt_courte
        self.opt_longue = opt_longue
        self.test = test
        self.type = type
    
    def __str__(self):
        courte = "-" + self.opt_courte
        longue = "--" + self.opt_longue if self.opt_longue else ""
        if self.type:
            courte += " ARG"
            longue += "=ARG" if self.opt_longue else ""
        return courte + ", " + longue if self.opt_longue else courte
    
    def tester(self, objet, valeur):
        """Teste le filtre"""
        if self.type:
            if self.type == "str":
                try:
                    valeur = re.compile(valeur.replace("_b_", "|"))
                except re.error:
                    raise TypeError(
                            "le type précisé doit être une chaîne valide")
            elif self.type == "int":
                try:
                    valeur = int(valeur)
                except ValueError:
                    raise TypeError("le type précisé doit être un int")
            elif self.type == "bool":
                try:
                    assert valeur in ("1", "0")
                except AssertionError:
                    raise TypeError("le type précisé doit être un booléen")
                else:
                    valeur = True if valeur != "0" else False
        else:
            valeur = ""
        # On teste
        if callable(self.test):
            return self.test(objet, valeur)
        else:
            if self.type == "str":
                return valeur.search(getattr(objet, self.test))
            elif self.type in ("int", "bool"):
                return getattr(objet, self.test) == valeur
            else:
                return bool(getattr(objet, self.test))

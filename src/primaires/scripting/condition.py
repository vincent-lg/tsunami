# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 LE GOFF Vincent
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


"""Fichier contenant la classe Condition, détaillée plus bas."""

from .instruction import Instruction
from .parser import expressions

class Condition(Instruction):
    
    """Classe définissant une condition.
    
    Une condition est une instruction optionnellement suivie d'une suite
    de tests.
    Par exemple :
    >>> si variable = 5:
    ...     # Instructions si variable vaut 5
    ... sinon si titre(salle) = "...":
    ...     # Instructions si le titre de la salle est '...'
    ... sinon:
    ...     # Instruction sinon
    ... finsi
    
    """
    
    def __init__(self):
        """Constructeur d'une condition"""
        Instruction.__init__(self)
        self.type = None
        self.tests = None
    
    def __str__(self):
        ret = "|mr|" + self.type + "|ff|"
        if self.type == "si" or self.type == "sinon si":
            ret += " " + str(self.tests) + "|mr|:|ff|"
        elif self.type == "sinon":
            ret += "|mr|:|ff|"
        
        return ret
    
    @classmethod
    def peut_interpreter(cls, chaine):
        """La chaîne peut-elle être interprétée par la classe Condition."""
        mot_cles = ("si ", "sinon si ", "sinon", "finsi")
        return any(chaine.startswith(m) for m in mot_cles)
    
    @classmethod
    def construire(cls, chaine):
        """Construit l'instruction.
        
        L'instruction est sous la forme :
            type tests
            
        """
        taille_type = 0
        chn_condition = chaine
        condition = Condition()
        mot_cles = ("si ", "sinon si ", "sinon", "finsi")
        for mot in mot_cles:
            if chaine.startswith(mot):
                taille_type = len(mot)
                condition.type = mot.rstrip(" ")
                break
        
        if chaine.endswith(":"):
            chaine = chaine[:-1]
        
        condition.tests, chaine = expressions["tests"].parser(
                chaine[taille_type:])
        
        return condition
    
    def deduire_niveau(self, dernier_niveau):
        """Déduit le niveau de l'instruction."""
        self.niveau = dernier_niveau
        if self.type != "si":
            self.niveau -= 1
    
    def get_niveau_suivant(self):
        """Retourne le niveau de la prochaine instruction."""
        niveau = self.niveau
        if self.type != "finsi":
            niveau += 1
        
        return niveau
    
    @property
    def code_python(self):
        """Retourne le code Python de l'instruction."""
        py_types = {
            "si": "if",
            "sinon si": "elif",
            "sinon": "else",
            "finsi": "",
        }
        
        py_code = py_types[self.type]
        if self.type in ("si", "sinon si"):
            py_code += " " + self.tests.code_python
        
        if self.type != "finsi":
            py_code += ":"
        
        return py_code

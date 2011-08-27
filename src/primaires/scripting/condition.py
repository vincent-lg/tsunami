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


from .instruction import Instruction
from .parser import expressions

"""Fichier contenant la classe Condition, détaillée plus bas."""

class Condition(Instruction):
    
    """Classe définissant une condition.
    
    Une condition est une instruction optionnellement suivie d'une suite
    de tests.
    
    Par exemple :
        si variable = 5:
        sinon si titre(salle) = "...":
        sinon:
        finsi
    
    """
    
    def __init__(self):
        """Construction d'une condition.
        
        """
        Instruction.__init__(self)
        self.type = None
        self.tests = None
    
    def __str__(self):
        ret = self.type
        if self.type in ("si", "sinon si"):
            ret += str(self.tests) + ":"
        elif self.type == "sinon":
            ret += ":"
        
        return ret
    
    def __call__(self, evenement):
        """Exécute l'condition selon l'évènement."""
        raise NotImplementedError
    
    @classmethod
    def peut_interpreter(cls, chaine):
        """La chaîne peut-elle être interprétée par la classe Condition ?"""
        mot_cles = ("si", "sinon si", "sinon", "finsi")
        return any(chaine.startswith(m + " ") for m in mot_cles)
    
    @classmethod
    def construire(cls, chaine):
        """Construit l'instruction.
        
        L'instruction est sous la forme :
            type tests
            
        """
        chn_condition = chaine
        condition = Condition()
        mot_cles = ("si", "sinon si", "sinon", "finsi")
        for mot in mot_cles:
            if chaine.startswith(mot + " "):
                condition.type = mot
                break
        
        if chaine.endswith(":"):
            chaine = chaine[:-1]
        
        condition.tests = expressions["tests"].parser(
                chaine[len(condition.type) + 1:])
        
        return condition

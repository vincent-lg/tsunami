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

"""Fichier contenant la classe Commentaire, détaillée plus bas."""

class Commentaire(Instruction):
    
    """Classe définissant un commentaire.
    
    Un commentaire est une instruction commençant par un #,
    non interprétée par Python.
    
    """
    
    def __init__(self):
        """Construction d'un commentaire."""
        Instruction.__init__(self)
        self.commentaire = ""
    
    def __str__(self):
        return "#" + self.commentaire
    
    @classmethod
    def peut_interpreter(cls, chaine):
        """La chaîne peut-elle être interprétée par la classe Commentaire ?"""
        return chaine.startswith("#")
    
    @classmethod
    def construire(cls, chaine):
        """Construit l'instruction."""
        commentaire = chaine[1:]
        if commentaire and commentaire[0] != " ":
            commentaire = " " + commentaire
        
        ins = Commentaire()
        ins.commentaire = commentaire
        
        return ins
    
    @property
    def code_python(self):
        """Retourne le code Python associé à l'instruction."""
        py_code = "#" + self.commentaire
        return py_code

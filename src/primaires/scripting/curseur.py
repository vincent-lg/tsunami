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


"""Fichier contenant la classe Curseur, détaillée plus bas."""

class Curseur:
    
    """Classe définissant un curseur pour le parcourt du scripting.
    
    Un curseur est un objet qui conserve en mémoire la ligne et le niveau
    d'indentation du bloc exécuté.
    
    Quand on exécute une suite d'actions, le curseur se contente de
    passer d'une ligne à l'autre.
    
    En revanche, quand il s'agit de conditions, la première condition du
    bloc (une condition en si ...) est testée.
    Si elle est vraie, le curseur va explorer les instructions du bloc.
    Sinon, on passe à la condition suivante du bloc, si elle existe.
    Sinon, on recommence à la fin déclarée du bloc.
    
    """
    
    def __init__(self):
        """Constructeur d'un curseur."""
        self.ligne = 0
        self.niveau = 0
        self.valide = {}
    
    def executer_instructions(self, evenement, instructions):
        """Parcourt la suite des instructions."""
        try:
            instruction = instructions[0]
        except IndexError:
            return
        
        while instruction:
            print("Exec", instruction, instruction.niveau, self.niveau)
            if self.niveau >= instruction.niveau:
                instruction(self, evenement)
            else:
                self.ligne += 1
            
            try:
                instruction = instructions[self.ligne]
            except IndexError:
                instruction = None

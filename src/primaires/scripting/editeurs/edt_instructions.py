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
# pereIBILITY OF SUCH DAMAGE.


"""Ce fichier contient l'éditeur EdtInstructions, détaillé plus bas."""

from textwrap import wrap

from primaires.interpreteur.editeur import Editeur
from primaires.interpreteur.editeur.env_objet import EnveloppeObjet
from primaires.format.fonctions import *

class EdtInstructions(Editeur):
    
    """Contexte-éditeur d'une suite d'instructions.
    
    L'objet appelant est la suite de tests contenant le code.
    Par code, il faut entendre ici la liste des instructions constituant
    un script.
    
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
    
    def accueil(self):
        """Message d'accueil du contexte"""
        tests = self.objet
        instructions = tests.instructions
        evenement = tests.evenement
        appelant = evenement.script.parent
        msg = "| |tit|"
        msg += "Edition d'un script de {}[{}]".format(appelant,
                evenement.nom).ljust(61)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        variables = evenement.variables
        msg += "Variables :\n  "
        if variables:
            msg += "\n  ".join(["{:<15} : {}".format(var.nom, var.aide) \
                    for var in variables.values()])
        else:
            msg += "Aucune variable n'a été définie pour ce script."
        
        msg += "\n\nInstructions :\n  "
        if instructions:
            msg += "\n  ".join(["{:>3} {}{}".format(i + 1,
                    "  " * instruction.niveau, instruction) \
                    for i, instruction in enumerate(instructions)])
        else:
            msg += "Aucune instruction n'est définie dans ce script."
        
        return msg
    
    def interpreter(self, msg):
        """Interprétation de l'éditeur"""
        tests = self.objet
        try:
            tests.ajouter_instruction(msg)
        except ValueError as err:
            self.pere << "|err|" + str(err) + "|ff|"
        else:
            self.actualiser()

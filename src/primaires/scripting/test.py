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


"""Fichier contenant la classe Test détaillée plus bas."""

import traceback
from fractions import Fraction

from abstraits.id import ObjetID
from .parser import expressions
from primaires.scripting.constantes.connecteurs import CONNECTEURS
from .instruction import Instruction

class Test(ObjetID):
    
    """Classe contenant un ensemble de tests.
    
    """
    
    groupe = "test"
    sous_rep = "scripting/tests"
    def __init__(self, evenement, chaine_test=""):
        """Constructeur d'une suite de tests.
        
        Elle prend en paramètre :
            evenement -- l'évènement qui possède le test
            chaine_test -- la suite de test sous la forme d'une chaîne
        
        """
        ObjetID.__init__(self)
        self.__evenement = evenement
        self.__tests = None
        self.__instructions = []
        self.dernier_niveau = 0
        self.etape = None
        self._construire()
        
        if chaine_test:
            self.construire(chaine_test)
    
    def __getnewargs__(self):
        return (None, )
    
    def __str__(self):
        return str(self.__tests)
    
    @property
    def evenement(self):
        return self.__evenement
    
    @property
    def instructions(self):
        """Retourne une liste déréférencée des instructions."""
        return list(self.__instructions)
    
    @property
    def appelant(self):
        """Retourne l'appelant, c'est-à-dire le parent du script."""
        return self.evenement.script.parent
    
    @property
    def acteur(self):
        """Retourne l'acteur de la quête.
        
        C'est la variable personnage. Elle doit donc exister.
        
        """
        return self.evenement.espaces.variables["personnage"]
    
    def construire(self, chaine_test):
        """Construit la suite de chaînes en fonction de la chaîne.
        
        """
        # On essaye d'interpréter la suite de tests
        self.__tests = expressions["tests"].parser(chaine_test)[0]
        self.appelant.enregistrer()
    
    def ajouter_instruction(self, message):
        """Construit et ajoute l'instruction."""
        type_instruction = Instruction.test_interpreter(message)
        instruction = type_instruction.construire(message)
        instruction.deduire_niveau(self.dernier_niveau)
        self.dernier_niveau = instruction.get_niveau_suivant()
        self.__instructions.append(instruction)
        self.evenement.appelant.enregistrer()
    
    def remplacer_instruction(self, ligne, message):
        """Remplace une instruction."""
        if ligne not in range(len(self.__instructions)):
            raise IndexError("la ligne {} n'existe pas".format(ligne))
        
        ancienne_instruction = self.__instructions[ligne]
        type_instruction = Instruction.test_interpreter(message)
        instruction = type_instruction.construire(message)
        instruction.niveau = ancienne_instruction.niveau
        self.__instructions[ligne] = instruction
        self.evenement.appelant.enregistrer()
    
    def tester(self, evenement):
        """Test le tests."""
        # Si le test est relié à une quête, on test le niveau dans la quête
        etape = self.etape
        if etape:
            if not self.acteur.quetes[etape.quete.cle].peut_faire(
                    etape.quete, etape.niveau):
                return False
        
        if not self.__tests:
            return True
        
        py_code = self.__tests.code_python
        print("Evaluation de", py_code)
        globales = self.get_globales(evenement)
        return bool(eval(py_code, globales))
    
    def get_globales(self, evenement):
        """Retourne le dictionnaire des globales d'exécution."""
        # Constitution des globales
        return {
            "actions": type(self).importeur.scripting.actions,
            "fonctions": type(self).importeur.scripting.fonctions,
            "variables": evenement.espaces.variables,
            "evt": evenement,
            "Fraction": Fraction,
            "importeur": type(self).importeur,
        }
    
    def executer_instructions(self, evenement):
        """Convertit et exécute la suite d'instructions.
        
        Pour plus de facilité, on convertit le script en Python pour l'heure 
        avant l'exécution.
        
        """
        etape = self.etape
        if etape:
            self.acteur.quetes[etape.quete.cle].deverouiller()
        
        lignes = []
        instructions = self.instructions
        for instruction in instructions:
            lignes.append((" " * 4 * instruction.niveau) + instruction.code_python)
        
        code = "\n".join(lignes)
        print("Code :", code, sep="\n")
        
        # Constitution des globales
        globales = self.get_globales(evenement)
        
        # Exécution
        try:
            exec(code, globales)
        except Exception:
            print(traceback.format_exc())
        
        # Si le test est relié à une quête
        if etape:
            # Si aucun verrou n'a été posé
            if not self.acteur.quetes[etape.quete.cle].verrouille:
                self.acteur.quetes.valider(etape.quete, etape.niveau)

ObjetID.ajouter_groupe(Test)

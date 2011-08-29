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


"""Fichier contenant la classe Tests détaillée plus bas."""

import shlex
import traceback

from abstraits.obase import *
from primaires.scripting.constantes.connecteurs import CONNECTEURS
from .test import Test
from .instruction import Instruction

class Tests(BaseObj):
    
    """Classe contenant un ensemble de tests.
    
    Chaque test est relié par un connecteur (et / ou).
    
    Un ensemble de tests peut être évalué comme vrai ou faux.
    
    """
    
    def __init__(self, evenement):
        """Constructeur d'une suite de tests.
        
        Elle prend en paramètre :
            evenement -- l'évènement qui possède le test
        
        """
        BaseObj.__init__(self)
        self.__evenement = evenement
        self.__tests = []
        self.__connecteurs = []
        self.__instructions = []
        self.dernier_niveau = 0
        self._construire()
    
    def __getnewargs__(self):
        return (None, )
    
    def __iter__(self):
        return iter(list(self.__tests))
    
    def __str__(self):
        if not self.__tests:
            return "dans tous les cas"
        
        pr_test = str(self.__tests[0])
        msg = pr_test
        if len(self.__tests) > 1:
            msg += " "
            for test, connecteur in zip(self.__tests[1:], self.__connecteurs):
                msg += "{} {}".format(connecteur, test)
        
        return msg
    
    @property
    def evenement(self):
        return self.__evenement
    
    @property
    def instructions(self):
        """Retourne une liste déréférencée des instructions."""
        return list(self.__instructions)
    
    def ajouter_test(self, test, connecteur="et"):
        """Ajoute un test à la suite.
        
        Le test est donné sous la forme d'un tuple :
            (variable, opérateur, valeur)
        
        On peut préciser un connecteur qui sera "et" par défaut.
        
        """
        try:
            variable, operateur, valeur = test
        except ValueError:
            raise ValueError("erreur de syntaxe pour la construction " \
                    "d'un test")
        
        test = Test(self, variable, operateur, valeur)
        if len(self.__tests) > 0:
            self.__connecteurs.append(connecteur)
        
        self.__tests.append(test)
        self.evenement.script.parent.enregistrer()
    
    def __bool__(self):
        """Retourne True si les tests sont vrais, False sinon."""
        tests = [str(bool(test)) for test in self.__tests]
        py_test = tests[0]
        # On intercale un test, un connecteur
        for test, connecteur in zip(tests[1:], self.__connecteurs):
            py_connecteur = CONNECTEURS[connecteur]
            py_test += " {} ".format(py_connecteur)
            py_test += test
        
        return eval(py_test)
    
    def construire(self, chaine):
        """Construit la suite de chaînes en fonction de la chaîne.
        
        La chaîne se présente sous la forme :
            test1 [operateur test2 [operateur test3 [...]]]
        
        Par exemple :
            objet = "epee_longue" et nombre > 5
        
        Attention : aucun test ne doit déjà exister.
        
        """
        if self.__tests:
            raise ValueError("la chaîne de test n'est pas vide.")
        
        # On transforme la chaîne en liste
        liste = shlex.split(chaine, posix=False)
        tests, connecteurs = self.__extraire_tests(liste, True)
        if not tests:
            raise ValueError("aucun test n'a été interprété")
        
        test = tests[0]
        if not test:
            raise ValueError("aucun test n'a été interprété")
        
        self.ajouter_test(test)
        for test, connecteur in zip(tests[1:], CONNECTEURS):
            self.ajouter_test(test, connecteur)
    
    def __extraire_tests(self, liste, debut=False, tests=None,
            connecteurs=None):
        """Extrait de la liste le test et le connecteur, si debut == True."""
        tests = tests or []
        connecteurs = connecteurs or []
        test = self.__extraire_test(liste)
        tests.append(test)
        retour = True
        while retour:
            retour = self.__extraire_connecteur(liste)
            if retour:
                tests.append(retour)
                retour = self.__extraire_test(liste)
                if not retour:
                    raise ValueError("erreur de parsage de condition")
        
        return tests, connecteurs
    
    def __extraire_connecteur(self, liste):
        """Extrait le connecteur et le retourne."""
        if not liste:
            return None
        
        connecteur = liste[0]
        liste[:] = liste[1:]
        return connecteur if connecteur in CONNECTEURS.keys() else None
    
    def __extraire_test(self, liste):
        """Extrait le test et le retourne."""
        if not liste:
            return None
        
        # On cherche le premier connecteur
        pos_conns = [liste.index(conn) for conn in coNECTEURS.keys() \
                if conn in liste]
        if pos_conns:
            pos = min(pos_conns)
            test = tuple(liste[pos - 1:])
            liste[:] = liste[pos:]
        else:
            test = tuple(liste)
            liste[:] = []
        
        return test
    
    def ajouter_instruction(self, message):
        """Construit et ajoute l'instruction."""
        type_instruction = Instruction.test_interpreter(message)
        instruction = type_instruction.construire(message)
        instruction.deduire_niveau(self.dernier_niveau)
        self.dernier_niveau = instruction.get_niveau_suivant()
        self.__instructions.append(instruction)
        self.evenement.appelant.enregistrer()
    
    def executer_instructions(self, evenement):
        """Convertit et exécute la suite d'instructions.
        
        Pour plus de facilité, on convertit le script en Python pour l'heure 
        avant l'exécution.
        
        """
        lignes = []
        instructions = self.instructions
        for instruction in instructions:
            lignes.append((" " * 4 * instruction.niveau) + instruction.code_python)
        
        code = "\n".join(lignes)
        print("Code :", code, sep="\n")
        
        # Constitution des globales
        globales = {
            "actions": type(self).importeur.scripting.actions,
            "fonctions": type(self).importeur.scripting.fonctions,
            "variables": evenement.espaces.variables,
            "evt": evenement,
        }
        
        # Exécution
        try:
            exec(code, globales)
        except Exception:
            print(traceback.format_exc())
            
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


"""Ce fichier contient l'éditeur EdtEvenement, détaillé plus bas."""

from textwrap import wrap

from primaires.interpreteur.editeur import Editeur
from primaires.interpreteur.editeur.env_objet import EnveloppeObjet
from primaires.format.fonctions import *
from .edt_instructions import EdtInstructions

class EdtEvenement(Editeur):
    
    """Contexte-éditeur d'un évènement.
    
    L'objet appelant est l'évènement.
    
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
    
    def accueil(self):
        """Message d'accueil du contexte"""
        evenement = self.objet
        msg = "| |tit|"
        msg += "Edition de l'évènement {} de {}".format(evenement.nom,
                evenement.script.parent).ljust(71)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += "Description :\n    "
        msg += "\n    ".join(wrap(evenement.aide_longue))
        msg += "\n\nVariables définies :\n"
        msg += "  "
        variables = evenement.variables
        if variables:
            msg += "\n  ".join(["{:<15} : {}".format(var.nom, var.aide) \
                    for var in variables.values()])
        else:
            msg += "Aucune variable n'a été définie pour ce script."
        
        msg += "\n\nConditions :"
        tests = evenement.tests
        if tests:
            msg += "\n  " +"\n  ".join(["{:>3}. si {}".format(i + 1, test) \
                    for i, test in enumerate(tests)])
        msg += "\n    |cmd|*|ff|  sinon"
        return msg
    
    def interpreter(self, msg):
        """Interprétation de l'éditeur"""
        evenement = self.objet
        if msg == "*":
            enveloppe = EnveloppeObjet(EdtInstructions, evenement.sinon)
            enveloppe.parent = self
            contexte = enveloppe.construire(self.pere)
            
            self.migrer_contexte(contexte)
        elif msg.isdigit():
            no_tests = int(msg) - 1
            try:
                tests = evenement.tests[no_tests]
            except IndexError:
                self.pere << "|err|Ce test n'existe pas.|ff|"
            else:
                enveloppe = EnveloppeObjet(EdtInstructions, tests)
                enveloppe.parent = self
                contexte = enveloppe.construire(self.pere)
                
                self.migrer_contexte(contexte)
        else:
            try:
                evenement.ajouter_test(msg)
            except ValueError as err:
                self.pere << "|err|Erreur lors du parsage du test.|ff|"
            else:
                self.actualiser()

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

import traceback
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
        self.ajouter_option("?", self.opt_aide_generale)
        self.ajouter_option("?s", self.opt_aide_syntaxe)
        #self.ajouter_option("?o", self.opt_aide_options)
        #self.ajouter_option("?f", self.opt_aide_fonctions)
        #self.ajouter_option("?a", self.opt_aide_actions)
        self.ajouter_option("r", self.opt_remplacer_instruction)
        self.ajouter_option("q", self.opt_relier_quete)
    
    def opt_remplacer_instruction(self, arguments):
        """Remplace une ligne par une nouvelle instruction."""
        test = self.objet
        instructions = test.instructions
        if not arguments.strip():
            self.pere << "|err|Entrez un numéro de ligne.|ff|"
            return
        
        arguments = arguments.split(" ")
        no = arguments[0]
        ligne = " ".join(arguments[1:])
        
        try:
            no = int(no) - 1
            assert no >= 0
            assert no < len(instructions)
        except (ValueError, AssertionError):
            self.pere << "|err|Entrez un numéro de ligne valide.|ff|"
            return
        
        if not ligne.strip():
            self.pere << "|err|Entrez une nouvelle instruction " \
                    "pour remplacer celle en ligne {}.|ff|".format(no + 1)
            return
        
        try:
            test.remplacer_instruction(no, ligne)
        except ValueError as err:
            self.pere << "|err|" + str(err) + ".|ff|"
        else:
            self.actualiser()
    
    def opt_relier_quete(self, argument):
        """Relie à une quête.
        
        La quête doit être au format :
            nom_quete:niveau
        
        """
        test = self.objet
        if not argument.strip():
            self.pere << "|err|Précisez <quete:niveau>.|ff|"
            return
        
        try:
            quete, niveau = argument.split(":")
        except ValueError:
            self.pere << "|err|Formattage de quête invalide.|ff|"
        else:
            # On cherche la quête
            if not quete in type(self).importeur.scripting.quetes:
                self.pere << "|err|Quête {} inconnue.|ff|".format(quete)
                return
            
            quete = type(self).importeur.scripting.quetes[quete]
            try:
                etape = quete[niveau]
            except KeyError:
                self.pere << "|err|Le niveau {} est inconnue pour la " \
                        "quête {}.|ff|".format(niveau, quete)
                return
            
            etape.test = test
            test.etape = etape
            self.actualiser()
    
    def opt_aide_generale(self, argument):
        """Option aide générale.
        
        Aucun argument n'est attendue.
        
        """
        self.pere << \
            "|rg|Bienvenue dans l'éditeur d'instruction.|ff|\n\n" \
            "Vous pouvez ici entrer des instructions en respectant " \
            "une certaine syntaxe\net modifier les instructions déjà " \
            "existantes. Vous pouvez obtenir plus d'aide\ngrâce " \
            "aux sujets suivants :\n" \
            "  |cmd|/?s|ff| affiche de l'aide sur la |syntaxe|ff| du " \
            "scripting\n" \
            "  |cmd|/?o|ff| affiche la liste des |ent|options|ff| de " \
            "l'éditeur disponibles\n" \
            "  |cmd|/?a|ff| affiche la liste des |ent|actions|ff| " \
            "disponibles\n" \
            "  |cmd|/?f|ff| affiche la liste des |ent|fonctions|ff| " \
            "disponibles.\n\n" \
            "Si donc la syntaxe du scripting ne vous est pas familière, " \
            "il vous est\nconseillé de lire l'aide consacrée en tapant " \
            "|cmd|/?s|ff|.\nSi vous connaissez la syntaxe mais " \
            "que vous voulez connaître les\npossibilités actuelles " \
            "du scripting, tapez |cmd|/?a|ff| pour connaître " \
            "la liste des\nactions et |cmd|/?f|ff| pour connaître " \
            "la liste des fonctions."
    
    def opt_aide_syntaxe(self, argument):
        """Option aide syntaxe.
        
        L'argument peut préciser l'aide spécifique.
        -   action      Syntaxe d'une action
        -   condition   Syntaxe d'une condition
        -   affectation Syntaxe d'une affectation
        
        """
        sujets = type(self).importeur.scripting.sujets_aides
        if not argument:
            self.pere << sujets["syntaxe"]
        else:
            self.pere << "A faire..."
    
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
        
        msg += "\n\n"
        if tests.etape:
            msg += "|att|ATTENTION : ce script est relié à la quête " \
                    "{}:{}.\n\n|ff|".format(tests.etape.quete.cle,
                    tests.etape.niveau)
        
        msg += "Instructions :\n  "
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
            print(traceback.format_exc())
            self.pere << "|err|" + str(err) + "|ff|"
        else:
            self.actualiser()

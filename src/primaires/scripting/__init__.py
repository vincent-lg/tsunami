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


"""Fichier contenant le module primaire scripting."""

import os
import re
from collections import OrderedDict

from abstraits.module import *
from .instruction import Instruction
from .condition import Condition
from .affectation import Affectation
from .action import Action, actions as lst_actions
from . import parser
from . import commandes
from .quete.quete import Quete
from .quete.etape import Etape
from .test import Test
from .editeurs.qedit import EdtQedit
from .constantes.aide import *
from .script import scripts

class Module(BaseModule):
    
    """Cette classe contient les informations du module primaire scripting.
    
    Ce module gère le langage de script utilisé pour écrire des quêtes et
    personnaliser certains objets de l'univers. Il regroupe également les
    éditeurs et les objets gérant les quêtes.
    
    """
    
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "scripting", "primaire")
        self.cfg = None
        self.fonctions = {}
        self.actions = {}
        self.commandes = {}
        self.quetes = {}
        self.sujets_aides = {
            "syntaxe": syntaxe,
        }
    
    def init(self):
        """Initialisation"""
        # Chargement des actions
        self.charger_actions()
        self.charger_fonctions()
        
        # Chargement des quêtes
        quetes = self.importeur.supenr.charger_groupe(Quete)
        for quete in quetes:
            if quete.parent is None:
                self.quetes[quete.cle] = quete
        
        # Chargement des étapes et tests
        etapes = self.importeur.supenr.charger_groupe(Etape)
        tests = self.importeur.supenr.charger_groupe(Test)
        BaseModule.init(self)
    
    def ajouter_commandes(self):
        """Ajout des commandes dans l'interpréteur"""
        self.commandes = [
            commandes.qedit.CmdQedit(),
        ]
        
        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)
        
        # Ajout de l'éditeur 'qedit'
        self.importeur.interpreteur.ajouter_editeur(EdtQedit)
    
    def preparer(self):
        """Préparation du module.
        
        On initialise les scripts.
        
        """
        for script in scripts:
            script.init()
    
    def charger_actions(self):
        """Chargement automatique des actions."""
        # Elles se trouvent dans le sous-répertoire actions
        chemin = self.chemin + os.sep + "actions"
        chemin_py = "primaires.scripting.actions"
        for nom_fichier in os.listdir(chemin):
            if not nom_fichier.startswith("_") and nom_fichier.endswith(".py"):
                nom_module = nom_fichier[:-3]
                chemin_py_mod = chemin_py + ".{}".format(nom_module)
                action = __import__(chemin_py_mod)
                action = getattr(getattr(getattr(getattr(action, "scripting"),
                        "actions"), nom_module), "ClasseAction")
                action.nom = nom_module
                action._parametres_possibles = OrderedDict()
                action.init_types()
                action.convertir_types()
                lst_actions[nom_module] = action
                self.actions[nom_module] = action
            
    def charger_fonctions(self):
        """Chargement automatique des fonctions."""
        # Elles se trouvent dans le sous-répertoire fonctions
        chemin = self.chemin + os.sep + "fonctions"
        chemin_py = "primaires.scripting.fonctions"
        for nom_fichier in os.listdir(chemin):
            if not nom_fichier.startswith("_") and nom_fichier.endswith(".py"):
                nom_module = nom_fichier[:-3]
                chemin_py_mod = chemin_py + ".{}".format(nom_module)
                fonction = __import__(chemin_py_mod)
                fonction = getattr(getattr(getattr(getattr(fonction,
                        "scripting"), "fonctions"), nom_module),
                        "ClasseFonction")
                fonction.nom = nom_module
                fonction._parametres_possibles = {}
                fonction.init_types()
                fonction.convertir_types()
                self.fonctions[nom_module] = fonction
    
    def get_objet(self, identifiant):
        """Récupère l'objet depuis son identifiant.
        
        Sont successivement testées :
        -   les salles
        
        """
        return self.importeur.salle[identifiant]

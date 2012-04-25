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
from primaires.format.fonctions import format_nb, supprimer_accents
from .instruction import Instruction
from .condition import Condition
from .affectation import Affectation
from .commentaire import Commentaire
from .action import Action, actions as lst_actions
from . import parser
from . import commandes
from . import masques
from .quete.quete import Quete
from .quete.etape import Etape
from .test import Test
from .editeurs.qedit import EdtQedit
from .editeurs.cmdedit import EdtCmdedit
from .constantes.aide import *
from .script import scripts
from .alerte import Alerte
from .commande_dynamique import CommandeDynamique

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
        self.a_charger = []
        self.fonctions = {}
        self.actions = {}
        self.commandes = {}
        self.quetes = {}
        self.alertes = {}
        self.commandes_dynamiques = {}
        self.sujets_aides = {
            "syntaxe": syntaxe,
        }
    
    @property
    def commandes_dynamiques_sa(self):
        """Retourne les commandes dynamiques {cle_sans_accent: commande}."""
        cmds = {}
        for cmd in self.commandes_dynamiques.values():
            cmds[supprimer_accents(cmd.nom_francais)] = cmd
        
        return cmds
    
    def config(self):
        """Configuration du module."""
        self.a_charger.append(self)
        BaseModule.config(self)
    
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
        
        # Chargement des alertes
        alertes = self.importeur.supenr.charger_groupe(Alerte)
        for alerte in alertes:
            self.alertes[alerte.no] = alerte
        
        # Chargement des commandes dynamiques
        commandes_dynamiques = importeur.supenr.charger_groupe(
                CommandeDynamique)
        for cmd in commandes_dynamiques:
            self.commandes_dynamiques[cmd.nom_francais] = cmd
        
        if alertes:
            Alerte.no_actuel = max(a.no for a in alertes)
        
        # On lie la méthode informer_alertes avec l'hook joueur_connecte
        # La méthode informer_alertes sera ainsi appelée quand un joueur
        # se connecte
        self.importeur.hook["joueur:connecte"].ajouter_evenement(
                self.informer_alertes)
        
        BaseModule.init(self)
    
    def ajouter_commandes(self):
        """Ajout des commandes dans l'interpréteur"""
        self.commandes = [
            commandes.dyncom.CmdDyncom(),
            commandes.qedit.CmdQedit(),
            commandes.scripting.CmdScripting(),
        ]
        
        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)
        
        # Ajout des éditeurs 'qedit' et 'cmdedit'
        self.importeur.interpreteur.ajouter_editeur(EdtQedit)
        self.importeur.interpreteur.ajouter_editeur(EdtCmdedit)
    
    def preparer(self):
        """Préparation du module.
        
        * On initialise les scripts.
        * On ajoute les commandes dynamiques.
        
        """
        for script in scripts:
            script.init()
        
        for cmd in self.commandes_dynamiques.values():
            cmd.ajouter()
    
    def charger_actions(self):
        """Chargement automatique des actions.
        
        On parcourt tous les modules dans self.a_charger.
        
        """
        for module in self.a_charger:
            # Elles se trouvent dans le sous-répertoire actions
            chemin = module.chemin + os.sep + "actions"
            chemin_py = module.chemin_py + ".actions"
            for nom_fichier in os.listdir(chemin):
                if not nom_fichier.startswith("_") and \
                        nom_fichier.endswith(".py"):
                    nom_module = nom_fichier[:-3]
                    chemin_py_mod = chemin_py + ".{}".format(nom_module)
                    action = __import__(chemin_py_mod)
                    action = getattr(getattr(getattr(getattr(action,
                            module.nom), "actions"), nom_module),
                            "ClasseAction")
                    action.nom = nom_module
                    action._parametres_possibles = OrderedDict()
                    action.init_types()
                    action.convertir_types()
                    lst_actions[nom_module] = action
                    self.actions[nom_module] = action
            
    def charger_fonctions(self):
        """Chargement automatique des fonctions.
        
        On charge les modules dans self.a_charger.
        
        """
        for module in self.a_charger:
            # Elles se trouvent dans le sous-répertoire fonctions
            chemin = module.chemin + os.sep + "fonctions"
            chemin_py = module.chemin_py + ".fonctions"
            for nom_fichier in os.listdir(chemin):
                if not nom_fichier.startswith("_") and \
                        nom_fichier.endswith(".py"):
                    nom_module = nom_fichier[:-3]
                    chemin_py_mod = chemin_py + ".{}".format(nom_module)
                    fonction = __import__(chemin_py_mod)
                    fonction = getattr(getattr(getattr(getattr(fonction,
                            module.nom), "fonctions"), nom_module),
                            "ClasseFonction")
                    fonction.nom = nom_module
                    fonction._parametres_possibles = OrderedDict()
                    fonction.init_types()
                    fonction.convertir_types()
                    self.fonctions[nom_module] = fonction
    
    def informer_alertes(self, personnage):
        """Informe le personnage si des alertes non résolues sont à lire.
        
        Ce message n'est envoyé que si le personnage est immortel.
        
        """
        if personnage.est_immortel() and self.alertes:
            msg = format_nb(len(self.alertes),
                    "|rg|{nb} alerte{s} non lue{s}.|ff|", fem=True)
            personnage << msg
    
    def get_objet(self, identifiant):
        """Récupère l'objet depuis son identifiant.
        
        Sont successivement testées :
        -   les salles
        
        """
        return self.importeur.salle[identifiant]
    
    def get_commande_dynamique(self, nom):
        """Retourne la commande dynamique correspondante au nom.
        
        Le nom peut être avec ou sans accent.
        
        Si la commande dynamique n'est pas trouvée, lève une exception
        KeyError.
        
        """
        return self.commandes_dynamiques_sa[nom]
    
    def creer_commande_dynamique(self, nom_francais, nom_anglais):
        """Crée et ajoute une commande dynamique."""
        commande = CommandeDynamique(nom_francais, nom_anglais)
        commande.ajouter()
        self.commandes_dynamiques[nom_francais] = commande
        return commande


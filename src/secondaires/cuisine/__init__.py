# -*-coding:Utf-8 -*

# Copyright (c) 2010 NOEL-BARON Léo
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


"""Fichier contenant le module secondaire 'cuisine'."""

from math import ceil

from abstraits.module import *
from primaires.format.fonctions import format_nb
from secondaires.cuisine import commandes
from secondaires.cuisine import types
from .recette import Recette
from .editeurs.recedit import EdtRecedit

class Module(BaseModule):
    
    """Ce module gère la cuisine en jeu, et tout ce qui s'y rattache.
    
    """
    
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "cuisine", "secondaire")
        self.logger = type(self.importeur).man_logs.creer_logger( \
                "cuisine", "cuisine")
        self.recettes = {}
        self.commandes = []
    
    def init(self):
        """Initialisation du module"""
        # On récupère les recettes
        recettes = self.importeur.supenr.charger_groupe(Recette)
        for recette in recettes:
            self.recettes[recette.cle] = recette
        
        nb_recettes = len(self.recettes)
        self.logger.info(format_nb(nb_recettes,
                "{nb} recette{s} récupérée{s}", fem=True))
                
        ajouter_talent = self.importeur.perso.ajouter_talent
        ajouter_talent("cuisine", "cuisine", "survie", 0.20)
        
        BaseModule.init(self)
    
    def ajouter_commandes(self):
        """Ajout des commandes dans l'interpréteur"""
        self.commandes = [
            commandes.cuisiner.CmdCuisiner(),
            commandes.recettes.CmdRecettes(),
        ]
        
        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)
        
        # Ajout des éditeurs
        self.importeur.interpreteur.ajouter_editeur(EdtRecedit)
    
    def ajouter_recette(self, cle):
        """Ajoute la recette au module."""
        recette = Recette(cle)
        self.recettes[cle] = recette
        return recette
    
    def identifier_recette(self, ingredients):
        """Associe une liste d'ingrédients à une recette du module."""
        # On parcourt les ingrédients de chaque recette
        for recette in self.recettes.values():
            proportions = []
            for ing, qtt in recette.ingredients.items():
                if ing in ingredients:
                    proportions.append(ingredients.count(ing) / qtt)
                # Si l'ingrédient n'existe pas, mauvaise recette
                else:
                    recette = False
            for ing in ingredients:
                if recette and ing not in recette.ingredients:
                    recette = False
            # Si la recette est vérifiée, cuisinable et proportionnée
            if recette and recette.cuisinable:
                diff = round((100 - recette.difficulte) / 100, 2)
                if not [p for p in proportions \
                        if abs(p - sum(proportions) / len(proportions)) >  diff]:
                    return recette, ceil(sum(proportions) / len(proportions))
        return None, 0

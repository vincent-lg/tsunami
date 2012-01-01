# -*-coding:Utf-8 -*

# Copyright (c) 2010 DAVY Guillaume
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


"""Fichier contenant la classe Sort, détaillée plus bas."""

from math import ceil
from random import random

from abstraits.obase import *
from primaires.format.description import Description
from .script import ScriptSort

STANDARD = 0
OFFENSIF = 1

class Sort(BaseObj):
    
    """Classe représentant un sortilège.
    
    """
    
    def __init__(self, cle, parent=None):
        """Constructeur du sort"""
        BaseObj.__init__(self)
        self.parent = parent
        self.cle = cle
        self.nom = "sortilège"
        self.description = Description(parent=self)
        self.type = "destruction"
        self._type_cible = "aucune"
        self.difficulte = 0
        self.distance = False
        self.script = ScriptSort(self)
        # On passe le statut en CONSTRUIT
        self._statut = CONSTRUIT
    
    def __getnewargs__(self):
        return ("", )
    
    def __str__(self):
        return "sort:" + self.cle
    
    def __setattr__(self, nom_attr, valeur):
        """Enregisre le parent si il est précisé"""
        construit = self.construit
        BaseObj.__setattr__(self, nom_attr, valeur)
        if construit and self.parent:
            self.parent.enregistrer()
    
    def _get_type_cible(self):
        """Retourne le type de cible."""
        return self._type_cible
    def _set_type_cible(self, nouveau_type):
        """Change le type de cible et la variable cible du script."""
        self._type_cible = nouveau_type
        if nouveau_type == "aucune":
            for evt in self.script.evenements.values():
                self.script = ScriptSort(self)
        elif nouveau_type == "personnage":
            for evt in self.script.evenements.values():
                self.script = ScriptSort(self)
                var_cible = evt.ajouter_variable("cible", "Personnage")
                var_cible.aide = "le personnage ciblé par le sort"
        elif nouveau_type == "objet":
            for evt in self.script.evenements.values():
                self.script = ScriptSort(self)
                var_cible = evt.ajouter_variable("cible", "Objet")
                var_cible.aide = "l'objet ciblé par le sort"
        elif nouveau_type == "salle":
            for evt in self.script.evenements.values():
                self.script = ScriptSort(self)
                var_cible = evt.ajouter_variable("cible", "Salle")
                var_cible.aide = "la salle ciblée par le sort"
    type_cible = property(_get_type_cible, _set_type_cible)
    
    def enregistrer(self):
        """Enregistre le sort dans son parent"""
        construit = self.construit
        if construit and self.parent:
            self.parent.enregistrer()
    
    def echoue(self, personnage):
        """Détermine si personnage réussit ou non à lancer ce sort."""
        maitrise = (100 - personnage.sorts.get(self.cle, 0)) / 100
        difficulte = sort.difficulte / 100
        if random() < difficulte * maitrise:
            return True
        return False
    
    def concentrer(self, personnage, cible, apprendre=True):
        """Fait concentrer le sort à 'personnage'."""
        maitrise = 0
        if apprendre:
            maitrise = personnage.pratiquer_sort(self.cle)
            personnage.pratiquer_talent(self.type)
        else:
            maitrise = personnage.sorts.get(self.cle, 0)
        self.script["concentration"].executer(personnage=personnage,
                maitrise=maitrise, cible=cible)
        action = self.lancer
        if self.echoue(personnage) and apprendre:
            action = self.echouer
        nom_act = "sort_" + self.cle + "_" + personnage.nom
        duree = ceil(3 * (100 - maitrise) / 100)
        type(self).importeur.diffact.ajouter_action(nom_act, duree,
                action, personnage, cible)
    
    def echouer(self, personnage, cible):
        """Fait rater le sort à personnage."""
        personnage.cle_etat = ""
        maitrise = personnage.sorts.get(self.cle, 0)
        self.script["echec"].executer(personnage=personnage, maitrise=maitrise,
                cible=cible)
    
    def lancer(self, personnage, cible):
        """Fait lancer le sort à personnage."""
        maitrise = personnage.sorts.get(self.cle, 0)
        self.script["lancement"].executer(personnage=personnage,
                maitrise=maitrise, cible=cible)
        self.toucher(personnage, cible)
    
    def toucher(self, personnage, cible):
        """Active les effets du sort."""
        personnage.cle_etat = ""
        maitrise = personnage.sorts.get(self.cle, 0)
        self.script["effet"].executer(personnage=personnage,
                maitrise=maitrise, cible=cible)

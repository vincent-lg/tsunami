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
        self.type = STANDARD
        self.type_cible = "aucune"
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
    
    def enregistrer(self):
        """Enregistre le sort dans son parent"""
        construit = self.construit
        if construit and self.parent:
            self.parent.enregistrer()
    
    @property
    def str_type(self):
        """Retourne le type de sort"""
        if self.type == STANDARD:
            return "standard"
        else:
            return "offensif"
    
    def concentrer(self, personnage, cible=None):
        """Fait concentrer le sort à 'personnage'."""
        personnage << "Vous vous concentrez intensément."
        maitrise = personnage.pratiquer_sort(self.cle)
        self.script["concentration"].executer(personnage=personnage,
                maitrise=maitrise)
        nom_act = "sort_" + self.cle + "_" + personnage.nom
        duree = ceil(3 * (100 - maitrise) / 100)
        type(self).importeur.diffact.ajouter_action(nom_act, duree,
                self.lancer, personnage, cible=cible)
    
    def lancer(self, personnage, cible=None):
        """Fait lancer le sort à 'personnage'."""
        personnage << "Vous lancez le sort {}.".format(self.nom)

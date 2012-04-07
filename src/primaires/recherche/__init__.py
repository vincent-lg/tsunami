# -*-coding:Utf-8 -*

# Copyright (c) 2012 NOEL-BARON Léo
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


"""Fichier contenant le module primaire recherche."""

from abstraits.module import *
from primaires.recherche import commandes
from primaires.recherche import masques
from primaires.recherche import cherchables

class Module(BaseModule):
    
    """Classe représentant le module primaire 'recherche'.
    
    Ce module constitue le moteur de recherche de la plateforme. On peut
    y implémenter divers outils dont la finalité est de permettre aux
    administrateurs de mieux manipuler l'univers qu'ils créent.
    
    """
    
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "recherche", "primaire")
        self.logger = type(self.importeur).man_logs.creer_logger( \
                "recherche", "recherche")
        self.masques = []
        self.commandes = []
        self._cherchables = cherchables
    
    def init(self):
        """Initialisation du module"""
        BaseModule.init(self)
    
    def ajouter_commandes(self):
        """Ajout des commandes"""
        self.commandes = [
            commandes.trouver.CmdTrouver(),
        ]
        
        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)
        
        # Ajout des éditeurs
        # self.importeur.interpreteur.ajouter_editeur(EdtChedit)
    
    @property
    def cherchables(self):
        """Retourne les cherchables existants"""
        return list(self._cherchables)

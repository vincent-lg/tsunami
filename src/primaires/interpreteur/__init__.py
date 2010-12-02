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


"""Fichier contenant le module primaire interpreteur."""

from abstraits.module import *
from primaires.interpreteur.contexte import Contexte
from primaires.interpreteur.masque.noeuds.fonctions import creer_noeud
from primaires.interpreteur.masque.noeuds.embranchement import Embranchement
from primaires.interpreteur.masque.noeuds.base_noeud import BaseNoeud

class Module(BaseModule):
    """Cette classe est la classe gérant tous les interpréteurs.
    Elle recense les différents contextes, en crée certains et permet
    à chaque module de créer ses propres contextes, commandes, éditeurs...
    
    """
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "interpreteur", "primaire")
        Contexte.importeur = importeur
        BaseNoeud.importeur = importeur
        self.contextes = {} # Dictionnaire des contextes
        self.commandes = Embranchement()
        self.masques = {}
    
    def ajouter_contexte(self, nouv_contexte):
        """Ajoute le contexte dans le dictionnaire self.contextes.
        On se sert du nom comme identifiant du contexte.
        
        """
        self.contextes[nouv_contexte.nom] = nouv_contexte
    
    def ajouter_commande(self, schema):
        """Ajoute une commande à l'embranchement"""
        creer_noeud(self.commandes, schema)
        print(self.commandes)
    
    def ajouter_masque(self, masque):
        """Méthode d'ajout d'un masque"""
        self.masques[masque.nom] = masque
    
    def get_masque(self, nom_masque):
        """Retourne le masque portant le nom correspondant"""
        return self.masques[nom_masque]

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


"""Ce fichier contient la classe NoeudCommande, détaillée plus bas."""

from primaires.interpreteur.masque.noeuds.base_noeud import BaseNoeud
from primaires.interpreteur.masque.noeuds.embranchement import Embranchement
from primaires.interpreteur.masque.fonctions import *

class NoeudCommande(BaseNoeud):
    
    """Noeud encapsulant une commande.
    
    """
    
    def __init__(self, commande):
        """Constructeur du noeud et de la commande"""
        BaseNoeud.__init__(self)
        self.commande = commande
        self.nom = commande.nom_francais
        if self.commande.schema:
            schema = self.commande.schema
            self.construire_arborescence(schema)
    
    def construire_arborescence(self, schema):
        """Redirection vers la construction de la commande"""
        self.suivant = self.commande.construire_arborescence(schema)
    
    def __str__(self):
        """Fonction d'affichage"""
        res = str(self.commande)
        if self.suivant:
            res += " : " + str(self.suivant)
        
        return res
    
    @property
    def fils(self):
        """Retourne les fils, c'est-à-dire :
        -   le noeud éventuel du schéma de la commande
        -   les différents paramètres de la commande
        
        """
        fils = Embranchement()
        if self.suivant:
            fils.ajouter_fils(self.suivant)
        for noeud_param in self.commande.parametres.values():
            fils.ajouter_fils(noeud_param)
        
        return fils
    
    def valider(self, personnage, dic_masques, commande, tester_fils=True):
        """Validation d'un noeud commande.
        La commande est sous la forme d'une liste de caractères.
        
        """
        valide = self.commande.valider(personnage, dic_masques, commande)
        if valide:
            dic_masques[self.commande.nom] = self.commande
            if commande:
                valide = self.fils.valider(personnage, dic_masques, \
                        commande)
        
        return valide
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation"""
        self.commande.interpreter(personnage, dic_masques)
        for fils in self.fils:
            fils.interpreter(personnage, dic_masques)

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


"""Fichier définissant la classe NoeudOptionnel détaillée plus bas;"""

from primaires.interpreteur.masque.noeuds.base_noeud import BaseNoeud

class NoeudOptionnel(BaseNoeud):
    
    """Cette classe contient un noeud optionnel.
    Le noeud masque considéré comme "optionnel" est contenu dans l'attribut
    'interne'.
    
    """
    
    def __init__(self, interne, suivant):
        """Constructeur du noeud optionnel"""
        BaseNoeud.__init__(self)
        self.interne = interne
        self.suivant = suivant
    
    def _get_reste(self):
        """Retourne le reste.
        On le demande récursivement au noeud optionnel jusqu'à tomber sur un
        noeud masque.
        
        """
        if self.optionnel:
            reste = self.optionnel.reste
        else:
            reste = ""
        
        return reste
    
    reste = property(_get_reste)
    
    def __str__(self):
        """Méthode d'affichage"""
        msg = "opt("
        if self.interne:
            msg += str(self.interne)
        
        msg += ")"
        if self.suivant:
            msg += " : " + str(self.suivant)
        
        return msg
    
    def valider(self, personnage, dic_masques, commande, tester_fils=True):
        """Valide un noeud optionnel.
        Un noeud optionnel se valide automatiquement et passe le relais à ses
        fils.
        
        """
        self.interne.valider(personnage, dic_masques, commande)
        if self.suivant and tester_fils:
            valide = self.suivant.valider(personnage, dic_masques, commande)
        else:
            valide = True
        
        return valide


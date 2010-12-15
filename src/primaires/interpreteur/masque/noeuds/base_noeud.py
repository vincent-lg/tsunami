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


"""Fichier définissant la classe BaseNoeud détaillée plus bas;"""

class BaseNoeud:
    
    """Classe représentant la base d'un noeud.
    Cette classe est héritée par tous les autres types de noeuds.
    
    """
    
    importeur = None
    
    def __init__(self):
        """Constructeur du noeud de base"""
        self.nom = ""
        self.suivant = None
    
    def valider(self, personnage, dic_masques, commande, tester_fils=True):
        """Validation du noeud.
        Cette méthode est à redéfinir dans chacune des classes-filles créée.
        Chaque type de noeud a sa propre méthode de validation.
        Dans tous les cas, une booléen doit être retourné :
        -   True si le noeud a pu être interprété
        -   False sinon
        
        Note : pour la plupart des noeuds, la validation est aussi fonction
            des fils.
        
        """
        raise NotImplementedError
    
    def _get_fils(self):
        """Retourne les fils du noeud sous la forme d'une liste"""
        return [self.suivant]
    
    fils = property(_get_fils)

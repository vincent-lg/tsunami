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


"""Fichier définissant la classe NoeudMasque, détaillée plus bas."""

from collections import OrderedDict

class NoeudMasque:
    
    """Classe définissant un noeud de masque.
    Ce noeud permet de constituer une arborescence. A la différence d'un arbre
    "classique", un noeud de masque est constitué :
    -   d'un masque pouvant être à None si la liste des masques est non vide
    -   d'une liste de masques à valider pour valider ce noeud (les
        éléments de la liste sont elles-mêmes des noeuds)
    -   d'une liste des noeuds-fils (également des noeuds). Si le noeud
        courant se valide, on va tester la validation de tous ses noeuds fils
        jusqu'à trouver le bon.
        Si cette liste de fils est vide, le noeud courant est une feuille.
    
    Le schéma de validation d'un noeud est le suivant :
    1)  Si le masque du noeud existe (is not None), on tente de le valider
        grâce à l'entrée de l'utilisateur (une bribe de commande)
    2)  Si le masque est vide (is None), on applique récursivement la
        validation à chacun des noeuds de la liste de validation
    3)  Si l'étape 1 ou 2 a pu être validée (en fonction du masque du noeud),
        le noeud se valide. Le bribe de la commande reçue est tronquée pour
        exclure la partie interprétée par le noeud et on passe le tests aux
        noeuds fils que l'on tente de valider
    
    Enfin, un noeud peut être obligatoire ou facultatif. Un noeud facultatif
    est automatiquement validé ; même si la bribe de la colmmande qui lui ai
    passé ne correspond pas à ses attentes. Dans ce dernier cas, il applique à
    ses masques leur valeur par défaut (si elle existe), ou None sinon.
    
    Pour plus d'information, consultez la syntaxe d'un masque.
    
    """
    
    def __init__(self, masque=None, obligatoire=True):
        """Construction d'un noeud.
        Un noeud est constitué de trois informations (voir plus haut) :
        -   un masque
        -   une liste de noeuds à valider (peut être vide)
        -   une liste de noeuds fils
        -   un statut (oblligatoire par défaut ou facultatif)
        
        """
        self.masque = masque
        self.noeuds_a_valider = []
        self.noeuds_fils = []
        self.obligatoire = obligatoire
    
    def ajouter_noeud_a_valider(self, noeud):
        """Ajoute un noeud à valider dans la liste."""
        self.noeuds_a_valider.append(noeud)
    
    def ajouter_noeud_fils(self, noeud):
        """Ajoute un noeud fils au noeud courant"""
        self.noeuds_fils.append(noeud)

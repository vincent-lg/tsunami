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


"""Fichier définissant la classe Embranchement, détaillée plus bas."""

from primaires.interpreteur.masque.noeuds.base_noeud import BaseNoeud
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation

class Embranchement(BaseNoeud):
    """Un noeud embranchement, constitué non pas d'un seul suivant mais de
    plusieurs, sous la forme d'une liste extensible.
    
    """
    
    def __init__(self):
        """Constructeur de l'embranchement"""
        BaseNoeud.__init__(self)
        self.schema = None
        self.suivant = []
    
    def _get_fils(self):
        """Retourne les noeuds fils, c'est-à-dire suivant qui est à passer sous
        la forme d'un tuple.
        
        """
        return tuple(self.suivant)
    fils = property(_get_fils)
    
    def __iter__(self):
        """Méthode intégrant un itérateur sur l'embranchement"""
        return iter(self.suivant)
    
    def ajouter_fils(self, noeud_fils):
        """Ajoute un fils à l'embranchement"""
        self.suivant.append(noeud_fils)
    
    def __str__(self):
        """Méthode d'affichage"""
        msg = "emb("
        msg += ", ".join( \
            [str(noeud) for noeud in self.suivant])
        msg += ")"
        return msg
    
    def repartir(self, personnage, masques, commande):
        """Répartition de la commande.
        
        On teste chaque embranchement en s'arrêtant dès qu'un embranchement
        répartit.
        
        """
        liste_fils = self.fils
        # Tri la liste des fils par ordre alphabétique français ou anglais
        if personnage.langue_cmd == "francais":
            liste_fils = sorted(liste_fils, \
                key=lambda noeud: noeud.commande.nom_francais)
        elif personnage.langue_cmd == "anglais":
            liste_fils = sorted(liste_fils, \
                key=lambda noeud: noeud.commande.nom_anglais)
        
        valide = True
        for fils in liste_fils:
            valide = fils.repartir(personnage, masques, commande)
            if valide:
                break
        
        if not valide and not self.schema:
            raise ErreurValidation
        elif self.schema:
            valide = self.schema.repartir(personnage, masques, commande)
            if not valide:
                raise ErreurValidation
        
        return valide
    
    def valider(self, personnage, dic_masques, commande, tester_fils=True):
        """Validation du noeud Embranchement.
        La commande entrée par le personnage peut avoir été déjà réduite par
        les noeuds précédents. Elle est sous la forme d'une liste de
        caractères.
        
        """
        liste_fils = self.fils
        # Tri la liste des fils par ordre alphabétique français ou anglais
        if personnage.langue_cmd == "francais":
            liste_fils = sorted(liste_fils, \
                key=lambda noeud: noeud.commande.nom_francais)
        elif personnage.langue_cmd == "anglais":
            liste_fils = sorted(liste_fils, \
                key=lambda noeud: noeud.commande.nom_anglais)
        
        valide = True
        for fils in liste_fils:
            valide = fils.valider(personnage, dic_masques, tester_fils)
            if valide:
                break
        
        if not valide and not self.schema:
            raise ErreurValidation
        elif self.schema:
            valide = self.schema.valider(personnage, dic_masques, tester_fils)
            if not valide:
                raise ErreurValidation
        
        return valide
    
    def interpreter(self, personnage, dic_masques):
        """Redirection vers la méthode interpreter des fils."""
        for fils in self.fils:
            fils.interpreter(personnage, dic_masques)

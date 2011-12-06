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


"""Fichier contenant la classe BaseElement, détaillée plus bas."""

from abstraits.id import ObjetID
from bases.collections.liste_id import ListeID
from corps.fonctions import valider_cle
from primaires.format.description import Description
from . import MetaElt

class BaseElement(ObjetID, metaclass=MetaElt):
    
    """Classe abstraite représentant le type de base d'un élément.
    
    Si des données doivent être communes à tous les types d'éléments
    c'est dans cette classe qu'elles apparaissent.
    
    """
    
    groupe = "elements"
    sous_rep = "navires/elements"
    nom_type = "" # à redéfinir
    
    def __init__(self, cle=""):
        """Constructeur d'un type"""
        if cle:
            valider_cle(cle)
        
        ObjetID.__init__(self)
        self.cle = cle
    
        self._attributs = {}
        self.nom = "un élément inconnu"
        
        # Editeur
        self._extensions_editeur = []
    
    def __getnewargs__(self):
        return ()
    
    def __str__(self):
        return self.cle
    
    def __getstate__(self):
        """Retourne le dictionnaire à enregistrer."""
        attrs = dict(ObjetID.__getstate__(self))
        del attrs["_extensions_editeur"]
        del attrs["_attributs"]
        return attrs
    
    def etendre_editeur(self, raccourci, ligne, editeur, objet, attribut, *sup):
        """Permet d'étendre l'éditeur d'éléments en fonction du type.
        
        Paramètres à entrer :
        -   raccourci   le raccourci permettant d'accéder à la ligne
        -   ligne       la ligne de l'éditeur (exemple 'Description')
        -   editeur     le contexte-éditeur (exemple Uniligne)
        -   objet       l'objet à éditer
        -   attribut    l'attribut à éditer    
        
        Cette méthode est appelée lors de la création de l'éditeur
        d'éléments.
        
        """
        self._extensions_editeur.append(
            (raccourci, ligne, editeur, objet, attribut, sup))
    
    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes.
        
        On récupère un dictionnaire représentant la présentation avec en
        clé les raccourcis et en valeur les enveloppes.
        
        Cela peut permettre de travailler sur les enveloppes ajoutées par
        'etendre_editeur'.
        
        """
        pass
    
    @staticmethod
    def get_description_ligne(elt, personnage):
        """Retourne une description d'une ligne de l'élément."""
        return elt.nom.capitalize() + " est là"
    
    @staticmethod
    def get_nom_pour(elt, personnage):
        """Retourne le nom de l'élément."""
        return elt.nom


ObjetID.ajouter_groupe(BaseElement)

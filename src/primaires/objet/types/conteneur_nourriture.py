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


"""Fichier contenant le type ConteneurNourriture."""

from primaires.interpreteur.editeur.choix import Choix
from corps.fonctions import lisser
from .base import BaseType
from .conteneur import Conteneur

# Constante
LISTE_SUFFIXES = [""]

class ConteneurNourriture(Conteneur):
    
    """Type d'objet: conteneur de nourriture.
    
    Les conteneurs de nourriture sont des conteneurs spéciaux genre assiette.
    
    """
    
    nom_type = "conteneur de nourriture"
    
    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        Conteneur.__init__(self, cle)
        self.types_admis = ["nourriture"]
        self.suffixe = "de"
        self.reduire_editeur("t")
        self.etendre_editeur("s", "suffixe", Choix, self,
                "suffixe", LISTE_SUFFIXES)
    
    @property
    def suffixes(self):
        """Retourne la liste des suffixes possibles."""
        return ", ".join(LISTE_SUFFIXES)
            
    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes"""
        suffixe = enveloppes["s"]
        suffixe.apercu = "{objet.suffixe}"
        suffixe.aide_courte = \
            "Choisissez un |ent|types admis|ff| ou entrez |cmd|/|ff| pour revenir à la " \
            "fenêtre parente.\nLe suffixe sera utilisé pour afficher le contenu de cet objet, par exemple :\n" \
            "|grf|une assiette|ff| |bc|pleine de|ff| |grf|ragoût|ff|.\n\n" \
            "Choix possibles : {objet.suffixes}\n\n" \
            "Suffixe actuel : {objet.suffixe}"
    
    # Actions sur les objets
    def get_nom(self, nombre=1):
        """Retourne le nom complet en fonction du nombre.
        
        Par exemple :
        Si nombre == 1 : retourne le nom singulier
        Sinon : retourne le nombre et le nom pluriel
        
        """
        print("get_nom", type(self))
        ajout = ""
        if hasattr(self, "conteneur"):
            for contenu in self.conteneur:
                nom = contenu.get_nom()
                nom = nom[3:] if nom.startswith("un ") else nom[4:]
                ajout = lisser(" " + self.suffixe + " " + nom)
        if nombre <= 0:
            raise ValueError("la fonction get_nom a été appelée " \
                    "avec un nombre négatif ou nul.")
        elif nombre == 1:
            return self.nom_singulier + ajout
        else:
            if self.noms_sup:
                noms_sup = list(self.noms_sup)
                noms_sup.reverse()
                for nom in noms_sup:
                    if nombre >= nom[0]:
                        return nom[1]
            return str(nombre) + " " + self.nom_pluriel + ajout
    
    def regarder(self, personnage):
        """Le personnage regarde l'objet"""
        msg = BaseType.regarder(self, personnage)
        contenu = None
        for o in self.conteneur:
            contenu = o
        
        if contenu:
            msg += "\nCe plat contient " + contenu.get_nom() + " :\n"
            msg += str(contenu.description)
        
        return msg

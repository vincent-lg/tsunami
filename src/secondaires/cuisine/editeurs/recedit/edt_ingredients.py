# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 NOEL-BARON Léo
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


"""Fichier contenant le contexte éditeur EdtIngredients"""

from primaires.interpreteur.editeur import Editeur

class EdtIngredients(Editeur):
    
    """Classe définissant le contexte éditeur 'ingrédients'.
    Ce contexte permet d'ajouter ou de supprimer des ingrédients d'une recette.
    
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.ajouter_option("d", self.suppr_ingredient)
    
    def accueil(self):
        """Message d'accueil du contexte"""
        recette = self.objet
        msg = "| |tit|" + "Ingrédients de {}".format(recette).ljust(76)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += self.aide_courte
        msg += "Ingrédients actuels :\n"
        
        # Parcours des ingredients
        ingredients = recette.ingredients
        ret = ""
        for ing, qtt in ingredients.items():
            ret += "\n  {} ({})".format(ing.get_nom(qtt), ing.cle)
        if not ingredients:
            ret += "\n  |att|Aucun ingrédient pour l'instant.|ff|"
        msg += ret
        
        return msg
    
    def suppr_ingredient(self, arguments):
        """Supprime un ingrédient ; syntaxe : /d <ingredient>."""
        recette = self.objet
        nom_ing = arguments.split(" ")[0]
        try:
            ingredient = importeur.objet.prototypes[nom_ing]
            assert ingredient in recette.ingredients
        except (KeyError, AssertionError):
            self.pere << "|err|Cet ingrédient n'existe pas.|ff|"
        else:
            del recette.ingredients[ingredient]
            self.actualiser()
    
    def interpreter(self, msg):
        """Interprétation du message"""
        recette = self.objet
        try:
            qtt, nom_ing = msg.split(" ")
            qtt = int(qtt)
            assert qtt > 0
        except (ValueError, AssertionError):
            self.pere << "|err|Précisez un ingrédient et une quantité.|ff|"
        else:
            try:
                ingredient = importeur.objet.prototypes[nom_ing]
            except KeyError:
                self.pere << "|err|Cet ingrédient est introuvable.|ff|"
            else:
                recette.ingredients[ingredient] = qtt
                self.actualiser()

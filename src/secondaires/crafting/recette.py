# -*-coding:Utf-8 -*

# Copyright (c) 2015 LE GOFF Vincent
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


"""Fichier contenant la classe Recette, détaillée plus bas."""

from abstraits.obase import BaseObj

class Recette(BaseObj):

    """Classe représentant une recette artisanale.

    Une recette est une combinaison d'objets ou de types utilisés
    pour former un résultat. Par exemple, de la fourrure en assez
    grande quantité et des bandes de cuir peuvent former un sac.
    La sélection de la bonne recette se fait en fonction des objets
    ou types. Une recette peut par exemple demander qu'on utilise
    de la fourrure (ce qui est un type d'objet), n'importe quelle
    fourrure peut faire l'affaire, ou bien de la fourrure de lapin
    précisément.

    En terme d'attribut d'objet, on utilise deux dictionnaires,
    un pour les objets précis, l'autre pour les types.

    """

    def __init__(self, rang):
        """Constructeur de la fiche."""
        BaseObj.__init__(self)
        self.rang = rang
        self.ingredients_objets = {}
        self.ingredients_types = {}
        self.resultat = ""
        self._construire()

    def __getnewargs__(self):
        return (None, )

    def __repr__(self):
        return "<Recette pour {}>".format(self.resultat)

    def __str__(self):
        return "recette pour {}".format(repr(self.cle))

    def ajouter_type(self, nom_type, quantite=1):
        """Ajoute un type d'ingrédient."""
        if nom_type not in self.ingredients_types:
            self.ingredients_types[nom_type] = 0
        self.ingredients_types[nom_type] += quantite

    def ajouter_objet(self, cle, quantite=1):
        """Ajoute une clé de prototype d'ingrédient."""
        if cle not in self.ingredients_objets:
            self.ingredients_objets[cle] = 0
        self.ingredients_objets[cle] += quantite

    def retirer_type(self, nom_type, quantite=1):
        """Retire le type de la liste des ingrédients."""
        if nom_type not in self.ingredients_types:
            raise ValueError("le type {} n'est pas dans la liste " \
                    "d'ingrédients".format(repr(nom_type)))

        self.ingredients_types[nom_type] -= quantite
        if self.ingredients_types[nom_type] <= 0:
            del self.ingredients_types[nom_type]

    def retirer_objet(self, cle, quantite=1):
        """Retire la clé de prototype de la liste des ingrédients."""
        if cle not in self.ingredients_objets:
            raise ValueError("l'objet {} n'est pas dans la liste " \
                    "d'ingrédients".format(repr(cle)))

        self.ingredients_objets[cle] -= quantite
        if self.ingredients_objets[cle] <= 0:
            del self.ingredients_objets[cle]

    def peut_faire(self, ingredients):
        """Vérifie si la liste des ingrédients fait la recette.

        Pour chaque ingrédient, on vérifie son type et sa clé.
        L'un d'eux doit se trouver dans les besoins de la recette.
        Notez que si il y a trop d'ingrédients, cette recette
        n'est pas sélectionnée.

        """
        types = self.ingredients_objets.copy()
        objets = self.ingredients_types.copy()

        for ingredient in list(ingredients):
            cle = ingredient.cle
            nom_type = ingredient.nom_type

            if cle in objets:
                objets[cle] -= 1
                if objets[cle] <= 0:
                    del objets[cle]
            elif nom_type in types:
                types[nom_type] -= 1
                if types[nom_type] <= 0:
                    del types[nom_type]
            else:
                return False

            ingredients.remove(ingredient)

        if types == {} and objets == {} and ingredients == []:
            # L'attente a été remplie
            return True

        return False

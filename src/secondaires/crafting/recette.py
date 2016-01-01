# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 LE GOFF Vincent
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
from primaires.format.fonctions import supprimer_accents
from primaires.scripting.script import Script

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

    nom_scripting = "la recette"

    def __init__(self, rang):
        """Constructeur de la fiche."""
        BaseObj.__init__(self)
        self.rang = rang
        self.nom = ""
        self.nb_max = 1
        self.ingredients_objets = {}
        self.ingredients_types = {}
        self.resultat = ""
        self.script = ScriptRecette(self)
        self._construire()

    def __getnewargs__(self):
        return (None, )

    def __repr__(self):
        return "<Recette pour {}>".format(self.resultat)

    def __str__(self):
        return "recette pour {}".format(repr(self.resultat))

    @property
    def description(self):
        msg = ""
        if self.nom:
            msg = self.nom + " pour "

        msg += self.resultat + "("
        premier = True

        # Affichage des types
        for cle, (qtt_min, qtt_max) in self.ingredients_types.items():
            qtt = qtt_min if qtt_min == qtt_max else "{}-{}".format(
                    qtt_min, qtt_max)
            if premier:
                premier = False
            else:
                msg += ", "

            msg += "type {} X {}".format(cle, qtt)

        # Affichage des objets
        for cle, (qtt_min, qtt_max) in self.ingredients_objets.items():
            qtt = qtt_min if qtt_min == qtt_max else "{}-{}".format(
                    qtt_min, qtt_max)
            if premier:
                premier = False
            else:
                msg += ", "

            msg += "objet {} X {}".format(cle, qtt)

        msg += ")"
        return msg

    def peut_faire(self, personnage, ingredients):
        """Vérifie si la liste des ingrédients fait la recette.

        Pour chaque ingrédient, on vérifie son type et sa clé.
        L'un d'eux doit se trouver dans les besoins de la recette.
        Notez que si il y a trop d'ingrédients, cette recette
        n'est pas sélectionnée.

        """
        ingredients = list(ingredients)
        evt = self.script["valide"]
        if evt.nb_lignes > 0:
            evt.executer(personnage=personnage, ingredients=ingredients)
            try:
                valide = evt.espaces.variables["valide"]
            except KeyError:
                raise ValueError("la variable 'valide' n'est apparemment " \
                        "pas définie")

            return bool(valide)

        types = self.ingredients_types.copy()
        types_min = dict((t, q) for t, (q, x) in types.items())
        types_max = dict((t, x - q) for t, (q, x) in types.items() if \
                x - q > 0)
        objets = self.ingredients_objets.copy()
        objets_min = dict((o, q) for o, (q, x) in objets.items())
        objets_max = dict((o, x - q) for o, (q, x) in objets.items() if \
                x - q > 0)

        for ingredient in list(ingredients):
            cle = ingredient.cle
            nom_type = ingredient.nom_type

            if cle in objets_min:
                objets_min[cle] -= 1
                if objets_min[cle] <= 0:
                    del objets_min[cle]
            elif cle in objets_max:
                objets_max[cle] -= 1
                if objets_max[cle] <= 0:
                    del objets_max[cle]
            elif nom_type in types_min:
                types_min[nom_type] -= 1
                if types_min[nom_type] <= 0:
                    del types_min[nom_type]
            elif nom_type in types_max:
                types_max[nom_type] -= 1
                if types_max[nom_type] <= 0:
                    del types_max[nom_type]
            else:
                return False

            ingredients.remove(ingredient)

        if types_min == {} and objets_min == {} and ingredients == []:
            # L'attente a été remplie
            return True

        return False

    def creer_resultat(self, personnage, ingredients):
        """Créé la recette et retourne l'objet créé."""
        if not self.peut_faire(personnage, ingredients):
            raise ValueError("Les ingrédients {} ne peuvent pas être " \
                    "utilisés pour cette recette {}".format(
                    ingredients, repr(self.resultat)))

        prototype = importeur.objet.prototypes[self.resultat]
        objet = importeur.objet.creer_objet(prototype)

        # Transfert des attributs
        attributs = {}
        for ingredient in ingredients:
            prototype = ingredient.prototype
            attrs = importeur.crafting.configuration[prototype].attributs
            if attrs:
                attributs.update(attrs)

            attrs = importeur.crafting.configuration[ingredient].attributs
            if attrs:
                attributs.update(attrs)

        sa_attributs = {}
        for cle, valeur in attributs.items():
            sa_attributs[supprimer_accents(cle).lower()] = valeur

        importeur.crafting.configuration[objet].attributs = sa_attributs

        personnage.salle.objets_sol.ajouter(objet)
        self.script["fabrique"].executer(personnage=personnage,
                objet=objet, ingredients=ingredients)

        for ingredient in ingredients:
            importeur.objet.supprimer_objet(ingredient.identifiant)

        return objet

class ScriptRecette(Script):

    """Script et évènements propres aux recettes."""

    def init(self):
        """Initialisation du script"""
        # Événement fabrique
        evt_fabrique = self.creer_evenement("fabrique")
        evt_fabrique.aide_courte = "la recette est fabriquée"
        evt_fabrique.aide_longue = \
            "Cet évènement est appelé quand un personnage fabrique " \
            "la recette. Elle est appelée après la fabrication de " \
            "la recette et permet de personnaliser l'objet créé " \
            "depuis les ingrédients (variable 'objet'). Les " \
            "ingrédients sont aussi disponibles dans la variable " \
            "'ingredients'."

        # Configuration des variables de l'évènement fabrique
        var_perso = evt_fabrique.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage fabriquant la recette"
        var_objet = evt_fabrique.ajouter_variable("objet", "Objet")
        var_objet.aide = "l'objet créé par la recette"
        var_ingredients = evt_fabrique.ajouter_variable("ingredients", "list")
        var_ingredients.aide = "la liste des ingrédients (liste d'objets)"

        # Événement valide
        evt_valide = self.creer_evenement("valide")
        evt_valide.aide_courte = "la recette est-elle valide ?"
        evt_valide.aide_longue = \
            "Cet évènement permet de configurer de façon plus précise " \
            "le fait qu'une recette est valide ou non. Elle permet " \
            "d'outre-passer les ingrédients précisés dans la recette, " \
            "pour utiliser des critères plus spécifiques, par exemple, " \
            "ou bien chercher d'autres ingrédients ailleurs. Un exemple " \
            "concret pourrait être de limiter le nombre d'ingrédients " \
            "en fonction de leur poids et pas de leur quantité. Si " \
            "cet évènement ne contient aucune instruction, les objets " \
            "et types définis dans la recette sont utilisés pour " \
            "savoir si elle est valide. Sinon, cet évènement est " \
            "appelé. La variable 'valide' doit être créée : elle " \
            "doit avoir une valeur de |ent|1|ff| pour indiquer que " \
            "la recette a bien été validée, |ent|0|ff| sinon."

        # Configuration des variables de l'évènement valide
        var_perso = evt_valide.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage fabriquant la recette"
        var_ingredients = evt_valide.ajouter_variable("ingredients", "list")
        var_ingredients.aide = "la liste des ingrédients (liste d'objets)"

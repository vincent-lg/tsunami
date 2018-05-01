# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 NOEL-BARON Léo
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


"""Package contenant l'éditeur 'recedit'.

Si des redéfinitions de contexte-éditeur standard doivent être faites, elles
seront placées dans ce package

Note importante : ce package contient la définition d'un éditeur, mais
celui-ci peut très bien être étendu par d'autres modules. Au quel cas,
les extensions n'apparaîtront pas ici.

"""

from textwrap import dedent

from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.selection import Selection
from primaires.interpreteur.editeur.entier import Entier
from primaires.interpreteur.editeur.choix import Choix
from .edt_ingredients import EdtIngredients
from .edt_resultat import EdtResultat
from secondaires.cuisine.types.ustensile import Ustensile

class EdtRecedit(Presentation):

    """Classe définissant l'éditeur de recette 'recedit'.

    """

    nom = "recedit"

    def __init__(self, personnage, recette):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None

        Presentation.__init__(self, instance_connexion, recette)
        if personnage and recette:
            self.construire(recette)

    def __getnewargs__(self):
        return (None, None)

    def construire(self, recette):
        """Construction de l'éditeur"""
        # Difficulté
        difficulte = self.ajouter_choix("difficulté", "d",
                Entier, recette, "difficulte", 1, 100)
        difficulte.parent = self
        difficulte.prompt = "Difficulté de la recette : "
        difficulte.apercu = "{objet.difficulte}"
        difficulte.aide_courte = \
            "Entrez la |ent|difficulté|ff| de la recette entre |cmd|1|ff| " \
            "et |cmd|100|ff| ou |cmd|/|ff| pour revenir à\nla fenêtre " \
            "parente.\n\nDifficulté actuelle : |bc|{objet.difficulte}|ff|"

        # Temps de cuisson
        temps = self.ajouter_choix("temps de cuisson", "t",
                Entier, recette, "temps_cuisson", 1)
        temps.parent = self
        temps.prompt = "Temps de cuisson : "
        temps.apercu = "{objet.temps_cuisson}"
        temps.aide_courte = \
            "Entrez le |ent|temps|ff| de cuisson en secondes " \
            "ou |cmd|/|ff| pour revenir à la fenêtre " \
            "parente.\n\nTemps actuel : |bc|{objet.temps_cuisson}|ff|"

        # Cuisson
        cuisson = self.ajouter_choix("cuisson", "c", Choix, recette,
                "cuisson", ["doux", "moyen", "vif"])
        cuisson.parent = self
        cuisson.prompt = "Cuisson à feu : "
        cuisson.apercu = "feu {objet.cuisson}"
        cuisson.aide_courte = \
            "Entrez la |ent|cuisson|ff| (feu |cmd|doux|ff|, |cmd|moyen|ff| " \
            "ou |cmd|vif|ff|) ou |cmd|/|ff| pour revenir à\nla fenêtre " \
            "parente.\n\nCuisson actuelle : |bc|feu {objet.cuisson}|ff|"

        # Ustensiles
        l_ustensiles = list(Ustensile.types.keys())
        ustensiles = self.ajouter_choix("ustensiles", "u", Selection, recette,
                "ustensiles", l_ustensiles)
        ustensiles.parent = self
        ustensiles.prompt = "Type d'ustensile : "
        ustensiles.apercu = "{objet.aff_ustensiles}"
        ustensiles.aide_courte = \
            "Entrez les |ent|ustensiles|ff| dans lesquels on peut cuire " \
            "cette recette\nou |cmd|/|ff| pour revenir à la fenêtre " \
            "parente.\n\nTypes d'ustensiles existants : {}\n\nTypes " \
            "actuellement admis : |bc|{{objet.aff_ustensiles}}|ff|".format(
            ", ".join(l_ustensiles))

        # Liste des ingrédients
        ingredients = self.ajouter_choix("ingrédients", "i",
                EdtIngredients, recette, "ingredients")
        ingredients.parent = self
        ingredients.apercu = "{objet.aff_ingredients}"
        ingredients.aide_courte = \
            ""

        # Résultat
        resultat = self.ajouter_choix("résultat", "r",
                EdtResultat, recette, "resultat")
        resultat.parent = self
        resultat.prompt = "Résultat de la recette : "
        resultat.apercu = "{objet.aff_resultat}"
        resultat.aide_courte = \
            "Entrez le |ent|résultat|ff| de la recette (prototype d'objet) " \
            "ou |cmd|/|ff| pour revenir à\nla fenêtre parente.\n\n" \
            "Résultat actuel : |bc|{objet.aff_resultat}|ff|"

# Expérience
        xp = self.ajouter_choix("expérience", "x",
                Entier, recette, "xp", 0)
        xp.parent = self
        xp.prompt = "Expérience gagnée par le personnage en réussissant la recette : "
        xp.apercu = "{objet.xp} XP"
        xp.aide_courte = dedent("""
            Entrez l'|ent|expérience|ff| gagnée par le personnage.

            Entrez |cmd|/|ff| pour revenir à la fenêtre parente.
            Cette expérience est celle reçue dans le niveau survie par un
            personnage réusissant la recette. Le calcul de base conseillé
            est la difficulté de la recette multipliée par 50, le tout
            multiplié par le nombre d'ingrédients nécessaires et/ou
            le nombre de types d'ingrédients nécessaires.

            Expérience gagnée actuelle : |bc|{objet.xp}|ff|
        """.strip("\n"))

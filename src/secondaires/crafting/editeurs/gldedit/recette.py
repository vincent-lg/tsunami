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


"""Module contenant l'éditeur d'recettes de rang."""

from primaires.interpreteur.editeur.choix import Choix
from primaires.interpreteur.editeur.entier import Entier
from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.tableau import Tableau
from primaires.interpreteur.editeur.uniligne import Uniligne
from primaires.scripting.editeurs.edt_script import EdtScript

class GldRecetteEdit(Presentation):

    """Classe définissant l'éditeur d'recettes."""

    nom = "gldedit:recette"

    def __init__(self, personnage, recette, attribut=None):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None

        Presentation.__init__(self, instance_connexion, recette, None, False)
        if personnage and recette:
            self.construire(recette)

    def __getnewargs__(self):
        return (None, None)

    def construire(self, recette):
        """Construction de l'éditeur"""
        # Résultat
        resultat = self.ajouter_choix("résultat", "r", Choix, recette,
                "resultat", list(importeur.objet.prototypes.keys()))
        resultat.parent = self
        resultat.prompt = "Résultat de la recette : "
        resultat.apercu = "{valeur}"
        resultat.aide_courte = \
            "Entrez le |ent|résultat|ff| de l'recette ou |cmd|/|ff| pour " \
            "revenir à la fenêtre parente.\n\nLe résultat d'une " \
            "recette doit être la clé du prototype d'objet.\n\nRésultat " \
            "actuel : |bc|{valeur}|ff|"

        # Nom
        nom = self.ajouter_choix("nom", "n", Uniligne, recette, "nom")
        nom.parent = self
        nom.prompt = "Nom de la recette : "
        nom.apercu = "{valeur}"
        nom.aide_courte = \
            "Entrez le |ent|nom|ff| de l'recette ou |cmd|/|ff| pour " \
            "revenir à la fenêtre parente.\n\nCertaines guildes ont " \
            "besoin de nommer leur recette, car elles\nutilisent des " \
            "recettes avec des ingrédients identiques. Il faut\ndonc " \
            "demander précisément au joueur ce qu'il veut fabriquer, d'où\n" \
            "l'utilité des noms.\n\nNom actuel : |bc|{valeur}|ff|"

        # Quantité de résultat
        quantite = self.ajouter_choix("quantité d'objets à créer",
                "q", Entier, recette, "quantite", 1)
        quantite.parent = self
        quantite.apercu = "{valeur}"
        quantite.prompt = "Quantité d'objets à créer sur le prototype " \
                "'resultat' : "
        quantite.aide_courte = \
            "Entrez |ent|la quantité d'objets|ff| à créer " \
            "ou |cmd|/|ff| pour revenir\nà la fenêtre parente.\n\n" \
            "Ce paramètre détermine le nombre de fois que le résultat " \
            "sera créé\ndans la salle. Si la quantité est de 1, seul " \
            "un objet sera créé.\nSi la quantite est de 3, trois objets " \
            "sur le prototype du résultat\nprécisé seront créés. Les " \
            "attributs seront copiés dans tous ces objets.\n\n" \
            "Quantité actuelle : {valeur}"

        # Nombre nécessaire pour la progression
        nb_max = self.ajouter_choix("nombre d'objets nécessaires " \
                "pour progresser dans le rang", "b", Entier, recette,
                "nb_max", 1)
        nb_max.parent = self
        nb_max.apercu = "{valeur} fois"
        nb_max.prompt = "Nombre maximum d'objets à faire dans ce rang : "
        nb_max.aide_courte = \
            "Entrez |ent|le nombre d'objets|ff| nécessaires " \
            "ou |cmd|/|ff| pour revenir\nà la fenêtre parente.\n\n" \
            "Chaque rang définit des objets de rang. Les artisans " \
            "doivent fabriquer\nces objets pour progresser. Chaque " \
            "objet doit être fait une ou plusieurs\nfois. Ce nombre " \
            "est définit ici. Si vous renseigner |ent|3|ff| par\nexemple, " \
            "alors le membre devra faire cette recette trois fois pour\n" \
            "pouvoir progresser. Si il ne le fabrique pas trois fois, " \
            "il ne pourra\npas finir son rang.\n\nNombre actuel : {valeur}"

        # Types
        liste_types = list(importeur.objet.types.keys())
        types = self.ajouter_choix("types", "t", Tableau,
                recette, "ingredients_types",
                (("type", liste_types), ("minimum", "entier"),
                ("maximum", "entier")))
        types.parent = self
        types.apercu = "{taille}"
        types.aide_courte = \
            "Vous pouvez configurer ici les types " \
            "d'objets nécessaires pour la recette. Il existe " \
            "deux sortes\nd'ingrédients : les types (par " \
            "exemple fourrure) ou les\nclés d'objet précises (par " \
            "exemple rubis). Ce tableau\ncontient les types " \
            "d'objet et leur quantité. Précisez :\n |cmd|<nom " \
            "du type> / <qtt minimum> / <qtt maximum>|ff|\nPar " \
            "exemple :\n |cmd|légume / 8 / 15|ff|\n\nPour supprimer " \
            "un type d'ingrédient, utilisez l'option :\n |cmd|/s <nom " \
            "du type à supprimer>|ff|\n\nTypes actuel :\n{valeur}"

        # Objets
        liste_objets = list(importeur.objet.prototypes.keys())
        objets = self.ajouter_choix("objets", "o", Tableau,
                recette, "ingredients_objets",
                (("prototype", liste_objets), ("minimum", "entier"),
                ("maximum", "entier")))
        objets.parent = self
        objets.apercu = "{taille}"
        objets.aide_courte = \
            "Vous pouvez configurer ici les objets " \
            "nécessaires pour la recette. Il existe " \
            "deux sortes\nd'ingrédients : les types (par " \
            "exemple fourrure) ou les\nclés d'objet précises (par " \
            "exemple rubis). Ce tableau\ncontient les objets " \
            "et leur quantité. Précisez :\n |cmd|<clé " \
            "du prototype> / <qtt minimum> / <qtt maximum>|ff|\nPar " \
            "exemple :\n |cmd|pomme_rouge / 8 / 12|ff|\n\nPour " \
            "supprimer un ingrédient, utilisez l'option :\n |cmd|/s " \
            "<clé du prototype à supprimer>|ff|\n\nObjets actuel :\n{valeur}"

        # Script
        scripts = self.ajouter_choix("scripts", "sc", EdtScript,
                recette.script)
        scripts.parent = self

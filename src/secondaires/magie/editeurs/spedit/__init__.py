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


"""Package contenant l'éditeur 'spedit'.
Si des redéfinitions de contexte-éditeur standard doivent être faites, elles
seront placées dans ce package.

Note importante : ce package contient la définition d'un éditeur, mais
celui-ci peut très bien être étendu par d'autres modules. Auquel cas,
les extensions n'apparaîtront pas ici.

"""

from primaires.interpreteur.editeur.choix import Choix
from primaires.interpreteur.editeur.description import Description
from primaires.interpreteur.editeur.entier import Entier
from primaires.interpreteur.editeur.flag import Flag
from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.selection import Selection
from primaires.interpreteur.editeur.uniligne import Uniligne
from primaires.scripting.editeurs.edt_script import EdtScript
from secondaires.magie.constantes import ELEMENTS
from .edt_difficulte import EdtDifficulte
from .supprimer import NSupprimer

class EdtSpedit(Presentation):

    """Classe définissant l'éditeur de sort 'spedit'.

    """

    nom = "spedit"

    def __init__(self, personnage, sort):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None

        Presentation.__init__(self, instance_connexion, sort)
        if personnage and sort:
            self.construire(sort)

    def __getnewargs__(self):
        return (None, None)

    def construire(self, sort):
        """Construction de l'éditeur"""
        # Nom
        nom = self.ajouter_choix("nom", "n", Uniligne, sort, "nom")
        nom.parent = self
        nom.prompt = "Nom du sort (sans article) : "
        nom.apercu = "{objet.nom}"
        nom.aide_courte = \
            "Entrez le |ent|nom|ff| du sort ou |cmd|/|ff| pour revenir " \
            "à la fenêtre parente.\n\nNom actuel : |bc|{objet.nom}|ff|"

        # Description
        description = self.ajouter_choix("description", "d", Description, \
                sort)
        description.parent = self
        description.apercu = "{objet.description.paragraphes_indentes}"
        description.aide_courte = \
            "| |tit|" + "Description du sort {}".format(sort.cle).ljust(76) + \
            "|ff||\n" + self.opts.separateur

        # Points de tribut
        tribut = self.ajouter_choix("points de tribut", "tr", Entier, sort,
                "points_tribut", 1)
        tribut.parent = self
        tribut.prompt = "Points de tribut nécessaire pour apprendre le sort : "
        tribut.apercu = "{objet.points_tribut}"
        tribut.aide_courte = \
            "Entrez le |ent|nombre de points de tribut|ff| nécessaires "\
            "pour apprendre le sort\nou |cmd|/|ff| pour revenir à la " \
            "fenêtre parente.\n\nPoints de tribut actuels : " \
            "|bc|{objet.points_tribut}|ff|"

        # Éléments
        elements = self.ajouter_choix("eléments", "e", Selection, sort,
                "elements", ELEMENTS)
        elements.parent = self
        elements.apercu = "{objet.str_elements}"
        elements.aide_courte = \
            "Entrez un |ent|élément|ff| pour l'ajouter " \
            "ou le retirer\nou |cmd|/|ff| " \
            "pour revenir à la fenêtre parente.\n\n" \
            "Éléments existants : |cmd|" + "|ff|, |cmd|".join(
            ELEMENTS) + "\n" \
            "Éléments actuels : |bc|{objet.str_elements}|ff|"

        # Type de sort
        types = ["destruction", "alteration", "invocation", "illusion"]
        type = self.ajouter_choix("type de sort", "s", Choix, sort,
                "type", types)
        type.parent = self
        type.prompt = "Type de sort : "
        type.apercu = "{objet.type}"
        type.aide_courte = \
            "Entrez le |ent|type|ff| du sort ou |cmd|/|ff| " \
            "pour revenir à la fenêtre parente.\nTypes disponibles : |cmd|" \
            "{}|ff|.\n\nType actuel : |bc|{{objet.type}}|ff|".format(
            "|ff|, |cmd|".join(types))

        # Cible
        types = ["aucune", "personnage", "objet", "salle"]
        cible = self.ajouter_choix("type de cible", "c", Choix, sort,
                "type_cible", types)
        cible.parent = self
        cible.prompt = "Type de cible : "
        cible.apercu = "{objet.type_cible}"
        cible.aide_courte = \
            "Entrez le |ent|type de cible|ff| du sort ou |cmd|/|ff| " \
            "pour revenir à la fenêtre parente.\nTypes disponibles : |cmd|" \
            "{}|ff|.\n\nType actuel : |bc|{{objet.type_cible}}|ff|".format(
            "|ff|, |cmd|".join(types))

        # Stats
        stats = self.ajouter_choix("stats", "st", Selection, sort,
                "stats", ("agilite", "intelligence", "sensibilite"))
        stats.parent = self
        stats.apercu = "{objet.str_stats}"
        stats.aide_courte = \
            "Entrez une |ent|stat|ff| pour l'ajouter " \
            "ou la retirer\nou |cmd|/|ff| " \
            "pour revenir à la fenêtre parente.\n\n" \
            "stats actuelles : |bc|{objet.str_stats}|ff|"

        # Difficulté
        difficulte = self.ajouter_choix("difficulté", "i", Entier, sort,
                "difficulte", 0, 100)
        difficulte.parent = self
        difficulte.prompt = "Difficulté d'apprentissage : "
        difficulte.apercu = "{objet.difficulte}"
        difficulte.aide_courte = \
            "Paramétrez la |ent|difficulté|ff| d'apprentissage du sort " \
            "entre |cmd|0|ff| et |cmd|100|ff| ou entrez\n|cmd|/|ff| pour " \
            "revenir à la fenêtre parente. |cmd|100|ff| signifie que le sort " \
            "ne peut pas\nêtre appris par la pratique.\n\n" \
            "Difficulté actuelle : |bc|{objet.difficulte}|ff|"

        # Coût
        cout = self.ajouter_choix("coût", "o", Entier, sort, "cout")
        cout.parent = self
        cout.prompt = "Coùt en mana : "
        cout.apercu = "{objet.cout}"
        cout.aide_courte = \
            "Entrez la |ent|quantité|ff| d'énergie magique nécessaire pour " \
            "lancer ce sort ou |cmd|/|ff| pour\nrevenir à la fenêtre " \
            "parente.\n\n" \
            "Coût : |bc|{objet.cout}|ff|"

        # Durée
        duree = self.ajouter_choix("durée de concentration", "u", Entier, sort,
                "duree", 1)
        duree.parent = self
        duree.prompt = "Durée de concentration : "
        duree.apercu = "{objet.duree}"
        duree.aide_courte = \
            "Entrez la |ent|durée|ff| de concentration du sort, en " \
            "secondes, ou |cmd|/|ff| pour revenir à\nla fenêtre parente. La " \
            "durée diminue automatiquement quand la maîtrise du sort\n" \
            "augmente ; la valeur entrée correspond au temps maximum.\n\n" \
            "Durée actuelle : |bc|{objet.duree}|ff|"

        # Offensif
        offensif = self.ajouter_choix("offensif", "of", Flag, sort,
                "offensif")
        offensif.parent = self

        # Distance
        distance = self.ajouter_choix("distance", "t", Flag, sort,
                "distance")
        distance.parent = self

        # Script
        scripts = self.ajouter_choix("scripts", "sc", EdtScript,
                sort.script)
        scripts.parent = self

        # Suppression
        suppression = self.ajouter_choix("supprimer", "sup", NSupprimer, \
                sort)
        suppression.parent = self
        suppression.aide_courte = "Souhaitez-vous réellement supprimer " \
                "le sort {} ?".format(sort.nom)
        suppression.action = "magie.supprimer_sort"
        suppression.confirme = "Le sort {} a bien été supprimé.".format(
                sort.nom)

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


"""Module contenant l'éditeur de commande dynamique."""

from primaires.interpreteur.editeur.choix import Choix
from primaires.interpreteur.editeur.description import Description
from primaires.interpreteur.editeur.flag import Flag
from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.tableau import Tableau
from primaires.interpreteur.editeur.uniligne import Uniligne
from primaires.scripting.editeurs.edt_script import EdtScript

class EdtCmdedit(Presentation):

    """Classe définissant l'éditeur de commande dynamique."""

    nom = "gldedit:commande"

    def __init__(self, personnage, commande, attribut=None, *args):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None

        Presentation.__init__(self, instance_connexion, commande)
        if personnage and commande:
            self.construire(commande)

    def __getnewargs__(self):
        return (None, None)

    def construire(self, commande):
        """Construction de l'éditeur"""
        # Groupe
        groupes = importeur.interpreteur.groupes.nom_groupes
        groupe = self.ajouter_choix("groupe", "r", Choix, commande,
                "groupe", groupes)
        groupe.parent = self
        groupe.apercu = "{valeur}"
        groupe.aide_courte = \
            "Entrez le |ent|groupe d'exécution|ff| de la commande ou\n" \
            "|cmd|/|ff| pour revenir à la fenêtre " \
            "parente.\n\nGroupes existants : " + ", ".join(groupes) + \
            ".\n\nGroupe actuel : |bc|{valeur}|ff|"

        # Catégorie
        categories = sorted(list(importeur.interpreteur.categories.items()),
                key=lambda c: c[1])
        categorie = self.ajouter_choix("catégorie", "c", Choix, commande,
                "nom_categorie", list(
                importeur.interpreteur.categories.keys()))
        categorie.parent = self
        categorie.apercu = "{valeur}"
        categorie.aide_courte = \
            "Entrez la |ent|catégorie|ff| de la commande ou " \
            "|cmd|/|ff| pour revenir à la fenêtre " \
            "parente.\n\nCatégories possibles :"

        for identifiant, nom in categories:
            categorie.aide_courte += "\n  |ent|{}|ff| ({})".format(
                    identifiant, nom)

        categorie.aide_courte += \
            "\n\nCatégorie actuelle : |bc|{valeur}|ff|"

        # Schéma
        schema = self.ajouter_choix("schéma", "h", Uniligne, commande,
                "schema")
        schema.parent = self
        schema.prompt = "Schéma de la commande : "
        schema.apercu = "{valeur}"
        schema.aide_courte = \
            "Entrez le |ent|schéma|ff| de la commande ou |cmd|/|ff| " \
            "pour revenir à la fenêtre parente.\n\n" \
            "Le schéma d'une commande représente les informations " \
            "qui\ndoivent être passées en paramètre de la commande. " \
            "La syntaxe\ncomplète d'un schéma peut parfois être " \
            "assez complexe et mérite de\nplus longues explications. " \
            "En fonction du schéma choisit, certaines\nvariables seront " \
            "accessibles dans le script de la commande.\n\nQuelques " \
            "exemples :\n" \
            "    <message>\n" \
            "    (<texte_libre>)\n" \
            "    (<nombre>) <objet_inventaire>\n" \
            "    <objet_sol> dans/into <objet_inventaire>\n\n" \
            "Schéma actuel : |bc|{valeur}|ff|"

        # Aide courte
        synopsys = self.ajouter_choix("synopsys", "s", Uniligne, commande,
                "aide_courte")
        synopsys.parent = self
        synopsys.prompt = "Synopsys de la commande : "
        synopsys.apercu = "{valeur}"
        synopsys.aide_courte = \
            "Entrez le |ent|synopsys|ff| de la commande ou |cmd|/|ff| " \
            "pour revenir à la fenêtre parente.\n\n" \
            "Synopsys actuel : |bc|{valeur}|ff|"

        # Aide longue
        aide_longue = self.ajouter_choix("aide longue", "g", Description, \
                commande, "aide_longue")
        aide_longue.parent = self
        aide_longue.apercu = "{objet.aide_longue.paragraphes_indentes}"
        aide_longue.aide_courte = \
            "| |tit|" + "Aide longue de la commande {}".format(
            commande).ljust(76) + "|ff||\n" + self.opts.separateur

        # Utilisable
        utilisable = self.ajouter_choix("commande utilisable", "uti",
                Flag, commande, "utilisable")
        utilisable.parent = self

        # États
        etats = self.ajouter_choix("états", "t", Tableau,
                commande, "etats",
                (("clé", "clé"), ("refus", "chaîne"), ("visible", "chaîne"),
                ("actions autorisées", "chaîne")), None, "maj")
        etats.parent = self
        etats.apercu = "{taille}"
        etats.aide_courte = \
            "Vous pouvez configurer ici le tableau des états.\n" \
            "Un état empêche un personnage d'effectuer certaines " \
            "actions.\nPar exemple, si le personnage est en train " \
            "de pêcher (un état\nspécifique est associé à la pêche), " \
            "il ne peut se déplacer. Le\nconcept d'états permet " \
            "de mettre en pause une certaine action en\ngarantissant " \
            "que le joueur est toujours occupé.\nPour créer un état, " \
            "précisez quatre arguments séparés par le\nsigne |ent|/|ff| :\n" \
            "    |ent|La clé de l'état|ff| (utile pour le scripting " \
            "notammment)\n" \
            "    |ent|Le message de refus|ff| (par exemple " \
            "|cmd|Vous êtes en train de pêcher|ff|)\n" \
            "    |ent|Le message visible pour les personnages " \
            "présents dans la salle|ff| ;\n" \
            "    |ent|Les actions autorisées|ff| séparées par un " \
            "espace.\n(Les actions peuvent être |ent|parler|ff|, " \
            "|ent|regarder|ff| ou |ent|ingérer|ff| par exemple)\n\n" \
            "Par exemple :\n    |ent|peche / Vous êtes en train de " \
            "pêcher / pêche tranquillement ici|ff|\n\n" \
            "Pour supprimer un état, utilisez :\n" \
            " |ent|/s <clé de l'état à supprimer>|ff|\n\n" \
            "États actuel :\n{valeur}"

        # Script
        scripts = self.ajouter_choix("scripts", "sc", EdtScript,
                commande.script)
        scripts.parent = self


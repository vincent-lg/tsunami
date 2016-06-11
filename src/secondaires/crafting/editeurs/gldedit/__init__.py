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


"""Package contenant l'éditeur de guilde 'gldedit'.

Si des redéfinitions de contexte-éditeur standard doivent être faites, elles
seront placées dans ce package

Note importante : ce package contient la définition d'un éditeur, mais
celui-ci peut très bien être étendu par d'autres modules. Au quel cas,
les extensions n'apparaîtront pas ici.

"""

from primaires.interpreteur.editeur.aes import AES
from primaires.interpreteur.editeur.flag import Flag
from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.uniligne import Uniligne
from primaires.scripting.editeurs.edt_script import EdtScript
from secondaires.crafting.editeurs.gldedit import atelier
from secondaires.crafting.editeurs.gldedit import commande
from secondaires.crafting.editeurs.gldedit import extension
from secondaires.crafting.editeurs.gldedit import rang
from secondaires.crafting.editeurs.gldedit import recette
from secondaires.crafting.editeurs.gldedit import talent
from secondaires.crafting.editeurs.gldedit import type
from secondaires.crafting.editeurs.gldedit.types import EdtTypes

class GldEdit(Presentation):

    """Classe définissant l'éditeur de guilde."""

    nom = "gldedit"

    def __init__(self, personnage, guilde):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None

        Presentation.__init__(self, instance_connexion, guilde)
        if personnage and guilde:
            self.construire(guilde)

    def __getnewargs__(self):
        return (None, None)

    def construire(self, guilde):
        """Construction de l'éditeur"""
        # Nom
        nom = self.ajouter_choix("nom", "n", Uniligne, guilde, "nom")
        nom.parent = self
        nom.prompt = "Nom de la guilde : "
        nom.apercu = "{valeur}"
        nom.aide_courte = \
            "Entrez le |ent|nom|ff| de la guilde ou |cmd|/|ff| pour " \
            "revenir à la fenêtre parente.\n\nNom actuel : " \
            "|bc|{valeur}|ff|"

        # Ouverte
        ouverte = self.ajouter_choix("ouverte", "ouv", Flag, guilde,
                "ouverte")
        ouverte.parent = self

        # Ateliers
        ateliers = self.ajouter_choix("ateliers", "a", AES,
                guilde, "ateliers", "gldedit:atelier", (("clé", "clé"), ),
                "get_atelier", "ajouter_atelier", "supprimer_atelier",
                "cle_complete")
        ateliers.parent = self
        ateliers.apercu = "{valeur}"
        ateliers.aide_courte = \
            "Entrez la clé d'un atelier pour l'éditer ou :\n" \
            " |ent|/a <clé de l'atelier à créer>|ff|\n" \
            " |ent|/s <clé de l'atelier à supprimer>|ff|\n\n" \
            "Ateliers actuels :{valeur}"

        # Rangs
        rangs = self.ajouter_choix("rangs", "r", AES,
                guilde, "rangs", "gldedit:rang", (("clé", "clé"), ),
                "get_rang", "ajouter_rang", "supprimer_rang", "nom_complet")
        rangs.parent = self
        rangs.apercu = "{valeur}"
        rangs.aide_courte = \
            "Entrez la clé d'un rang pour l'éditer ou :\n" \
            " |ent|/a <clé du rang à créer>|ff|\n" \
            " |ent|/s <clé du rang à supprimer>|ff|\n\n" \
            "Rangs actuels :{valeur}"

        # Types
        types = self.ajouter_choix("types dynamiques", "t", EdtTypes,
                guilde, "types", "gldedit:type",
                (("parent", "chaîne"), ("nom", "chaîne")), "get_type",
                "ajouter_type", None, "nom_complet")
        types.parent = self
        types.apercu = "{valeur}"
        types.aide_courte = \
            "Entrez |ent|le nom du type|ff| pour l'éditer ou :\n" \
            " |ent|/a <nom du type parent / nom du type à créer>|ff|\n" \
            " |ent|/i <nom du type pour plus d'informations>|ff|\n\n" \
            "Types définis dans cette guilde :{valeur}"

        # Commandes dynamique
        commandes = self.ajouter_choix("commandes dynamiques", "c", AES,
                guilde, "commandes", "gldedit:commande",
                (("nom", "chaîne"), ), "get_commande",
                "ajouter_commande", "supprimer_commande", "nom_complet")
        commandes.parent = self
        commandes.apercu = "{valeur}"
        commandes.aide_courte = \
            "Entrez |ent|le nom de la commande|ff| pour l'éditer ou :\n" \
            " |ent|/a <nom de la commande à ajouter>|ff|\n" \
            " |ent|/s <nom de la commande à supprimer>|ff|\n\n" \
            "Le nom d'une commande doit être composé du nom éventuel " \
            "des commandes\nparentes, un signe deux points, le " \
            "nom français, un signe |ent|/|ff|\net le nom anglais.\n\n" \
            "Par exemple :\n" \
            "    |ent|chanter/sing|ff|\n" \
            "Pour créer la commande sans parent. Ou :\n" \
            "    |ent|oeuf:casser/break|ff|\n" \
            "Pour ajouter le paramètre casser/break à la commande " \
            "oeuf.\n\nCommandes définies dans cette guilde :{valeur}"


        # Talents
        talents = self.ajouter_choix("talents", "l", AES,
                guilde, "talents", "gldedit:talent",
                (("clé", "clé"), ), "get_talent", "ajouter_talent", None,
                "nom_complet")
        talents.parent = self
        talents.apercu = "{valeur}"
        talents.aide_courte = \
            "Entrez |ent|la clé du talent|ff| pour l'éditer ou :\n" \
            " |ent|/a <clé du talent à ajouter>|ff|\n\n" \
            "Talents actuels :{valeur}"

        # Extensions
        extensions = self.ajouter_choix("extensions d'éditeur", "e", AES,
                guilde, "extensions", "gldedit:extension",
                (("éditeur", "chaîne"), ("nom", "chaîne"), ("type", "chaîne")),
                "get_extension", "ajouter_extension", "supprimer_extension",
                "nom_complet")
        extensions.parent = self
        extensions.apercu = "{valeur}"
        extensions.aide_courte = \
            "Entrez |ent|le nom de l'extension|ff| pour l'éditer ou :\n" \
            " |ent|/a <éditeur / nom de l'extension à ajouter / type>|ff|\n" \
            " |ent|/s <nom de l'extension à supprimer>|ff|\n\n" \
            "Les éditeurs possibles sont : |ent|salle|ff|, " \
            "|ent|objet|ff| ou |ent|PNJ|ff|.\n" \
            "Les types d'extension possibles sont :\n" \
            "    bool (un bool ou flag vrai ou faux)\n" \
            "    chaîne (une chaîne de caractères sans contrainte)\n" \
            "    clé (une chaîne sans accent ni majuscules)\n" \
            "    entier (un nombre entier sans contrainte)\n" \
            "    entier positif / négatif / positif ou nul / " \
            "négatif ou nul\n" \
            "    entier entre X et Y\n" \
            "    flottant (un nombre à virgule flottante)\n" \
            "    prototype d'objet (un prototype d'objet)\n" \
            "    tableau avec les colonnes nom (type), nom2 (type2)...\n\n" \
            "Exemples de types :\n" \
            "    entier positif ou nul\n" \
            "    entier entre 5 et 32\n" \
            "    tableau avec les colonnes nom (chaîne), âge (entier)\n\n" \
            "Extensions actuelles :{valeur}"

        # Script
        scripts = self.ajouter_choix("scripts", "sc", EdtScript,
                guilde.script)
        scripts.parent = self

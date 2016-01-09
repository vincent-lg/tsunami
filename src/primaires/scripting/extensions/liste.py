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


"""Module contenant la classe Liste, détaillée plus bas."""

from textwrap import dedent

from primaires.interpreteur.editeur.aes import AES
from primaires.interpreteur.editeur.env_objet import EnveloppeObjet
from primaires.interpreteur.editeur.uniligne import Uniligne, CLE
from primaires.scripting.editeurs.edt_script import EdtScript
from primaires.scripting.extensions.base import Extension
from primaires.scripting.script import Script

class Liste(Extension):

    """Classe représentation le type éditable 'liste'.

    Ce type utilise l'éditeur AES. Il s'agit donc d'une liste d'objets
    complexes, dont chacun peut posséder son éditeur.

    """

    extension = "liste"
    aide = "une liste de structures externes"

    def __init__(self, structure, nom):
        Extension.__init__(self, structure, nom)
        self.script = ScriptListe(self)
        self.structure_externe = None
        self.case_affichage = None

    @property
    def editeur(self):
        """Retourne le type d'éditeur."""
        return AES

    @property
    def arguments(self):
        """Retourne les arguments de l'éditeur."""
        return (None, (("titre", "chaîne"), ), "get_element",
                "ajouter_element", "supprimer_element", "afficher_element",
                self)

    def etendre_editeur(self, presentation):
        """Ëtend l'éditeur en fonction du type de l'extension."""
        # Clé de l'extension externe
        externe = presentation.ajouter_choix("structure externe",
                "s", Uniligne, self, "structure_externe", CLE)
        externe.parent = presentation
        externe.apercu = "{valeur}"
        externe.prompt = "Structure externe : "
        externe.aide_courte = dedent("""
            Entrez |ent|la clé de l'extension externe|ff|
            Ou |cmd|/|ff| pour revenir à la fenêtre parente.

            Il s'agit ici de préciser le type de structure qui sera
            créée et manipulée par le système, quand le joueur utilisera
            l'éditeur d'ajout ou suppression. Plus important encore, le
            système a besoin de savoir quel éditeur appeler quand le
            joueur veut éditer un élément de la liste. Par exemple, on
            peut imaginer que des structures de type |cmd|journal|ff|
            définissent une liste d'|cmd|articles|ff| pourvant être
            ajoutés et supprimés d'un journal. Ainsi, la structure
            |cmd|journal|ff| pourra définir une liste, dont la structure
            externe sera |cmd|article|ff|, c'est-à-dire qu'une structure
            de type |cmd|article|ff| pourrra être créée et éditée depuis
            l'éditeur de |cmd|journal|ff|. L'éditeur |cmd|article|ff|
            devra exister dans ce contexte.

            Structure externe actuelle : {valeur}""".strip("\n"))

        # Nom de la case de l'extension externe
        nom = presentation.ajouter_choix("nom de la case de l'extension " \
                "à afficher", "n", Uniligne, self, "case_affichage", CLE)
        nom.parent = presentation
        nom.apercu = "{valeur}"
        nom.prompt = "Nom de la case à afficher : "
        nom.aide_courte = dedent("""
            Entrez |ent|le nomm de la case à afficher|ff|
            Ou |cmd|/|ff| pour revenir à la fenêtre parente.

            On doit ici préciser le nom de la case de l'extension
            qui sera affichée lors de l'affichage et de l'ajout. Il
            peut s'agir souvent du nom |cmd|titre|ff| : quand un joueur
            créera le nouvel élément à l'aide de l'option |cmd|/a|ff|,
            il devra préciser une information en paramètre. Cette
            information sera mise dans la case précisée ici. Les
            éléments de la liste seront également affichés grâce à
            cette case. Choisissez donc une des cases de l'extension
            à créer : elle doit la représenter et être appropriée pour
            l'édition de joueur. Elle est forcément une chaîne de
            caractères (pas un nombre ou une autre information).

            Nom actuel de la case : {valeur}""".strip("\n"))

        # Script
        scripts = presentation.ajouter_choix("scripts", "sc", EdtScript,
                self.script)
        scripts.parent = presentation

    def get_element(self, liste, numero, exception=True):
        """Retourne l'élément dans la case indiquée."""
        try:
            numero = int(numero)
            assert numero > 0
            assert numero <= len(liste)
        except (ValueError, AssertionError):
            if exception:
                raise ValueError("Numéro invalide {}.".format(numero))

            return None
        else:
            return liste[numero - 1]

    def ajouter_element(self, structure, liste, information):
        """Ajoute un élément."""
        element = importeur.scripting.creer_structure(self.structure_externe)
        setattr(element, self.case_affichage, information)
        liste.append(element)
        self.script["ajout"].executer(structure=structure, externe=element)

    def supprimer_element(self, structure, liste, numero):
        """Supprime un élément."""
        element = self.get_element(liste, numero)
        liste.remove(element)
        importeur.scripting.supprimer_structure(element)
        self.script["supprime"].executer(structure=structure, externe=element)

    def afficher_element(self, liste, element):
        """Affichage de l'élément de la liste."""
        indice = liste.index(element) + 1
        information = getattr(element, self.case_affichage)
        return "  {:>2} - {}".format(indice, information)

    def editer_element(self, editeur, structure, liste, element):
        """Édite un élément de la liste."""
        EdtEditeur = __import__("primaires.scripting.editeurs.personnalise") \
                .scripting.editeurs.personnalise.EdtEditeur
        pere = editeur.pere
        personnage = pere.joueur
        obj_editeur = importeur.scripting.editeurs[self.structure_externe]
        enveloppe = EnveloppeObjet(EdtEditeur, obj_editeur,
                element, False)
        enveloppe.parent = editeur
        contexte = enveloppe.construire(pere)
        editeur.migrer_contexte(contexte)


class ScriptListe(Script):

    """Définition des ajout scriptables."""

    def init(self):
        """Initialisation du script."""
        # Événement ajout
        evt_ajout = self.creer_evenement("ajout")
        evt_ajout.aide_courte = "un joueur ajoute un élément dans la liste"
        evt_ajout.aide_longue = \
            "Cet évènement est appelé quand un joueur dans l'éditeur " \
            "ajoute un élément à l'aide de l'option |cmd|/a|ff|. La " \
            "structure externe est créée et ajoutée à la liste " \
            "d'éléments. Cet évènement peut être utile pour établir " \
            "un lien entre la structure externe et la structure " \
            "parente. L'évènement 'supprime' est utile dans l'autre sens."

        # Configuration des variables de l'évènement ajout
        var_structure = evt_ajout.ajouter_variable("structure", "Structure")
        var_structure.aide = "la structure parente éditée"
        var_externe = evt_ajout.ajouter_variable("externe", "Structure")
        var_externe.aide = "la structure externe ajoutée"

        # Événement supprime
        evt_supprime = self.creer_evenement("supprime")
        evt_supprime.aide_courte = "un joueur supprime un élément dans la liste"
        evt_supprime.aide_longue = \
            "Cet évènement est appelé quand un joueur dans l'éditeur " \
            "supprime un élément à l'aide de l'option |cmd|/s|ff|. La " \
            "structure externe est supprimée et retirée de la liste " \
            "d'éléments. Cet évènement peut être utile pour détruire " \
            "un lien entre la structure externe et la structure " \
            "parente. L'évènement 'ajoute' est utile dans l'autre sens."

        # Configuration des variables de l'évènement supprime
        var_structure = evt_supprime.ajouter_variable("structure", "Structure")
        var_structure.aide = "la structure parente éditée"
        var_externe = evt_supprime.ajouter_variable("externe", "Structure")
        var_externe.aide = "la structure externe supprimée"

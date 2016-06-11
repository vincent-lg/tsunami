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


"""Module contenant la classe Selection, détaillée plus bas."""

from textwrap import dedent

from primaires.interpreteur.editeur.selection import Selection as EdtSelection
from primaires.interpreteur.editeur.selection_objet import SelectionObjet
from primaires.scripting.editeurs.edt_script import EdtScript
from primaires.scripting.extensions.base import Extension
from primaires.scripting.script import Script

class Selection(Extension):

    """Classe représentant le type éditable 'selection'.

    Ce type utilise l'éditeur SelectionObjet. Il permet de
    sélectionner aucune, un ou plusieurs valeurs.

    """

    extension = "selection"
    aide = "une liste de zéro, une ou plusieurs possibilités"
    nom_scripting = "la sélection d'éditeur"

    def __init__(self, structure, nom):
        Extension.__init__(self, structure, nom)
        self.selection = []
        self.script = ScriptSelection(self)

    @property
    def editeur(self):
        """Retourne le type d'éditeur."""
        return SelectionObjet

    @property
    def arguments(self):
        """Retourne les arguments de l'éditeur."""
        evt = self.script["selection"]
        if evt.nb_lignes:
            evt.executer()
            cles = evt.espaces.variables["retour"]
            evt = self.script["valeurs"]
            if evt.nb_lignes:
                evt.executer()
                valeurs = evt.espaces.variables["retour"]
            else:
                valeurs = list(cles)
        else:
            cles = valeurs = self.selection

        selection = dict(zip(cles, valeurs))
        return (selection, )

    def etendre_editeur(self, presentation):
        """Ëtend l'éditeur en fonction du type de l'extension."""
        # Selection
        selection = presentation.ajouter_choix("valeurs", "v", EdtSelection,
                self, "selection")
        selection.parent = presentation
        selection.apercu = "{valeur}"
        selection.aide_courte = dedent("""
            Entrez |ent|ue valeur|ff| pour l'ajouter ou le retirer.
            Entrez |cmd|/|ff| pour revenir à la fenêtre parente.

            Cet éditeur existe pour laisser le joueur choisir entre
            séro, une ou plusieurs valeurs parmi une liste. On parle
            de sélection, car le joueur sélectionne certaines
            informations. La liste de valeurs peut être très
            simple : par exemple, on demande au joueur de choisir les noms
            de villes qu'il fréquente régulièrement : le joueur
            peut en choisir aucune, une ou plusieurs. La case de la
            structure contiendra la liste des valeurs sélectionnées par
            le joueur. Dans ce cas, vous pouvez entrer directement les
            valeurs possibles pour les ajouter dans la liste des choix
            proposés par l'éditeur.

            Parfois cependant, on a besoin d'offrir un choix plus complexe.
            Par exemple, entrer un ou plusieur noms de joueurs (la liste
            des joueurs étant dynamiquement générée, pas statique).
            Dans ce cas, on peut utiliser les deux évènements définis
            dans le script de cet éditeur : l'évènement 'selection'
            doit retourner une liste des choix possibles. Par exemple,
            dans ce cas, une liste des noms de joueurs. L'évènement
            'valeurs' permet de faire correspondre chaque choix
            de la liste avec une valeur de remplacement : dans le
            cas qui nous occupe, le joueur rentre le nom du  ou des
            joueurs, mais le systhème fait la correspondance avec
            les joueur (les personnages sont écrits dans la structure, pas la
            chaîne de caractères contenant leur nom). Ces scripts sont
            donc bien plus puissants qu'une liste statique, mais peuvent
            s'avérer complexes à utiliser.

            La liste statique définie ici n'est utilisée que si
            l'évènement 'selection' est vide.
            Si l'évènement 'selection' existe mais que l'évènement
            'valeurs' est vide, les chaînes de caractères sont ajoutées
            dans la liste (il n'y a pas de remplacement d'effectué).

            Valeurs autorisées : {valeur}""".strip("\n"))

        # Script
        scripts = presentation.ajouter_choix("scripts", "sc", EdtScript,
                self.script)
        scripts.parent = presentation


class ScriptSelection(Script):

    """Définition des sélection scriptables."""

    def init(self):
        """Initialisation du script."""
        # Événement selection
        evt_selection = self.creer_evenement("selection")
        evt_selection.aide_courte = "la liste des choix scriptables"
        evt_selection.aide_longue = \
            "Cet évènement est appelé pour déterminer les choix possibles " \
            "que le joueur dans l'éditeur pourra sélectionner. Une " \
            "variable |ent|retour|ff| doit être créée dans cet évènement, " \
            "contenant une liste de chaînes. Le joueur dans l'éditeur " \
            "pourra choisir aucune, une ou plusieurs des valeurs se " \
            "trouvant dans cette liste. L'évènement 'valeurs' permet de " \
            "configurer de façon encore plus précise ce qui sera conservé " \
            "dans la structure."

        # Événement valeurs
        evt_valeurs = self.creer_evenement("valeurs")
        evt_valeurs.aide_courte = "la liste des valeurs correspondantes"
        evt_valeurs.aide_longue = \
            "Cet évènement est couplé à l'évènement 'selection' pour " \
            "déterminer les choix possibles et leur valeur respective. " \
            "Quand le joueur dans l'éditeur entrera l'un des choix " \
            "(une des chaînes contenues dans la liste de la variable " \
            "|ent|retour|ff| de l'évènement 'selection'), le système " \
            "recherchera la même case de la liste contenue dans la " \
            "variable |ent|retour|ff| de l'évènement 'valeurs'. Ainsi, " \
            "cet évènement doit contenir dans le même ordre que ''selection' " \
            "les valeurs correspondantes. Si 'selection' contient une liste " \
            "de noms de joueurs, l'évènement 'valeurs' doit contenir " \
            "la liste des joueurs correspondants dans le même ordre. " \
            "Quand le joueur dans l'éditeur entrera un nom de joueur, " \
            "la structure sera modifiée pour contenir le joueur (et " \
            "non pas son nom)."

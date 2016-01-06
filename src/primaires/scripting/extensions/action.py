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


"""Module contenant la classe Action, détaillée plus bas."""


from primaires.interpreteur.editeur.action import Action as EdtAction
from primaires.scripting.editeurs.edt_script import EdtScript
from primaires.scripting.extensions.base import Extension
from primaires.scripting.script import Script

class Action(Extension):

    """Classe représentant le type éditable 'action'.

    Ce type utilise l'éditeur Action. Au moment de l'exécution de
    l'action, l'éditeur redirige sur un script défini dans cette
    extension.

    """

    extension = "action"
    aide = "une action scriptable quittant l'éditeur"

    def __init__(self, structure, nom):
        Extension.__init__(self, structure, nom)
        self.script = ScriptAction(self)

    @property
    def editeur(self):
        """Retourne le type d'éditeur."""
        return EdtAction

    @property
    def arguments(self):
        """Retourne les arguments de l'éditeur."""
        return (self, "action")

    def creer(self, parent, structure):
        """Crée l'éditeur sur le modèle du parent."""
        enveloppe = parent.ajouter_choix(self.titre, self.raccourci,
                EdtAction, structure, self.nom, self, "action", structure)
        enveloppe.parent = parent
        return enveloppe

    def action(self, editeur, structure):
        """Active l'action."""
        personnage = getattr(editeur.pere, "joueur", None)
        if personnage:
            self.script["active"].executer(personnage=personnage,
                    structure=structure)

    def etendre_editeur(self, presentation):
        """Ëtend l'éditeur en fonction du type de l'extension."""
        # Script
        scripts = presentation.ajouter_choix("scripts", "sc", EdtScript,
                self.script)
        scripts.parent = presentation


class ScriptAction(Script):

    """Définition de l'action scriptable."""

    def init(self):
        """Initialisation du script."""
        # Événement active
        evt_active = self.creer_evenement("active")
        evt_active.aide_courte = "un personnage active ce menu"
        evt_active.aide_longue = \
            "Cet évènement est appelé quand le personnage dans " \
            "l'éditeur configuré édite le menu sélectionné. L'éditeur " \
            "est quitté à ce moment et une action particulière peut " \
            "être scriptée (changer le statut d'une structure, " \
            "l'effacer, envoyer un mudmail pour avertir un administrateur, " \
            "etc...). Aucun message n'est envoyé au joueur qui active " \
            "ce menu, c'est donc une des choses qui doit être scriptée " \
            "ici."

        # Configuration des variables de l'évènement active
        var_perso = evt_active.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage dans l'éditeur"
        var_structure = evt_active.ajouter_variable("structure", "Structure")
        var_structure.aide = "la structure éditée"

# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
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


"""Package contenant l'éditeur 'floatedit'.

Si des redéfinitions de contexte-éditeur standard doivent être faites, elles
seront placées dans ce package

Note importante : ce package contient la définition d'un éditeur, mais
celui-ci peut très bien être étendu par d'autres modules. Au quel cas,
les extensions n'apparaîtront pas ici.

"""

from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.description import Description
from primaires.salle.editeurs.redit.edt_details import EdtDetails

class EdtFloatedit(Presentation):

    """Classe définissant l'éditeur de description flottante 'floatedit'."""

    nom = "floatedit"

    def __init__(self, personnage, flottante):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None

        Presentation.__init__(self, instance_connexion, flottante)
        if personnage and flottante:
            self.construire(flottante)

    def __getnewargs__(self):
        return (None, None)

    def construire(self, flottante):
        """Construction de l'éditeur"""
        # Description
        description = self.ajouter_choix("description", "d", Description,
                flottante)
        description.parent = self
        description.apercu = "{objet.description.paragraphes_indentes}"
        description.aide_courte = \
            "| |tit|" + "Description flottante '{}'".format(
            flottante.cle).ljust(76) + "|ff||\n" + self.opts.separateur

        # Détails
        details = self.ajouter_choix("details", "e", EdtDetails, flottante,
                "details")
        details.parent = self
        details.aide_courte = \
            "Entrez le nom d'un |cmd|détail existant|ff| pour l'éditer ou " \
            "un |cmd|nouveau détail|ff|\n" \
            "pour le créer ; |ent|/|ff| pour revenir à la fenêtre parente.\n" \
            "Options :\n" \
            " - |ent|/s <détail existant> / <synonyme 1> (/ <synonyme 2> / " \
            "...)|ff| : permet\n" \
            "   de modifier les synonymes du détail passée en paramètre. " \
            "Pour chaque\n" \
            "   synonyme donné à l'option, s'il existe, il sera supprimé ; " \
            "sinon, il sera\n" \
            "   ajouté à la liste.\n" \
            " - |ent|/d <détail existant>|ff| : supprime le détail " \
            "indiqué\n\n"


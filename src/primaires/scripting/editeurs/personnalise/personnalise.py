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


"""Fichier contenant la classe EdtPersonnalise, détaillée plus bas."""

from textwrap import dedent

from primaires.interpreteur.editeur.description import Description
from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.uniligne import Uniligne

class EdtPersonnalise(Presentation):

    """Classe définissant l'éditeur personnalisé."""

    nom = "personnalise"

    def __init__(self, personnage, extension, attribut=""):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None

        Presentation.__init__(self, instance_connexion, extension,
                attribut, False)

        if personnage and extension:
            self.construire(extension)

    def __getnewargs__(self):
        return (None, None)

    def construire(self, extension):
        """Construction de l'éditeur"""
        # Nom
        nom = self.ajouter_choix("clé", "c", Uniligne, extension, "nom")
        nom.parent = self
        nom.prompt = "Clé de la case : "
        nom.apercu = "{valeur}"
        nom.aide_courte = dedent("""
            Entrez la |ent|clé|ff| de la case ou
            |cmd|/|ff| pour revenir à la fenêtre parente.

            |att|ATTENTION|ff| : si vous modifiez cette information, la
            case dans la structure créée à l'aide de cet éditeur sera
            également modifiée, ce qui pourrait poser des problèmes lors
            du traitement de la structure. En d'autres termes, ne modifiez
            cette valeur que si vous avez fait une erreur lors de la
            création de l'éditeur mais qu'aucune structure n'a encore
            été créée.

            Clé actuelle : |bc|{valeur}|ff|""".strip("\n"))

        # Titre
        titre = self.ajouter_choix("titre", "t", Uniligne, extension, "titre")
        titre.parent = self
        titre.prompt = "Titre du menu : "
        titre.apercu = "{valeur}"
        titre.aide_courte = \
            "Entrez le |ent|titre|ff| du menu ou |cmd|/|ff| pour revenir " \
            "à la fenêtre parente.\n\nTitre actuel : |bc|{valeur}|ff|"

        # Description
        description = self.ajouter_choix("aide", "a", Description, extension)
        description.parent = self
        description.apercu = "{objet.description.paragraphes_indentes}"
        description.aide_courte = \
            "| |tit|" + "Aide du menu".ljust(76) + "|ff||\n" + \
            self.opts.separateur

        # Aperçu
        apercu = self.ajouter_choix("aperçu", "p", Uniligne, extension,
                "apercu")
        apercu.parent = self
        apercu.prompt = "Aperçu du nenu : "
        apercu.apercu = "{valeur}"
        apercu.aide_courte = dedent("""
            Entrez |ent|l'aperçu|ff| du menu ou
            |cmd|/|ff| pour revenir à la fenêtre parente.

            L'aperçu est affiché dans l'éditeur parent, pour connaître
            la valeur sans avoir besoin d'entrer dans le menu. C'est
            généralement |cmd|$valeur|ff| qui sera remplacé par la
            valeur de l'élément modifiable par le menu. Vous n'aurez
            très probablement pas à modifier cette valeur, mais vous
            pourriez vouloir afficher une information complémentaire,
            comme par exemple l'unité (si vous demandez au joueur
            d'entrer des centimètres, vous pourriez écrire dans l'aperçu
            |cmd|$valeur cm|ff|).

            Aperçu actuel : |bc|{valeur}|ff|""".strip("\n"))

        # Raccourci
        raccourci = self.ajouter_choix("raccourci", "r", Uniligne, extension,
                "raccourci")
        raccourci.parent = self
        raccourci.prompt = "Raccourci du menu : "
        raccourci.apercu = "{valeur}"
        raccourci.aide_courte = dedent("""
            Entrez |ent|le raccourci|ff| du menu ou
            |cmd|/|ff| pour revenir à la fenêtre parente.

            Le raccourci est une suite de lettres permettant d'accéder
            au menu. Si ce champ est laissé à sa valeur par défaut
            (une valeur nulle), le système choisira tout seul un
            raccourci disponible. Le raccourci peut être constitué
            d'une ou plusieurs lettres, minuscules et sans accent,
            présentes dans le titre. Par exemple si le titre est
            |ent|description|ff|, le raccourci pourrait être |ent|d|ff|
            ou |ent|de|ff| ou |ent|cr|ff| car ces lettres ou combinaisons
            se trouvent dans le titre. Le raccourci ne pourrait pas
            être |ent|dsc|ff|, car |ent|ddescription|ff| ne comprend
            pas |ent|dsc|ff| à la suite. Enfin, il faut ajouter que
            si le raccourci a été utilisé par un autre menu dans le
            même éditeur, l'éditeur ne pourra être créé. Ainsi, de
            manière générale, si vous n'y accordez pas trop d'importanc,
            il est préférable de laisser le système s'occuper de ce
            détail, sauf si vous éditez un menu dont vous voulez absolument
            changer le raccourci. Si par exemple vous faites une
            action dans le menu |ent|supprimer|ff|, il peut êtr eutile
            de mettre un raccourci |ent|sup|ff| (qui sera plus long
            à entrer et évitera les suppressions involontaires).

            raccourci actuel : |bc|{valeur}|ff|""".strip("\n"))

        # Autres informations
        extension.etendre_editeur(self)

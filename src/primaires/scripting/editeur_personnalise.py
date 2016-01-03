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


"""Fichier contenant la classe EditeurPersonnalise, détaillée plus bas."""

from abstraits.obase import *
from primaires.format.fonctions import supprimer_accents
from primaires.scripting.editeurs.personnalise import EdtEditeur
from primaires.scripting.extensions import EXTENSIONS

class EditeurPersonnalise(BaseObj):

    """Classe contenant un éditeur personnalisé.

    Un éditeur personnalisé, tout comme une commande dynamique, permet
    de créer des éditeurs dynamiques, définis dans l'univers, au
    lieu de les définir de façon statique dans le code. Ces éditeurs
    peuvent ensuite être appelés par scripting et remplis par des
    personnages. Ces éditeurs sont scriptables de point en point.

    Un éditeur personnalisé se présente par défaut comme une
    présentation (voir primaires.interpreteur.editeur.presentation).
    Dans cette présentation peuvent être ajoutés différents types
    d'éditeurs, dont certains peuvent être des présentations, créant
    ainsi une véritable hiérarchie. Le mécanisme scripting derrière
    ce système peut se résumer ainsi :

        1.  Une structure vide du bon type est créée :
            journal = creer_structure("journal")
        2.  La structure peut être optionnellement modifiée :
            ecrire structure "titre" "Le titre de ce journal"
            date = date()
            ecrire structure "date_creation" date
            ...
        3.  On demande de créer et afficher un éditeur pour cette structure :
            editer personnage structure
        4.  Le reste du mécanisme est contenu dans les scripts de
            l'éditeur.

    Pour plus d'informations, voir la page d'aide consacrée :
    http://redmine.kassie.fr/projects/documentation/wiki/EditeurPersonnalise

    """

    enregistrer = True

    def __init__(self, structure):
        """Constructeur d'un éditeur personnalisé."""
        BaseObj.__init__(self)
        self.structure = structure
        self.editeurs = []
        self._construire()

    def __getnewargs__(self):
        return ("inconnue", )

    def __repr__(self):
        return "<EditeurPersonnalise {}>".format(repr(self.structure))

    def __str__(self):
        return self.structure

    def ajouter_editeur(self, attribut, nom_type):
        """Ajoute un sous-éditeur, c'est-à-dire une extension."""
        classe = None
        nom_type = supprimer_accents(nom_type).lower()
        for nom, extension in EXTENSIONS.items():
            if nom == nom_type:
                classe = extension
                break

        if classe is None:
            raise ValueError("Type inconnu : {}".format(repr(nom_type)))

        extension = classe(self.structure, attribut)
        self.editeurs.append(extension)
        return extension

    def editer(self, personnage, structure):
        """Fait éditer le personnage."""
        editeur = EdtEditeur(personnage, self, structure)
        personnage.contextes.ajouter(editeur)
        editeur.actualiser()

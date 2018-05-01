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


"""Fichier contenant l'éditeur présentation pour editeur/editor.."""

from primaires.interpreteur.editeur.flag import Flag
from primaires.interpreteur.editeur.presentation import Presentation
from primaires.scripting.editeurs.personnalise.editeurs import EdtEditeurs

class EdtPresentation(Presentation):

    """Classe définissant l'éditeur de présentation."""

    nom = "editeur"

    def __init__(self, personnage, editeur, attribut=None):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None

        Presentation.__init__(self, instance_connexion, editeur)
        if personnage and editeur:
            self.construire(editeur)

    def __getnewargs__(self):
        return (None, None, None)

    def construire(self, editeur):
        """Construction de l'éditeur"""
        # Éditeurs
        editeurs = self.ajouter_choix("éditeurs", "t", EdtEditeurs, editeur)
        editeurs.parent = self

        # Afficher quitter
        quitter = self.ajouter_choix("afficher le menu quitter", "a",
                Flag, editeur, "afficher_quitter")
        quitter.parent = self

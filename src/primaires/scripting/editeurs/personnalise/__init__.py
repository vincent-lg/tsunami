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


"""Package contenant l'éditeur d'éditeur personnalisé."""

from primaires.interpreteur.editeur.presentation import Presentation
from primaires.scripting.editeurs.personnalise import personnalise
from primaires.scripting.editeurs.personnalise import presentation

class EdtEditeur(Presentation):

    """Classe définissant l'éditeur d'éditeur personnalisé."""

    def __init__(self, personnage, editeur, structure, quitter=None):
        """Constructeur de l'éditeur"""
        if hasattr(personnage, "instance_connexion"):
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = personnage

        if quitter is None:
            quitter = True
            if editeur:
                quitter = editeur.afficher_quitter

        Presentation.__init__(self, instance_connexion, editeur, None, quitter)
        if personnage and editeur and structure:
            self.construire(editeur, structure)

    def __getnewargs__(self):
        return (None, None, None)

    def construire(self, editeur, structure):
        """Construction de l'éditeur"""
        for sous_editeur in editeur.editeurs:
            sous_editeur.creer(self, structure)

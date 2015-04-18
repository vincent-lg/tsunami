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


"""Module contenant l'éditeur d'ateliers de guilde."""

from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.uniligne import Uniligne

class GldAtelierEdit(Presentation):

    """Classe définissant l'éditeur d'ateliers."""

    nom = "gldedit:atelier"

    def __init__(self, personnage, atelier, attribut):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None

        Presentation.__init__(self, instance_connexion, atelier, None, False)
        if personnage and atelier:
            self.construire(atelier)

    def __getnewargs__(self):
        return (None, None)

    def construire(self, atelier):
        """Construction de l'éditeur"""
        # Nom
        nom = self.ajouter_choix("nom", "n", Uniligne, atelier, "nom")
        nom.parent = self
        nom.prompt = "Nom de la atelier : "
        nom.apercu = "{valeur}"
        nom.aide_courte = \
            "Entrez le |ent|nom|ff| de l'atelier ou |cmd|/|ff| pour " \
            "revenir à la fenêtre parente.\n\nNom actuel : " \
            "|bc|{valeur}|ff|"

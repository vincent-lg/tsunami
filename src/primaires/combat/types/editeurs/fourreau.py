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


"""Module contenant l'éditeur de fourreau."""

from primaires.interpreteur.editeur.flag import Flag
from primaires.interpreteur.editeur.flottant import Flottant
from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.selection import Selection
from primaires.objet.types import types

class EdtFourreau(Presentation):

    """Classe définissant l'éditeur de fourreau."""

    def __init__(self, instance_connexion, prototype, attribut=""):
        """Constructeur de l'éditeur"""
        Presentation.__init__(self, instance_connexion, prototype, "", False)
        if instance_connexion and prototype:
            self.construire(prototype)

    def __getnewargs__(self):
        return (None, None)

    def construire(self, armure):
        """Construction de l'éditeur"""
        # Fourreau
        fourreau = self.ajouter_choix("fourreau", "f", Flag, armure,
                "fourreau")
        fourreau.parent = self

        # Visible dans le nom
        visible = self.ajouter_choix("visible dans le nom", "v", Flag,
                armure, "fourreau_visible")
        visible.parent = self

        # Poids maximum
        poids_max = self.ajouter_choix("poids maximum de l'arme au fourreau",
                "p", Flottant, armure, "poids_max_fourreau")
        poids_max.parent = self
        poids_max.apercu = "{objet.poids_max_fourreau} kg"
        poids_max.prompt = "Poids maximum de l'arme au fourreau : "
        poids_max.aide_courte = \
            "Entrez le poids maximum, en kilos, de l'arme qui pourra\n" \
            "être contenue dans ce fourreau.\n\nPoids maximum actuel : " \
            "{objet.poids_max_fourreau}"

        # Types admis
        possibles = sorted(list(types["arme"].types.keys()))
        types_f = self.ajouter_choix("types admis", "t", Selection, armure,
                "types_fourreau", possibles)
        types_f.parent = self
        types_f.apercu = "{objet.str_types_fourreau}"
        types_f.aide_courte = \
            "Entrez les différents |ent|types admis|ff| de ce fourreau " \
            "ou |cmd|/|ff| pour revenir à la\n" \
            "fenêtre parente. Pour ajouter un |ent|type admis|ff|, entrez " \
            "son nom. Si il est déjà\n" \
            "dans la liste, il sera ajouté. Sinon, il sera retiré.\n" \
            "Types possibles : {}\nTypes admis actuels : " \
            "{{objet.str_types_fourreau}}".format(", ".join(possibles))

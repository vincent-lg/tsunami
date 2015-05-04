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


"""Module contenant l'éditeur de types de guilde."""

from primaires.interpreteur.editeur.aes import AES
from primaires.interpreteur.editeur.presentation import Presentation

class GldTypeEdit(Presentation):

    """Classe définissant l'éditeur de types."""

    nom = "gldedit:type"

    def __init__(self, personnage, type, attribut=None):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None

        Presentation.__init__(self, instance_connexion, type, None, False)
        if personnage and type:
            self.construire(type)

    def __getnewargs__(self):
        return (None, None)

    def construire(self, type):
        """Construction de l'éditeur"""
        # Attributs
        attributs = self.ajouter_choix("attributs", "a", AES,
                type, "attributs", None, (("nom", "chaîne"), ),
                None, "ajouter_attribut", "supprimer_attribut")
        attributs.parent = self
        attributs.apercu = "{valeur}"
        attributs.aide_courte = \
            "Entrez |cmd|/|ff| pour revenir à la fenêtre parente ou :\n" \
            " |ent|/a <nom de l'attribut à créer>|ff|\n" \
            " |ent|/s <nom de l'attribut à supprimer>|ff|\n\n" \
            "Attributs actuels :{valeur}"

        # Extensions
        extensions = self.ajouter_choix("extensions de l'éditeur 'oedit'",
                "e", AES, type, "extensions", "gldedit:extension",
                (("nom", "chaîne"), ("type", "chaîne")),
                "get_extension", "ajouter_extension", "supprimer_extension",
                "nom_complet")
        extensions.parent = self
        extensions.apercu = "{valeur}"
        extensions.aide_courte = \
            "Entrez |ent|le nom de l'extension|ff| pour l'éditer ou :\n" \
            " |ent|/a <nom de l'extension à ajouter / type>|ff|\n" \
            " |ent|/s <nom de l'extension à supprimer>|ff|\n\n" \
            "Les types d'extension possibles sont :\n" \
            "    chaîne (une chaîne de caractères sans contrainte)\n" \
            "    entier (un nombre entier sans contrainte)\n" \
            "    entier positif / négatif / positif ou nul / " \
            "négatif ou nul\n" \
            "    entier entre X et Y\n" \
            "    tableau avec les colonnes nom (type), nom2 (type2)...\n\n" \
            "Exemples de types :\n" \
            "    entier positif ou nul\n" \
            "    entier entre 5 et 32\n" \
            "    tableau avec les colonnes nom (chaîne), âge (entier)\n\n" \
            "Extensions actuelles :{valeur}"

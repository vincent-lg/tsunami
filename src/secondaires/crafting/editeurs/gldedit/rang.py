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


"""Module contenant l'éditeur de rangs de guilde."""

from primaires.interpreteur.editeur.aes import AES
from primaires.interpreteur.editeur.entier import Entier
from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.uniligne import Uniligne

class GldRangEdit(Presentation):

    """Classe définissant l'éditeur de rangs."""

    nom = "gldedit:rang"

    def __init__(self, personnage, rang, attribut=None):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None

        Presentation.__init__(self, instance_connexion, rang, None, False)
        if personnage and rang:
            self.construire(rang)

    def __getnewargs__(self):
        return (None, None)

    def construire(self, rang):
        """Construction de l'éditeur"""
        # Nom
        nom = self.ajouter_choix("nom", "n", Uniligne, rang, "nom")
        nom.parent = self
        nom.prompt = "Nom du rang : "
        nom.apercu = "{valeur}"
        nom.aide_courte = \
            "Entrez le |ent|nom|ff| du rang ou |cmd|/|ff| pour " \
            "revenir à la fenêtre parente.\n\nNom actuel : " \
            "|bc|{valeur}|ff|"

        # Points de guilde
        points = self.ajouter_choix("points de guilde nécessaires", "p",
                Entier, rang, "points_guilde", 1)
        points.parent = self
        points.apercu = "{valeur} points"
        points.prompt = "Points de guilde nécessaires pour rejoindre " \
                "ce rang : "
        points.aide_courte = \
            "Entrez |ent|le nombre de points|ff| de guilde nécessaires " \
            "ou |cmd|/|ff| pour revenir\nà la fenêtre parente.\n\n" \
            "Points actuels : {valeur}"

        # Recettes
        recettes = self.ajouter_choix("recettes", "r", AES,
                rang, "recettes", "gldedit:recette", (("resultat", "clé"), ),
                "get_recette", "ajouter_recette", "supprimer_recette", "description")
        recettes.parent = self
        recettes.apercu = "{valeur}"
        recettes.aide_courte = \
            "Entrez la clé d'une recette pour l'éditer ou :\n" \
            " |ent|/a <clé de l'objet résultat de la recette à créer>|ff|\n" \
            " |ent|/s <clé de la recette à supprimer>|ff|\n\n" \
            "Recettes actuelles :{valeur}"

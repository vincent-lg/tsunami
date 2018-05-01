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


"""Module contenant l'éditeur de talents de guilde."""

from primaires.interpreteur.editeur.flag import Flag
from primaires.interpreteur.editeur.flottant import Flottant
from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.uniligne import Uniligne

class GldTalentEdit(Presentation):

    """Classe définissant l'éditeur de talents."""

    nom = "gldedit:talent"

    def __init__(self, personnage, talent, attribut=None):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None

        Presentation.__init__(self, instance_connexion, talent, None, False)
        if personnage and talent:
            self.construire(talent)

    def __getnewargs__(self):
        return (None, None)

    def construire(self, talent):
        """Construction de l'éditeur"""
        # Nom
        nom = self.ajouter_choix("nom", "n", Uniligne, talent, "nom")
        nom.parent = self
        nom.prompt = "Nom du talent : "
        nom.apercu = "{valeur}"
        nom.aide_courte = \
            "Entrez le |ent|nom|ff| du talent ou |cmd|/|ff| pour " \
            "revenir à la fenêtre parente.\n\nÀ la différence de " \
            "la clé de talent, vous pouvez modifier le nom\nsans " \
            "inconvénients, même après l'ouverture du talent aux " \
            "joueurs.\n\nNom actuel : |bc|{valeur}|ff|"

        # Difficulté
        difficulte = self.ajouter_choix("difficulté", "d", Flottant, talent,
                "difficulte")
        difficulte.parent = self
        difficulte.prompt = "Difficulté du talent : "
        difficulte.apercu = "{valeur}%"
        difficulte.aide_courte = \
            "Entrez la |ent|difficulté|ff| du talent ou |cmd|/|ff| pour " \
            "revenir à la fenêtre parente.\n\nLa difficulté est " \
            "un pourcentage indiquant à quel point il est\nfacile " \
            "d'apprendre un talent. Plus le pourcentage est élevé,\nplus " \
            "apprendre le talent est facile. La plupart des talents " \
            "configurés\nont une difficulté entre |ent|20|ff| et " \
            "|ent|40|ff|. En fonction\ndu nombre de fois où la pratique " \
            "se produit, mieux vaut tester pour\nse faire une meilleure " \
            "idée.\nVous pouvez entrer un nombre à virgule.\n\nDifficulté " \
            "actuelle : |bc|{valeur}|ff|%"

        # Ouvert
        ouvert = self.ajouter_choix("ouvert", "o", Flag, talent,
                "ouvert")
        ouvert.parent = self

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


"""Fichier contenant le type Recette."""

from bases.objet.attribut import Attribut
from primaires.format.description import Description
from primaires.interpreteur.editeur.description import Description as EdtDesc
from primaires.interpreteur.editeur.uniligne import Uniligne, LOWER
from primaires.objet.types.base import BaseType

class Recette(BaseType):

    """Type d'objet : recette de cuisine.

    Ce type d'objet permet de conserver une recette de cuisine sur
    un parchemin par exemple. En plus des attributs habituels, la
    recette de cuisine possède un nom (le ragoût de lapin)
    et un contenu.

    """

    nom_type = "recette"

    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        BaseType.__init__(self, cle)
        self.nom_recette = "la recette de quelque chose"
        self.contenu = Description(parent=self, scriptable=False)

        # Éditeurs
        self.etendre_editeur("o", "nom de la recette", Uniligne, self,
                "nom_recette", 0, LOWER)
        self.etendre_editeur("c", "contenu de la recette", EdtDesc, self,
                "contenu")

    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes"""
        contenu = enveloppes["c"]
        contenu.aide_courte = \
            "| |tit|" + "Contenu de la recette {}".format(self.cle).ljust(
            76) + "|ff||\n" + "-" * 79

        nom = enveloppes["o"]
        nom.apercu = "{valeur}"
        nom.prompt = "Nom de la recette"
        nom.aide_courte = \
            "Entrez |ent|le nom de la recette|ff| ou |cmd|/|ff| pour " \
            "revenir à la fenêtre parente.\n\n" \
            "Choisissez le nom de la recette avec article (par exemple,\n" \
            "|ent|le poulet farci aux chatâignes|ff|).\n\n"\
            "Nom actuel : {objet.nom_recette}"

    def regarder(self, personnage):
        """Le personnage regarde l'objet."""
        prototype = getattr(self, "prototype", self)
        variables = {
            "recette": prototype.nom_recette,
            "RECETTE": prototype.nom_recette.upper(),
            "Recette": prototype.nom_recette.capitalize(),
            "contenu": prototype.contenu.regarder(personnage, self),
        }
        BaseType.regarder(self, personnage, variables)

    def get_structure(self, structure):
        """Retourne la structure étenduee."""
        BaseType.get_structure(self, structure)
        structure.nom_recette = self.nom_recette
        structure.contenu = self.contenu.regarder(None, self)

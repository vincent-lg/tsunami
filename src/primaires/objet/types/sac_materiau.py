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


"""Fichier contenant le type SacMateriau."""

from bases.objet.attribut import Attribut
from primaires.interpreteur.editeur.flottant import Flottant
from primaires.interpreteur.editeur.selection import Selection
from primaires.interpreteur.editeur.uniligne import Uniligne
from .base import BaseType

class SacMateriau(BaseType):

    """Type d'objet: sac de materiau.

    Les sacs de matériau sont des conteneurs spéciaux pour les
    matières premières qu'on ne peut manipuler à la main. Ce ne
    sont pas nécessairement des sacs, mais ds conteneurs plus
    génériques (comme des jarres, des tonneaux ou autre). Chaque
    prototype peut définir le ou les types de matériau qu'il pourra
    accepter.

    """

    nom_type = "sac de matériau"

    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        BaseType.__init__(self, cle)
        self.materiaux_admis = []
        self.poids_max = 10
        self.connecteur = "de"
        self.etendre_editeur("t", "matériaux admis", Selection, self,
                "materiaux_admis", importeur.objet.get_types_herites(
                "matériau"))
        self.etendre_editeur("x", "poids max", Flottant, self, "poids_max")

        # Attributs propres à l'objet (non au prototype)
        self._attributs = {
            "materiau": Attribut(),
            "quantite": Attribut(),
        }

    def get_nom(self, nombre=1, pluriels=True):
        """Retourne le nom complet en fonction du nombre.

        Par exemple :
        Si nombre == 1 : retourne le nom singulier
        Sinon : retourne le nombre et le nom pluriel

        """
        ajout = ""
        if hasattr(self, "materiau"):
            materiau = self.materiau
            quantite = self.quantite
            ajout = " {} {}".format(self.connecteur, materiau.get_nom(
                    quantite))

        if nombre <= 0:
            raise ValueError("la fonction get_nom a été appelée " \
                    "avec un nombre négatif ou nul.")
        elif nombre == 1:
            return self.nom_singulier + ajout
        else:
            return "{} {}{}".format(nombre, self.nom_pluriel, ajout)

    def calculer_poids(self):
        """Retourne le poids de l'objet et celui des objets contenus."""
        poids = self.poids_unitaire
        if self.materiau and self.quantite:
            poids += self.materiau.poids * self.quantite

        return round(poids, 3)

    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes"""
        materiaux_admis = enveloppes["t"]
        materiaux_admis.apercu = "{valeur}"
        materiaux_admis.aide_courte = \
            "Entrez les différents |ent|matériaux admis|ff| de ce sac " \
            "de matériau ou\n|cmd|/|ff| pour revenir à la" \
            "fenêtre parente. Pour ajouter un |ent|matériau admis|ff|, entrez " \
            "son nom. Si il est déjà\n" \
            "dans la liste, il sera ajouté. Sinon, il sera retiré.\n" \
            "Matériaux admis actuels : {valeur}"

        poids_max = enveloppes["x"]
        poids_max.apercu = "{valeur} kg"
        poids_max.prompt = "Poids max du sac de matériau : "
        poids_max.aide_courte = \
            "Entrez le |ent|poids maximum|ff| du sac de matériau ou " \
            "|cmd|/|ff| pour revenir à la fenêtre parente.\n\n" \
            "Poids maximum actuel : {valeur} kg"

    # Actions sur les objets
    def regarder(self, personnage):
        """Le personnage regarde l'objet"""
        variables = {"contenu": ""}
        if self.materiau and self.materiau.quantite:
            variables["contenu"] = self.nom_singulier.capitalize() + \
                    " contient " + self.materiau.get_nom(self.quantite) + "."

        return BaseType.regarder(self, personnage, variables)

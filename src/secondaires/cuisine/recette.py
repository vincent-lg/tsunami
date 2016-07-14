# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 NOEL-BARON Léo
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


"""Ce fichier contient la classe Recette, détaillée plus bas."""

from abstraits.obase import BaseObj

class Recette(BaseObj):

    """Classe définissant une recette de cuisine.

    Une recette est définie par sa difficulté, la liste des ingrédients qui
    la composent ainsi que leurs quantités relatives, et un prototype d'objet
    obtenu à son terme.

    """

    enregistrer = True

    def __init__(self, cle):
        """Constructeur d'un rapport."""
        BaseObj.__init__(self)
        self.cle = cle
        self.difficulte = 10
        self.temps_cuisson = 10
        self.cuisson = "moyen"
        self.ustensiles = ["casserole"]
        self.ingredients = {}
        self.resultat = None

    def __getnewargs__(self):
        return ("", )

    def __repr__(self):
        resultat = self.resultat.cle if self.resultat else "rien"
        return "<recette {} (donne {})>".format(self.cle, resultat)

    def __str__(self):
        return self.cle

    @property
    def cuisinable(self):
        return self.ingredients and self.resultat

    @property
    def feu_mini(self):
        forces = {
                "doux": 5,
                "moyen": 10,
                "vif": 25,
        }

        return forces[self.cuisson]

    @property
    def feu_maxi(self):
        return {"doux":15, "moyen":30, "vif":40}[self.cuisson]

    @property
    def aff_ingredients(self):
        """Affichage sommaire des ingrédients"""
        ret = []
        for ing, qtt in self.ingredients.items():
            ret.append("{} ({})".format(ing.get_nom(qtt), ing.cle))
        return "\n    " + "\n    ".join(ret) if ret else ""

    @property
    def aff_ustensiles(self):
        """Affichage sommaire des ustensiles admis"""
        return ", ".join(self.ustensiles)

    @property
    def aff_resultat(self):
        """Affichage du résultat"""
        return "{} ({})".format(self.resultat.nom_singulier,
                self.resultat.cle) if self.resultat else "rien"

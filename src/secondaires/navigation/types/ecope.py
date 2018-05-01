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


"""Fichier contenant le type ecope."""

from bases.objet.attribut import Attribut
from primaires.interpreteur.editeur.flottant import Flottant
from primaires.objet.types.base import BaseType

class Ecope(BaseType):

    """Type d'objet: écope.

    """

    nom_type = "écope"
    nettoyer = False
    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        BaseType.__init__(self, cle)
        self.poids_max = 5.0
        self.etendre_editeur("ma", "poids maximum", Flottant,
                self, "poids_max")

    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes"""
        poids_max = enveloppes["ma"]
        poids_max.prompt = "Poids maximum de l'écope : "
        poids_max.aide_courte = \
            "Entrez le |ent|poids maximum|ff| en kg " \
            "de l'écope.\n" \
            "Entrez |cmd|/|ff| pour revenir à la fenêtre " \
            "parente.\n\n" \
            "Poids maximum actuel : {objet.poids_max} kg"

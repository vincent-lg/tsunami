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


"""Fichier contenant le type calfeutrage."""

from bases.objet.attribut import Attribut
from primaires.interpreteur.editeur.flag import Flag
from primaires.interpreteur.editeur.entier import Entier
from primaires.objet.types.base import BaseType

class Calfeutrage(BaseType):

    """Type d'objet: calfeutrage.

    """

    nom_type = "calfeutrage"
    nettoyer = False
    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        BaseType.__init__(self, cle)
        self.onces_max_contenu = 50
        self.etendre_editeur("on", "nombre d'onces au maximum", Entier,
                self, "onces_max_contenu")

        # Attributs propres à l'objet (non au prototype)
        self._attributs = {
            "onces_contenu": Attribut(lambda: self.onces_max_contenu),
        }

    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes"""
        contenu = enveloppes["on"]
        contenu.apercu = "{objet.onces_max_contenu}"
        contenu.prompt = "Nombre maximum d'onces que peut contenir le " \
                "conteneur : "
        contenu.aide_courte = \
            "Entrez le |ent|contenu|ff| en onces " \
            "du conteneur pour calfeutrer.\n" \
            "Entrez |cmd|/|ff| pour revenir à la fenêtre " \
            "parente.\n\n" \
            "Onces maximum actuelles : {objet.onces_max_contenu}"

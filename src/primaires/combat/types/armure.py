# -*-coding:Utf-8 -*

# Copyright (c) 2013 LE GOFF Vincent
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


"""Fichier contenant le type armure."""

from random import randint

from primaires.interpreteur.editeur.entier import Entier
from primaires.objet.types.base import BaseType

class Armure(BaseType):

    """Type d'objet: armure.

    Ce type est une classe-mère des armuers spécifiques (casque,
    cotte de mailles...).

    """

    nom_type = "armure"

    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        BaseType.__init__(self, cle)
        self.empilable_sur = ["vêtement"]
        self.encaissement_fixe = 5
        self.encaissement_variable = 0

        # Editeurs
        self.etendre_editeur("f", "encaissement fixe", Entier, self,
                "encaissement_fixe")
        self.etendre_editeur("v", "encaissement variable", Entier, self,
                "encaissement_variable")

    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes"""
        fixe = enveloppes["f"]
        fixe.apercu = "{objet.encaissement_fixe}"
        fixe.prompt = "Encaissement fixe de l'armure : "
        fixe.aide_courte = \
            "Entrez l'|ent|encaissement fixe|ff| de l'armure. Il " \
            "représente\nla quantité de dégâts fixes que l'armure peut " \
            "encaisser.\nÀ cet encaissement s'ajoute l'encaissement " \
            "variable. Si les\ndégâts dépassent l'encaissement de l'armure, " \
            "l'armure n'encaisse\nque ce qu'elle a été configurée pour " \
            "et le personnage derrière\nreçoit les dégâts compensés. Si " \
            "les dégâts sont inférieurs à\nl'enciassement de l'armure, " \
            "le personnage ne reçoit rien.\n\n" \
            "Encaissement fixe actuel : {objet.encaissement_fixe}"

        variable = enveloppes["v"]
        variable.apercu = "{objet.encaissement_variable}"
        variable.prompt = "Encaissement variable de l'armure : "
        variable.aide_courte = \
            "Entrez l'|ent|encaissement variable|ff| de l'armure. Il " \
            "représente\nla partie variable de l'encaissement global, " \
            "celui-ci étant\nl'encaissement fixe plus l'encaissement " \
            "variable déterminé aléatoirement,\nentre |ent|0|ff| et " \
            "l'encaissement variable configuré. Une armure\navec un " \
            "encaissement fixe de |ent|5|ff| et des dégâts variables de " \
            "|ent|2|ff|\naura un encaissement entre |ent|5|ff| et " \
            "|ent|7|ff|.\n\nEncaissement variable actuel : " \
            "{objet.encaissement_variable}"

    def encaisser(self, personnage, arme, degats):
        """Retourne les dégâts en tenant compte de l'encaissement.

        La stat 'robustesse' du personnage est utilisée pour estimer
        à quel point l'armure protège le membre (pour la robustesse est
        élevée, plus la protection est importante).

        """
        if degats <= 1:
            return 0

        taux = 0.5 + personnage.stats.robustesse / 200
        encaissement = self.encaissement_fixe
        if self.encaissement_variable > 0:
            encaissement = randint(self.encaissement_fixe,
                    self.encaissement_fixe + self.encaissement_variable)

        encaissement = int(taux * encaissement)
        if encaissement > degats - 1:
            encaissement = degats - 1

        return encaissement

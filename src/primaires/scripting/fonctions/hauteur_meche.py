# -*-coding:Utf-8 -*

# Copyright (c) 2014 LE GOFF Vincent
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


"""Fichier contenant la fonction hauteur_meche."""

from fractions import Fraction

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Renvoie la hauteur de la mèche (en pourcent)."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.hauteur_meche, "Objet")
        cls.ajouter_types(cls.prototype_hauteur_meche, "PrototypeObjet")

    @staticmethod
    def hauteur_meche(objet):
        """Retourne la hauteur de la mèche entre 1 et 100.

        Paramètres à préciser :

          * objet : l'objet (type objet lumière)

        Cette fonction retourne la hauteur de la mèche en pourcent.
        Une lumière qui n'a pas du tout brûlée est à 100. Une
        lumière qui n'a plus de mèche (ne peut plus brûler) est à
        0. Quand une lampe est allumée, sa mèche descend
        généralement. On parle ici de mèche, mais bien sûr cela
        dépend de la lumière (ce peut être une torche, une lampe ou
        même quelque chose de magique qui n'a pas de mèche).

        Exemple d'utilisation :

          hauteur = hauteur_meche(objet)
          si hauteur = 100:
              dire personnage "Cette torche est intacte et n'a jamais servie."
          sinon si hauteur > 80:
              dire personnage "Cette torche est à peine brûlée." longtemps."
          sinon si hauteur > 60:
              dire personnage "Cette torche n'est pas encore à moitié brûlée."
          sinon si hauteur > 40:
              dire personnage "Cette torche est à moitié brûlée."
          ...
          sinon si hauteur = 0:
              # Note : cela ne se produit que quand la torche est
              # éteinte et ne peut être rallumée
              dire personnage "Cette torche est fichue, passez à la suivante."
          finsi

        """
        if not objet.est_de_type("lumière"):
            raise ErreurExecution("L'objet {} n'est pas une lumière.".format(
                    objet.identifiant))

        return Fraction(100 - (objet.duree_en_cours() / objet.duree_max * \
                100))

    @staticmethod
    def prototype_hauteur_meche(prototype):
        """Retourne invariablement 100.

        Cette fonction est simplement utilisée pour la compatibilité
        avec l'objet. Quand on examine le prototype, la mèche doit
        être intacte.

        """
        return Fraction(100)

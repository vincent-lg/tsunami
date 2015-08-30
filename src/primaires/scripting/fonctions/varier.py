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


"""Fichier contenant la fonction varier."""

from fractions import Fraction

from corps.aleatoire import varier
from primaires.scripting.fonction import Fonction

class ClasseFonction(Fonction):

    """Fait varier le nombre précisé aléatoirement."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.varier, "Fraction", "Fraction")

    @staticmethod
    def varier(base, marge):
        """Fait varier un nombre en fonction d'une marge.

        Le nombre précisée est la base. La marge renseigne la
        différence entre la base et la valeur minimum, d'une part,
        la base et la valeur maximum de l'autre. Ce peut sembler
        un peu dur à expliquer, mais voici un exemple qui rendra
        la chose limpide :
            varier(100, 20) -- retourne un nombre entre 80 et 120
        Consulter les exemples ci-dessous pour plus d'informations.
        La marge peut être inférieure à 1. Dans ce cas, elle représente
        un pourcentage de la base :
            varier(200, 0,1) -- retourne entre 180 et 220

        Paramètres à préciser :

          * base : la base (un nombre)
          * marge : la marge (un nombre)

        Exemples d'utilisation :

          # Retourne entre 800 et 1200
          nombre = varier(1000, 200)
          # Retourne entre 900 et 1100
          nombre = varier(1000, 0,1)
          # Retourne entre 99 et 101
          nombre = varier(100, 0,01)
          # Préciser un nombre à virgule inférieur à 1 est utile si
          # vous ne connaissez pas l'ordre de grandeur de la base
          # (par exemple pour faire varier l'XP à donner au joueur).

        """
        if marge < 1:
            marge = float(marge)
            marge = int(base * marge)

        variation = varier(int(base), int(marge), None)
        return Fraction(variation)

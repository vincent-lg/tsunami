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


"""Fichier contenant la fonction nombre."""

from fractions import Fraction

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Renvoie le nombre converti."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.nombre, "str")

    @staticmethod
    def nombre(chaine):
        """Retourne le nombre converti.

        Paramètres à entrer :

          * chaine : la chaîne contenant le nombre

        Cette fonction est simple : elle prend en paramètre une
        chaîne de caractères et retourne le nombre correspondant.
        Il est généralement inutile de convertir une chaîne en nombre,
        sauf dans certains cas précis : par exemple, si le joueur dit
        quelque chose contenant un nombre et que ce nombre est nécessaire
        à un certain traitement, il peut être nécessaire de le
        convertir.

        Exemple simple :

          chaine = "32"
          nombre = nombre(chaine)
          # nombre contiendra 32

        """
        try:
            return Fraction(chaine)
        except ValueError:
            raise ErreurExection("Le nombre {} n'a pas pu être " \
                    "converti".format(repr(chaine)))

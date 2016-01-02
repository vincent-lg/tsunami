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


"""Fichier contenant la fonction indice."""

from fractions import Fraction

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Renvoie l'indice de la donnée dans la liste."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.liste, "object", "list")

    @staticmethod
    def liste(element, liste):
        """Renvoie l'indice de l'élément dans la liste.

        Cette fonction retourne l'indice, c'est-à-dire la position
        (le numéro de la case) dans lequel l'élément transmis est
        conservé dans la liste. Voyez ci-dessous pour des exemples.
        Veillez bien à utiliser le même élément : si l'élément n'est
        pas trouvé dans la liste, une alerte est créée.

        Paramètres à préciser :

          * element : l'élément (le type veut varier)
          * liste : la liste dans laquelle chercher.

        Exemples d'utilisation :

          animaux = liste("canard", "chien", "grenouille", "chameau", "parapluie")
          # J'aime bien les parapluies
          nombre = indice("canard", animaux)
          # nombre contient à présent 1 (première case de la liste)
          nombre = indice("chameau", animaux)
          # nombre contient 4 (la quatrième case de la liste)

        """
        if element in liste:
            return Fraction(liste.index(element) + 1)
        else:
            raise ErreurExecution("L'élément {} n'est pas présent " \
                    "dans cette liste".format(repr(element)))

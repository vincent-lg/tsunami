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


"""Fichier contenant la fonction correspond."""

import re

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution
from primaires.format.fonctions import supprimer_accents

class ClasseFonction(Fonction):

    """Test si une chaîne correspond à une expression régulière."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.correspond, "str", "str")

    @staticmethod
    def correspond(expression, chaine):
        """Retourne vrai si la chaine correspond à l'expression.

        Paramètres à préciser :

          * expression : l'expression régulière
          * chaine : la chaîne à tester

        On retire les accents de la chaîne avant de la tester. Ainsi :

          correspond("^[a-z]+$", "tête")

        Retournera VRAI, car le ê est remplacé par un e
        standard. De plus, les majuscules ou minuscules n'ont pas
        d'importance dans la recherche.

        Pour plus d'informations sur les expressions régulirèes, rendez-vous
        [[regex|sur cette page d'aide]].

        """
        chaine = supprimer_accents(chaine)
        expression = expression.replace("_b_", "|")
        try:
            return re.search(expression, chaine, re.I)
        except re.error as err:
            raise ErreurExecution("Syntaxe de l'expression régulière " \
                    "invalide : " + str(err))

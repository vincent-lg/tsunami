# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Fichier contenant la fonction expression."""

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution
from primaires.format.fonctions import supprimer_accents

class ClasseFonction(Fonction):

    """Test si une chaîne correspond à une expression.

    L'expression est une ou plusieurs chaînes de test. La chaîne testée
    l'est indépendemment de sa ponctuation, ses majuscules ou minuscules
    ou ses accents.

    """
    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.expression, "str", "str")

    @staticmethod
    def expression(chaine, expression):
        """Retourne vrai si la chaine  se retrouve dans expression.

        L'expression est une chaîne sous la forme :
            "bonjour" pour représenter l'expression bonjour
            "bonjour|salut" retourne vrai si la chaîne est bonjour ou salut

        Le test ne tient pas compte de la ponctuation, ni des majuscules,
        ni des accents.

        """
        chaine = supprimer_accents(chaine).lower()
        chaine = chaine.rstrip(".,?!")
        chaine = chaine.strip()

        if not expression:
            raise ErreurExecution("l'expression testée est vide")

        for exp in expression.split("_b_"):
            exp = supprimer_accents(exp).lower()
            if chaine == exp:
                return True

        return False

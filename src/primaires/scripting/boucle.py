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


"""Fichier contenant la classe Boucle, détaillée plus bas."""

from .instruction import Instruction
from .parser import expressions, MetaExpression

class Boucle(Instruction):

    """Classe définissant une instruction de boucle.

    Une boucle est une instruction suivie d'une forme particulière
    d'expression. Sa syntaxe IG est la suivante :
        pour chaque [variable] in [expression]:
            ...
        fait

    """

    def __init__(self):
        """Constructeur d'une boucle."""
        Instruction.__init__(self)
        self.type = None
        self.variable = None
        self.expression = None

    def __str__(self):
        ret = "|mr|" + self.type + "|ff|"
        if self.type == "pour chaque":
            ret += " " + str(self.variable) + "|mr| dans |ff|" + \
                    str(self.expression) + "|mr|:|ff|"

        return ret

    @classmethod
    def peut_interpreter(cls, chaine):
        """La chaîne peut-elle être interprétée par la classe Condition."""
        if chaine.startswith("pour chaque ") and chaine.endswith(":"):
            return True

        if chaine == "fait":
            return True

        return False

    @classmethod
    def construire(cls, chaine):
        """Construit l'instruction.

        L'instruction est sous la forme :
            pour chaque [variable] dans [expression]

        """
        taille_type = 0
        chn_condition = chaine
        boucle = Boucle()
        if chaine == "fait":
            boucle.type = "fait"
            return boucle

        # La chaîne doit avoir la forme 'pour chaque {variable]...'
        boucle.type = "pour chaque"
        chaine = chaine[12:-1]
        boucle.variable, chaine = expressions["variable"].parser(
                chaine)

        if not chaine.startswith(" dans ") or len(chaine) < 7:
            raise ValueError("Syntaxe invalide pour une boucle")

        chaine = chaine[6:]
        print(chaine, boucle.variable)
        boucle.expression, chaine = MetaExpression.choisir(
                ["fonction", "variable"], chaine)
        return boucle

    def deduire_niveau(self, dernier_niveau):
        """Déduit le niveau de l'instruction."""
        self.niveau = dernier_niveau
        if self.type == "fait":
            self.niveau -= 1

    def get_niveau_suivant(self):
        """Retourne le niveau de la prochaine instruction."""
        niveau = self.niveau
        if self.type != "fait":
            niveau += 1

        return niveau

    @property
    def code_python(self):
        """Retourne le code Python de l'instruction."""
        py_code = ""
        if self.type != "fait":
            py_code += "for " + self.variable.code_python
            py_code += " in " + self.expression.code_python + ":"

        return py_code

    def detruire(self):
        """Destruction de l'instruction."""
        super(Boucle, self).detruire()
        if self.variable:
            self.variable.detruire()
        if self.expression:
            self.expression.detruire()

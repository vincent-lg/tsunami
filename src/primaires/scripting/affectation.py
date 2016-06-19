# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 LE GOFF Vincent
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following affectations are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of affectations and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of affectations and the following disclaimer in the documentation
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


"""Fichier contenant la classe Affectation, détaillée plus bas."""

from .instruction import Instruction
from .parser import expressions, MetaExpression

class Affectation(Instruction):

    """Classe définissant une instruction d'affectation.

    Une instruction se présente sous une forme très simple :
    >>> variable = autre_variable
    ou
    >>> variable = expression
    ou
    >>> variable = fonction(parametres)

    """

    def __init__(self):
        """Construction d'une affectation."""
        Instruction.__init__(self)
        self.variable = None
        self.expression = None

    def __str__(self):
        return str(self.variable) + " |mr|=|ff| " + str(self.expression)

    @classmethod
    def peut_interpreter(cls, chaine):
        """La chaîne peut-elle être interprétée par la classe Condition ?"""
        return "=" in chaine

    @classmethod
    def construire(cls, chaine):
        """Construit l'instruction.

        L'instruction est sous la forme :
        >>> nom_variable = expression

        """
        chn_affectation = chaine
        affectation = Affectation()

        # On extrait le nom de la variable
        try:
            nom_variable, expression = chaine.split("=")
        except ValueError as err:
            print("Erreur de parsage de l'affectation", chn_affectation, ".")
            return

        affectation.variable, chn = expressions["variable"].parser(
                nom_variable.rstrip())

        # Parsage de l'expression
        chaine = expression.lstrip(" ")
        types = ("variable", "nombre", "chaine", "fonction", "calcul")
        expression, chaine = MetaExpression.choisir(types, chaine)
        affectation.expression = expression

        return affectation

    @property
    def code_python(self):
        """Retourne le code Python de l'instruction."""
        py_code = self.variable.code_python + " = " + \
                self.expression.code_python
        return py_code

    def detruire(self):
        """Destruction de l'instruction."""
        super(Affectation, self).detruire()
        if self.variable:
            self.variable.detruire()
        if self.expression:
            self.expression.detruire()

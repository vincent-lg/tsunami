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


"""Fichier contenant la classe Tests, détaillée plus bas."""

from .expression import Expression
from . import expressions

class Tests(Expression):

    """Expression tests."""

    nom = "tests"
    def __init__(self):
        """Constructeur de l'expression."""
        Expression.__init__(self)
        self.nom = None
        self.contraire = False
        self.expressions = ()

    def __repr__(self):
        expressions = [str(e) for e in self.expressions]
        chaine = " ".join(expressions)
        if self.contraire:
            chaine = "!" + chaine

        return chaine

    @classmethod
    def parsable(cls, chaine):
        """Retourne True si la chaîne est parsable, False sinon."""
        return True

    @classmethod
    def parser(cls, chaine):
        """Parse la chaîne.

        Retourne l'objet créé et la partie non interprétée de la chaîne.

        """
        objet = cls()
        expressions = cls.expressions_def

        # Parsage des expressions
        types = ("nombre", "chaine", "fonction", "operateur", "connecteur",
                "variable", "calcul")
        expressions = []

        if chaine.startswith("!"):
            objet.contraire = True
            chaine = chaine[1:]

        while chaine.strip():
            arg, chaine = cls.choisir(types, chaine)
            expressions.append(arg)

        objet.expressions = tuple(expressions)

        return objet, chaine

    @property
    def code_python(self):
        """Retourne le code Python du test."""
        py_tests = [t.code_python for t in self.expressions]
        code = " ".join(py_tests)
        if self.contraire:
            code = "not " + code

        return code

    def detruire(self):
        """Destruction de l' expression."""
        super(Tests, self).detruire()
        for expression in self.expressions:
            expression.detruire()

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


"""Fichier contenant la classe Calcul, détaillée plus bas."""

import re

from .expression import Expression
from . import expressions

## Constantes
# Regex
RE_INV = re.compile(r"[A-Za-z_]\(")
RE_OPERATEURS = re.compile(r"[-+*/()]")

class Calcul(Expression):

    """Expression calcul.

    Cette expression permet d'intégrer des calculs avec des opérateurs
    mathématiques et des parenthèses. Les expression pouvant être
    parsées par cette expression sont :
        1 + 2
        1 - variable
        3 * autre
        (4 + variable) / 2
        fonction(chose) + (3 * autre_variable) - 1

    """

    nom = "calcul"
    def __init__(self):
        """Constructeur de l'expression."""
        Expression.__init__(self)
        self.expressions = []
        self.operateurs = ""

    def __repr__(self):
        expressions = [str(e) for e in self.expressions]
        return self.operateurs.format(*expressions)

    @classmethod
    def parsable(cls, chaine):
        """Retourne True si la chaîne est parsable, False sinon."""
        inv = RE_INV.search(chaine)
        if inv:
            return False

        for op in ('\\"', '\\(', '\\)', '\\+', '-', '\\*', '/'):
            reg = r"\".*?" + op + r".*?\""
            if re.search(reg, chaine):
                return False

        return RE_OPERATEURS.search(chaine) is not None

    @classmethod
    def parser(cls, chaine):
        """Parse la chaîne.

        Retourne l'objet créé et la partie non interprétée de la chaîne.

        """
        objet = cls()

        # Parsage des paramètres
        types = ("variable", "nombre", "chaine", "fonction")
        while True:
            chaine = chaine.lstrip(" ")
            if not chaine:
                break

            if RE_OPERATEURS.search(chaine[0]):
                # C'est un opérateur, on l'ajoute à la chaîne operateurs
                operateur = chaine[0]
                if operateur == ")" and "(" not in objet.operateurs:
                    break

                chaine = chaine[1:]
                dernier_car = objet.operateurs and objet.operateurs[-1] or ""
                if dernier_car and operateur in "+-*/" and dernier_car not in \
                        "+-/*(":
                    objet.operateurs += " "
                objet.operateurs += operateur
                ops = objet.operateurs
                if operateur == ")" and ops.count("(") == ops.count(")"):
                    break
            else:
                # C'est une expression supposée
                try:
                    arg, chaine = cls.choisir(types, chaine)
                except ValueError:
                    break

                dernier_car = objet.operateurs and objet.operateurs[-1] or ""
                if dernier_car and dernier_car in "+-*/)":
                    objet.operateurs += " "

                objet.operateurs += "{" + str(len(objet.expressions)) + "}"
                objet.expressions.append(arg)

        return objet, chaine

    @property
    def code_python(self):
        """Retourne le code Python associé à la fonction."""
        expressions = [e.code_python for e in self.expressions]
        return self.operateurs.format(*expressions)

    def detruire(self):
        """Destruction de l' expression."""
        super(Calcul, self).detruire()
        for expression in self.expressions:
            expression.detruire()

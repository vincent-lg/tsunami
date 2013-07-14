# -*-coding:Utf-8 -*

# Copyright (c) 2013 LE GOFF Vincent
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


"""Fichier contenant la classe Bloc détaillée plus bas."""

import re

from abstraits.obase import BaseObj
from primaires.scripting.espaces import Espaces
from primaires.scripting.instruction import ErreurExecution
from primaires.scripting.test import Test
from primaires.scripting.variable import Variable

# Constantes
RE_VAR = re.compile(r"^[A-Za-z][A-Za-z0-9]*$")

class Bloc(BaseObj):

    """Classe contenant un bloc d'instructions scripting.

    Un bloc est un ensemble d'instructions mais, à la différence des
    évènements et des tests qui le composent, un bloc n'est pas appelé
    automatiquement par le système, mais par une instruction scripting.
    En somme, en terme de programmation, il s'agit d'une fonction
    avec des paramètres. Pour l'appeler depuis un évènement, il faut utiliser
    soit l'action 'appeler', soit la fonction du même nom. Utiliser
    la fonction a l'avantage de pouvoir capturer le retour dans une variable.

    """

    def __init__(self, script, nom):
        """Constructeur d'un  bloc.

        Il prend en paramètre :
            script -- le script possédant le bloc
            nom -- le nom du bloc

        """
        BaseObj.__init__(self)
        self.script = script
        self.nom = nom
        self.__test = None
        self.variables = []
        self.espaces = Espaces(self)
        self._construire()

    def __getnewargs__(self):
        return (None, "inconnu")

    def __str__(self):
        return "bloc {}".format(self.nom)

    @property
    def test(self):
        """Retourne le test et le crée si nécessaire."""
        if self.__test is None:
            self.__test = Test(self)

        return self.__test

    def ajouter_variable(self, nom, str_type, aide):
        """Ajoute une variable.

        Le type est précisé en nom français.

        """
        if nom in [v.nom for v in self.variables]:
            raise ValueError("la variable '{}' existe déjà".format(nom))

        types = {
            "nombre": "Fraction",
        }

        if str_type in types:
            str_type = types[str_type]
        else:
            str_type = str_type.capitalize()

        if RE_VAR.search(nom) is None:
            raise ValueError("Le nom de variable '{}' est invalide".format(
                    nom))

        try:
            variable = Variable(self, nom, str_type)
        except AttributeError:
            raise ValueError("type '{}' inconnu".format(str_type))
        else:
            variable.aide = aide
            self.variables.append(variable)
            return variable

    def executer(self, *args):
        """Execute le bloc d'instructions.

        On valide d'abord le variable et leur type. En cas d'erreur,
        une ErreurExcecution est levée. On récupère le résultat de la
        variable 'retour', si il y en a une, que l'on retourne au cas où.

        """
        variables = {}
        for i, def_variable in enumerate(self.variables):
            try:
                variable = args[i]
            except IndexError:
                raise ErreurExecution("la variable '{}' pour le bloc '{}' " \
                        "n'a pas été précisée".format(def_variable.nom,
                        self.nom))

            v_type = def_variable.type
            if not isinstance(variable, v_type):
                raise ErreurExecution("La variable '{}' pour le bloc '{}' " \
                        "n'est pas du bon type ({} attendu, {} obtenu)".format(
                        def_variable.nom, self.nom, def_variable.type,
                        type(variable)))

            variables[def_variable.nom] = variable

        self.espaces.variables.update(variables)
        if self.__test:
            self.__test.executer_instructions(self)

        if "retour" in self.espaces.variables:
            return self.espaces.variables["retour"]

        return None

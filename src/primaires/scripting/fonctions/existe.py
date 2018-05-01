# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
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


"""Fichier contenant la fonction existe."""

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Teste si une variable ou donnée existe."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.variable_existe, "object")
        cls.ajouter_types(cls.donnee_existe, "str", "str")

    @staticmethod
    def variable_existe(variable):
        """Retourne vraie si la variable existe, False sinon."""
        return variable is not None

    @staticmethod
    def donnee_existe(type, cle):
        """Retourne vraie si la donnée existe, faux sinon.

        Une donnée peut être de nombreuses choses, comme un
        prototype d'objet, un PNJ, une plante... Pour savoir ce que
        vous voulez chercher, vous devez renseigner le type de la
        donnée (la liste des types est donnée ci-dessous) ainsi que
        la clé de la donnée. Consultez les exemples ci-dessous pour
        plus d'informations.

        Liste des types :

          * "prototype d'objet"


        Exemples d'utilisation :

          # Cherche si le prototype d'objet 'chapeau_gris' existe
          si existe("prototype d'objet", "chapeau_gris"):

        """
        types = importeur.scripting.valeurs
        dictionnaire = types.get(type)
        if dictionnaire is None:
            raise ErreurExecution("Type {} inconnu".format(repr(type)))

        return cle in dictionnaire

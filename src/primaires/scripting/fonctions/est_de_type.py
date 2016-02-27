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


"""Fichier contenant la fonction est_de_type."""

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Retourne vrai si l'objet ou prototype est de type indiqué."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.est_de_type_objet, "Objet", "str")
        cls.ajouter_types(cls.est_de_type_objet, "PrototypeObjet", "str")
        cls.ajouter_types(cls.est_de_type_cle, "str", "str")

    @staticmethod
    def est_de_type_objet(objet, nom_type):
        """Retourne vrai si l'objet est du type indiqué.

        Retourne vrai également si le nom de type est un parent du
        type de l'objet. Par exemple, si l'objet est un fruit
        mais que l'on test si c'est une nourriture.

        Paramètres à entrer :

          * objet : l'objet à tester
          * nom_type : le nom du type

        """
        return objet.est_de_type(nom_type)

    @staticmethod
    def est_de_type_cle(cle, nom_type):
        """Retourne vrai si le prototype d'objet est du type indiqué.

        Retourne vrai également si le nom de type est un parent du
        type du prototype. Par exemple, si le prototype est un fruit
        mais que l'on test si c'est une nourriture.

        Paramètres à entrer :

          * cle : la clé du prototype d'objet (une chaîne)
          * nom_type : le nom du type

        """
        cle = cle.lower()
        if not cle in importeur.objet.prototypes:
            raise ErreurExecution("prototype {} introuvable".format(
                    repr(cle)))

        prototype = importeur.objet.prototypes[cle]
        return prototype.est_de_type(nom_type)

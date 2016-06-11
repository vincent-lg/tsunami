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


"""Fichier contenant la fonction prix."""

from fractions import Fraction

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Renvoie le prix (en KG) de l'objet."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.prix, "PrototypeObjet")
        cls.ajouter_types(cls.prix, "Objet")
        cls.ajouter_types(cls.prix_prototype, "str")

    @staticmethod
    def prix(objet):
        """Retourne le prix de l'objet.

        Si le prix de l'objet n'a pas été changé, retourne le
        prix unitaire du prototype. L'objet précisé peut également être
        un prototype d'objet.

        Paramètres à préciser:

          * objet : l'objet ou le prototype dont on veut le prix.

        Exemple d'utilisation :

          # 'objet' contient un objet
          prix = prix(objet)
          # Ou depuis un prototype
          prototype = prototype_objet("pomme_rouge")
          prix = prix(prototype)

        """
        return Fraction(objet.m_valeur)

    @staticmethod
    def prix_prototype(cle_prototype):
        """Retourne le prix du prototype d'objet.

        Cette fonction retourne le prix unitaire du prototype d'objet,
        tel que défini dans l'éditeur 'oedit'.

        Paramètres à préciser:

          * cle_prototype : la clé du prototype d'objet.

        Exemple d'utilisation :

          prix = prix("pomme_rouge")

        """
        try:
            prototype = importeur.objet.prototypes[cle_prototype]
        except KeyError:
            raise ErreurExecution("prototype d'objet inconnu {}".format(
                    repr(cle_prototype)))

        return Fraction(prototype.m_valeur)

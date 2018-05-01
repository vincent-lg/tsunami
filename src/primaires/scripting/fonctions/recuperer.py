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


"""Fichier contenant la fonction recuperer."""

from fractions import Fraction

from corps.fonctions import valider_cle
from primaires.scripting.fonctions.recuperer_valeur_dans_liste import \
        ClasseFonction as CF
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(CF):

    """Récupère la valeur d'une liste."""

    @classmethod
    def init_types(cls):
        super(ClasseFonction, cls).init_types()
        cls.ajouter_types(cls.recuperer_structure, "Structure", "str")
        cls.ajouter_types(cls.recuperer_chaine, "str", "Fraction")

    @staticmethod
    def recuperer_structure(structure, cle):
        """Récupère la valeur contenue dans la case de clé indiquée.

        Paramètres à préciser :

          * structure : la structure qui nous occupe ici
          * cle : la clé de la case d'information à retrouver

        Exemple d'utilisation :

          # Sur une structure enregistrée dans un groupe, on pourrait faire :
          id = recuperer(structure, "id")
          # Pour récupérer son ID. Ou bien une autre case :
          message = recuperer(structure, "message")
          # Si la case de la clé indiquée n'existe pas, retourne
          # une valeur nulle qu'on peut donc tester.
          si message:
            # ...

        """
        valider_cle(cle)
        objet = getattr(structure, cle, None)
        if isinstance(objet, (int, float, bool)):
            objet = Fraction(objet)

        return objet

    @staticmethod
    def recuperer_chaine(chaine, indice):
        """Récupère la lettre à la position spécifiée.

        Une chaîne est un ensemble composite au même titre qu'une liste. Elle ne contient que des lettres, cependant (des caractères, qui sont des chaînes de caractère de longueur 1). Vous pouvez utiliser cette fonction la lettre en début ou en fin d'une chaîne, par exemple.

        Paramètres à préciser :

          * chaine : la chaîne utilisée ;
          * indice : l'indice (numéro de la case où se trouve la lettre).

        Exemples d'utilisation :

          # Récupère la première lettre de la chaîne
          premiere = recuperer("juste quelques mots", 1)
          # 'premiere' contient "j"
          derniere = recuperer("juste quelques mots", -1)
          # 'derniere' contient "s"

        """
        indice = int(indice)
        if indice > 0:
            if indice > len(chaine):
                raise ErreurExecution("L'indice précisé ({}) est trop " \
                        "important pour la chaîne {}.".format(
                        indice, repr(chaine)))
            indice -= 1
        elif indice < 0:
            if -indice > len(chaine):
                raise ErreurExecution("L'indice précisé ({}) est trop " \
                        "important pour la chaîne {}.".format(
                        indice, repr(chaine)))
        else:
            raise ErreurExecution("L'indice précisé vaut 0.")

        return chaine[indice]

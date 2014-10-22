# -*-coding:Utf-8 -*

# Copyright (c) 2010 LE GOFF Vincent
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


"""Fichier contenant l'action ajouter_a_liste"""

from primaires.perso.exceptions.action import ExceptionAction
from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Modifie un élément d'une liste."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.modifier_element_liste, "object", "Fraction",
                "list")

    @staticmethod
    def modifier_element_liste(element, indice, liste):
        """Modifie l'élément de la liste à l'indice indiqué.

        Paramètres à préciser :

          * element : le nouvel élément à placer à l'indice
          * indice : l'indice (un nombre entier)
          * liste : la liste d'éléments à modifier

        Si on se représente une liste comme une suite de cases numérotées
        (de 1 à N), alors l'indice représente le numéro de la case dans
        lequel mettre element. Référez-vous aux exemples donnés
        pour avoir une idée de ce que fait cette action.

        *NOTE* : les actions 'modifier' et 'modifier_element_liste'
        font strictement la même chose. La seconde est conservée pour des
        raisons de compatibilité. Préférez utiliser la première
        ('modifier') dans vos scripts.

        Exemples d'utilisation :

          nombres = liste(5, 9, 7, 8)
          # On va mettre le nombre 6 dans la seconde case de la liste
          # qui contient pour l'instant 9
          modifier 6 2 nombres
          # La liste contient à présent : [5, 6, 7, 8]

        """
        if int(indice) != indice: # nombre flottant
            raise ErreurException("le nombre flottant {} a été précisé " \
                    "comme indice de liste. Seuls des nombres entiers " \
                    "(1, 2, 3, ...) sont acceptés".format(indice))

        if indice < 1:
            raise ErreurExecution("l'indice précisé doit être supérieur " \
                    "à 0".format(indice))

        if indice > len(liste):
            raise ErreurExecution("l'indice spécifié ({}) est plus grand " \
                    "que la taille de la liste ({})".format(indice,
                    len(liste)))

        liste[int(indice) - 1] = element

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


"""Fichier contenant l'action retirer"""

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Retire un élément d'une liste."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.retirer, "object", "list")

    @staticmethod
    def retirer(element, liste):
        """Retire l'élément d'une liste.

        Paramètres à préciser :

          * element : l'élément à retirer de la listeajouter à la liste
          * liste : la liste à modifier

        L'élément sera retirée de la liste même si il apparaît plusieurs
        fois (si la liste a des doublons). Cependant, si l'élément
        n'apparaît pas dans la liste, une alerte sera créée. Il est
        peut-être donc opportun de vérifier la présence de l'élément
        (avec la fonction 'contient') avant de le supprimer.

        Exemples d'utilisation :

          nombres = liste(1, 2, 3, 4, 5)
          retirer 3 nombres
          # nombres contient à présent [1, 2, 4, 5]
          nombres = liste(1, 2, 1, 2, 3)
          retirer 2 nombres
          # nombres contient à présent [1, 1, 3]

        """
        if element not in liste:
            raise ErreurExecution("cette liste ne contient pas l'élément " \
                    "{}".format(repr(element)))

        while element in liste:
            liste.remove(element)

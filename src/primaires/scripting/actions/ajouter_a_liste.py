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

    """Ajoute un élément à une liste."""
    verifier = False

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.ajouter_a_liste)

    @staticmethod
    def ajouter_a_liste(element, liste):
        """Ajoute un élément à une liste.

        Paramètres à préciser :

          * element : l'élément à ajouter à la liste
          * liste : la liste à modifier

        L'élément sera ajouté à la fin de la liste. L'élément peut être de
        différents types, nombres, chaînes de caractères, joueurs, salles,
        PNJ et autre. La liste spécifiée peut :

          * Contenir des données de différents types
          * Contenir la même donnée en double.

        *NOTE* : les actions 'ajouter' et 'ajouter_a_liste' font strictement
        la même chose et s'utilisent de la même façon. La seconde est
        conservée pour des raisons de compatibilité, préférez utiliser
        la première ('ajouter').

        Exemples d'utilisation :

          nombres = liste()
          ajouter 1 nombres
          ajouter 2 nombres
          # nombres contient maintenant [1, 2]

        """
        liste.append(element)

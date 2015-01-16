# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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
# LIABLE FOR ANY tipCT, INtipCT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant l'action tip."""

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Envoie une tip (court message d'aide contextuel).

    Vous pouvez utiliser cette action pour envoyer des tips uniques (qui
    ne sont envoyées qu'une fois) ou non unique (envoyées à chaque
    fois que le personnage est dans le contexte).

    """

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.tip_non_unique, "Personnage", "str")
        cls.ajouter_types(cls.tip_unique, "Personnage", "str", "str")

    @staticmethod
    def tip_non_unique(personnage, message):
        """Envoie la tip non unique au personnage.

        Si par exemple cette instruction se trouve dans l'évènement
        arrive d'une salle, la tip sera envoyée à chaque
        personnage entrant dans cette salle. Vous pouvez aussi envoyer
        des tips uniques, qui ne seront envoyées que la première fois
        et après ignorées (voir plus bas).

        """
        message = message.replace("_b_", "|").replace("|nl|", "\n")
        personnage.envoyer_tip(message)

    @staticmethod
    def tip_unique(personnage, cle, message):
        """Envoie une tip unique au personnage.

        Les tips uniques ne sont envoyées qu'une fois pour chaque personnage.
        Vous devez préciser une clé identifiant de façon unique la clé
        (si possible assez explicite), comme "entrer_taverne" si le
        personnage entre dans la taverne quand la tip est envoyée.

        """
        if not cle:
            raise ErreurExecution("une clé vide a été passée pour " \
                    "envoyer une tip unique")

        message = message.replace("_b_", "|").replace("|nl|", "\n")
        personnage.envoyer_tip(message, cle=cle, unique=True)

# -*-coding:Utf-8 -*

# Copyright (c) 2015 LE GOFF Vincent
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


"""Fichier contenant l'action agir."""

from primaires.perso.exceptions.action import ExceptionAction
from primaires.scripting.action import Action
from primaires.scripting.exceptions import InterrompreCommande
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Force le personnage d'agir pour vérifier ses états."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.agir, "Personnage")
        cls.ajouter_types(cls.agir, "Personnage", "str")

    @staticmethod
    def agir(personnage, cle_action=""):
        """Force un personnage à agir.

        Cette action est utile pour vérifier qu'un personnage a
        le droit de faire une action. Un état (ou plusieurs)
        pourraient l'en empêcher. Si un état empêche le personnage
        d'agir, un message de refus lui est envoyé (par exemple,
        "Vous êtes en train de combattre" ou "Vous êtes inconscient")
        et le script est interrompu.

        Paramètres à renseigner :

          * personnage : le personnage qui doit agir
          * cle_action : la clé de l'action (peut être laissée vide)

        Changer la clé de l'action permet spécifiquement
        d'autoriser certains états à être valiés quand même.

        """
        cle_action = cle_action or "action"

        try:
            personnage.agir(cle_action)
        except ExceptionAction as err:
            personnage << "|err|{}|ff|".format(str(err))
            raise InterrompreCommande()

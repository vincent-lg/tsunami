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


"""Fichier contenant l'action desaffecter."""

from primaires.format.fonctions import supprimer_accents
from primaires.perso.exceptions.action import ExceptionAction
from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Retire l'affection à un personnage ou une salle."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.desaffecter_personnage, "Personnage", "str")
        cls.ajouter_types(cls.desaffecter_salle, "Salle", "str")

    @staticmethod
    def desaffecter_personnage(personnage, affection):
        """Retire l'affection au personnage.

        Les paramètres à préciser sont :

          * personnage : le personnage à désaffecter
          * affection : la clé de l'affection sous la forme d'une chaîne.

        Si le personnage n'est pas aff"ecté par l'affection précisée,
        une alerte est levée.

        """
        # Essaye de trouver l'affection
        cle = affection.lower()
        try:
            affection = importeur.affection.get_affection("personnage", cle)
        except KeyError:
            raise ErreurExecution("l'affection {} n'existe pas".format(repr(
                    cle)))

        if cle not in personnage.affections:
            raise ErreurExecution("le personnage n'est pas affecté par " \
                    "cette affection")

        personnage.affections.pop(cle).detruire()

    @staticmethod
    def desaffecter_salle(salle, affection):
        """Retire l'affection à la salle.

        Les paramètres à préciser sont :

          * salle : la salle à désaffecter
          * affection : la clé de l'affection sous la forme d'une chaîne.

        Si la salle n'est pas affectée par l'affection précisée, une alerte
        est créée.

        """
        # Essaye de trouver l'affection
        cle = affection.lower()
        try:
            affection = importeur.affection.get_affection("salle", cle)
        except KeyError:
            raise ErreurExecution("l'affection {} n'existe pas".format(repr(
                    cle)))

        if cle not in salle.affections:
            raise ErreurExecution("la salle n'est pas affectée par " \
                    "cette affection")

        salle.affections.pop(cle).detruire()

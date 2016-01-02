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


"""Fichier contenant l'action affecter."""

from primaires.format.fonctions import supprimer_accents
from primaires.perso.exceptions.action import ExceptionAction
from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Donne une affection à un personnage ou une salle."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.affecter_personnage, "Personnage",
                "str", "Fraction", "Fraction")
        cls.ajouter_types(cls.affecter_salle, "Salle",
                "str", "Fraction", "Fraction")

    @staticmethod
    def affecter_personnage(personnage, affection, duree, force):
        """Donne l'affection au personnage.

        Les paramètres à préciser sont :

          * personnage : le personnage à affecter
          * affection : la clé de l'affection sous la forme d'une chaîne
          * duree : la durée de l'affection
          * force : la force de l'affection

        Si le personnage est déjà affecté par la même affection, les
        nouvelles valeurs sont modulées (le résultat final dépend de
        l'affection choisie).

        Généralement, la durée et la force sont ajoutées aux anciennes
        valeurs.

        """
        # Essaye de trouver l'affection
        cle = affection.lower()
        try:
            affection = importeur.affection.get_affection("personnage", cle)
        except KeyError:
            raise ErreurExecution("l'affection {} n'existe pas".format(repr(
                    cle)))

        personnage.affecte(cle, int(duree), int(force))

    @staticmethod
    def affecter_salle(salle, affection, duree, force):
        """Donne l'affection à la salle.

        Les paramètres à préciser sont :

          * salle : la salle à affecter
          * affection : la clé de l'affection sous la forme d'une chaîne
          * duree : la durée de l'affection
          * force : la force de l'affection

        Si la salle est déjà affectée par la même affection, les
        nouvelles valeurs sont modulées (le résultat final dépend de
        l'affection choisie).

        Généralement, la durée et la force sont ajoutées aux anciennes
        valeurs.

        """
        # Essaye de trouver l'affection
        cle = affection.lower()
        try:
            affection = importeur.affection.get_affection("salle", cle)
        except KeyError:
            raise ErreurExecution("l'affection {} n'existe pas".format(repr(
                    cle)))

        salle.affecte(cle, int(duree), int(force))

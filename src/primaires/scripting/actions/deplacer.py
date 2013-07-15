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
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant l'action deplacer."""

from primaires.format.fonctions import supprimer_accents
from primaires.perso.exceptions.action import ExceptionAction
from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Un ppersonnage se déplace vers une sortie indiquée.

    Cette action demande à un personnage de se déplacer dans la direction
    indiquée. Il est préférable de l'utiliser avec des tests ou conditions
    pour s'assurer que le personnage est bien dans la salle choisie
    avant de lui demander de se déplacer, sauf si c'est vraiment le but
    recherché. En outre, cette action peut aussi bien agir sur les
    PNJ que les joueurs, soyez prudent.

    """

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.deplacer_personnage, "Personnage",
                "str")

    @staticmethod
    def deplacer_personnage(personnage, sortie):
        """Déplace le personnage vers la sortie indiquée.

        La sortie peut être donnée sous la forme de sa direction absolue
        ou son nom renommé (les noms comme "escalier" sont autorisés).

        """
        # Obtension de la direction
        try:
            sortie = personnage.salle.sorties.get_sortie_par_nom_ou_direction(
                    supprimer_accents(sortie).lower())
            assert sortie
        except (KeyError, AssertionError):
            raise ErreurExecution("la sortie {} est introuvable en {}".format(
                    sortie, personnage.salle))

        try:
            personnage.deplacer_vers(sortie.nom)
        except ExceptionAction:
            pass

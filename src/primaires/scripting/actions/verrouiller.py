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


"""Fichier contenant l'action verrouiller_porte."""

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Verrouille une porte."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.verrouiller_porte, "Salle", "str")

    @staticmethod
    def verrouiller_porte(salle, nom_sortie):
        """Verrouille une porte.
        Le paramètre nom_sortie est un nom de sortie ou une direction.
        Une erreur est envoyée si la sortie n'est pas trouvée ou si
        aucune porte n'est définie sur cette sortie.

        """
        sortie = salle.sorties.get_sortie_par_nom_ou_direction(nom_sortie)
        if sortie is None:
            raise ErreurExecution("la salle {} n'a pas de sortie {}".format(
                    salle.ident, nom_sortie))

        if sortie.porte is None:
            raise ErreurExecution("la sortie {}[{}] n'a pas de porte".format(
                    salle.ident, sortie.nom))

        try:
            sortie.porte.verrouiller()
        except ValueError: # la porte est déjà verrouillée
            pass

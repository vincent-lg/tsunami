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
# LIABLE FOR ANY teleporterCT, INteleporterCT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant l'action creer_sortie."""

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Crée une sortie dans une salle.

    Une sortie doit obligatoirement mener vers une autre salle.

    """

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.creer_sortie, "Salle", "str", "Salle")

    @staticmethod
    def creer_sortie(salle, direction, destination):
        """Crée une sortie de salle dans la direction vers la destination.

        La direction est à choisir parmi est, ouest, nord, sud, nord-est,
        nord-ouest, sud-est, sud-ouest, haut et bas.

        """
        try:
            direction = salle.sorties.get_nom_long(direction)
        except KeyError:
            raise ErreurExecution("direction {} inconnue".format(direction))
        dir_opposee = salle.sorties.get_nom_oppose(direction)
        if salle.sorties.sortie_existe(direction):
            raise ErreurExecution("sortie {} déjà définie dans {}".format(
                    direction, salle))
        if destination.sorties.sortie_existe(dir_opposee):
            raise ErreurExecution("sortie opposée déjà définie dans {}".format(
                    destination))
        if salle is destination:
            raise ErreurExecution("salle et destination confondues")
        salle.sorties.ajouter_sortie(direction, direction,
                salle_dest=destination, corresp=dir_opposee)
        destination.sorties.ajouter_sortie(dir_opposee, dir_opposee,
                salle_dest=salle, corresp=direction)

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
# LIABLE FOR ANY teleporterCT, INteleporterCT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant l'action nommer_sortie."""

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Renomme une sortie d'une salle."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.nommer_sortie, "Salle", "str", "str")

    @staticmethod
    def nommer_sortie(salle, direction, nom):
        """Renomme la sortie de salle dans cette direction en 'nom'.

        La direction est à choisir parmi est, ouest, nord, sud, nord-est,
        nord-ouest, sud-est, sud-ouest, haut et bas. Vous devez en outre
        préciser l'article de la sortie (le, la ou l'), par exemple
        "la porte".

        """
        try:
            direction = salle.sorties.get_nom_long(direction)
        except KeyError:
            raise ErreurExecution("direction {} inconnue".format(direction))
        if not salle.sorties.sortie_existe(direction):
            raise ErreurExecution("sortie {} non définie".format(direction))
        article = nom.split(" ")[0]
        if not article in ("le", "la"):
            article = "l'"
        salle.sorties[direction].nom = nom[2:].strip()
        salle.sorties[direction].article = article

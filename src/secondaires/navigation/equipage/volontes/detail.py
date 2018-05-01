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


"""Fichier contenant la volonté Detail."""

import re

from secondaires.navigation.constantes import *
from secondaires.navigation.equipage.volonte import Volonte
from secondaires.navigation.visible import Visible

class Detail(Volonte):

    """Classe représentant une volonté.

    Cette volonté demande à la vigie ce qu'elle voit.

    """

    cle = "vigie"
    ordre_court = re.compile(r"^d([arbt])?$", re.I)
    ordre_long = re.compile(
            r"^detail\s*(avant|arriere|babord|tribord)?$", re.I)

    def __init__(self, navire, direction=None):
        """Construit une volonté."""
        Volonte.__init__(self, navire)
        self.direction = direction

    @property
    def arguments(self):
        """Propriété à redéfinir si la volonté comprend des arguments."""
        return (self.direction, )

    def choisir_matelots(self, exception=None):
        """Retourne le matelot le plus apte à accomplir la volonté."""
        navire = self.navire
        return navire.equipage.get_matelots_au_poste("vigie")

    def executer(self, vigies):
        """Exécute la volonté."""
        initiateur = self.initiateur
        if not vigies:
            return

        vigie = vigies[0]
        personnage = vigie.personnage
        salle = vigie.salle
        navire = salle.navire
        etendue = navire.etendue
        alt = etendue.altitude
        portee = get_portee(salle)
        point = self.direction
        if point:
            limite = 45
            precision = 5
            if point == "arriere":
                direction = 180
            elif point == "babord":
                direction = -90
            elif point == "tribord":
                direction = 90
            elif point == "avant":
                direction = 0
        else:
            direction = 0
            limite = 90
            precision = 15

        # On récupère les points
        points = Visible.observer(personnage, portee, precision,
                {"": navire})
        msg = points.formatter(direction, limite)
        if not msg:
            msg = "La vigie signale que rien n'est visible pour l'heure."

        initiateur.envoyer(msg)

    def crier_ordres(self, personnage):
        """On fait crier l'ordre au personnage."""
        return

    @classmethod
    def extraire_arguments(cls, navire, direction):
        """Extrait les arguments de la volonté."""
        if not direction:
            direction = None
        elif direction in ("a", "avant"):
            direction = "avant"
        elif direction in ("r", "arriere"):
            direction = "arriere"
        elif direction in ("b", "babord"):
            direction = "babord"
        elif direction in ("t", "tribord"):
            direction = "tribord"
        else:
            direction = None

        return (direction, )

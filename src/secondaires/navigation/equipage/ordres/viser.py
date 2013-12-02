# -*-coding:Utf-8 -*

# Copyright (c) 2013 LE GOFF Vincent
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


"""Fichier contenant l'ordre Viser."""

from vector import Vector

from primaires.vehicule.vecteur import get_direction
from secondaires.navigation.equipage.signaux import *

from ..ordre import *

class Viser(Ordre):

    """Ordre viser.

    Cet ordre demande au matelot de viser un navire adverse à l'aide
    d'un canon. Il s'agit de faire pivoter le canon pour trouver un
    angle de tir favorable, sachant qu'il n'est pas forcément trouvé.

    """

    cle = "viser"
    def __init__(self, matelot, navire, canon=None, adverse=None,
            bruyant=True):
        Ordre.__init__(self, matelot, navire)
        self.canon = canon
        self.adverse = adverse
        self.bruyant = bruyant

    def executer(self):
        """Exécute l'ordre : colmate."""
        navire = self.navire
        matelot = self.matelot
        personnage = matelot.personnage
        canon = self.canon
        salle = canon.parent
        adverse = self.adverse
        yield 0.3

        vecteur, cible = canon.cible()
        if cible and getattr(cible, "navire", None) is adverse:
            yield SignalInutile("on vise déjà ce navire")

        # On parcourt toutes les salles du navire adverse
        # Celles qui ne sont pas dans un angle favorable sont rejetées
        position = Vector(*salle.coords.tuple())
        cible = None
        if adverse is None or not adverse.e_existe:
            yield SignalAbandonne("Ce navire est déjà coulé")

        for adv_salle in adverse.salles.values():
            if adv_salle.coords.z != salle.coords.z:
                continue

            adv_vecteur = Vector(*adv_salle.coords.tuple())
            direction = adv_vecteur - position
            direction = get_direction(direction)
            direction = (direction - navire.direction.direction) % 360
            if salle.sabord_oriente(direction):
                if direction > 180:
                    direction = -360 + direction

                canon.h_angle = int(direction)
                vecteur, cible = canon.cible()
                if cible is adv_salle:
                    break

        if cible is None or getattr(cible, "navire", None) is not adverse:
            yield SignalAbandonne("On ne peut pas viser ce navire, capitaine.",
                    self.bruyant)

        yield SignalTermine()

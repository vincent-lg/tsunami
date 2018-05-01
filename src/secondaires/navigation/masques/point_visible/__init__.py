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


"""Fichier contenant le masque <point_visible>."""

from primaires.format.fonctions import contient, supprimer_accents
from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation
from secondaires.navigation.constantes import *
from secondaires.navigation.visible import Visible

class VPointVisible(Masque):

    """Masque <point_visible>.

    On attend un point observable en paramètre.

    """

    nom = "point_visible"
    nom_complet = "direction"

    def init(self):
        """Initialisation des attributs"""
        self.points = None
        self.retour = ""

    def repartir(self, personnage, masques, commande):
        """Répartition du masque."""
        point = liste_vers_chaine(commande)

        self.a_interpreter = point
        commande[:] = []
        masques.append(self)
        return True

    def valider(self, personnage, dic_masques):
        """Validation du masque"""
        Masque.valider(self, personnage, dic_masques)
        point = self.a_interpreter
        salle = personnage.salle
        if not hasattr(salle, "navire"):
            return False

        navire = salle.navire
        etendue = navire.etendue
        alt = etendue.altitude
        portee = get_portee(salle)
        if point:
            point = supprimer_accents(point)
            limite = 45
            precision = 5
            if point == "arriere":
                direction = 180
            elif point == "babord":
                direction = -90
            elif point == "tribord":
                direction = 90
            elif point in ("avant", "devant"):
                direction = 0
            else:
                raise ErreurValidation("|err|Direction invalide.|ff|")
        else:
            direction = 0
            limite = 90
            precision = 15

        # On récupère les points
        points = Visible.observer(personnage, portee, precision,
                {"": navire})
        msg = points.formatter(direction, limite)
        self.points = points
        self.retour = msg

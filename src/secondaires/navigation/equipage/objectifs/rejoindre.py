# -*-coding:Utf-8 -*

# Copyright (c) 2014 LE GOFF Vincent
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


"""Objectif rejoindre."""

from primaires.vehicule.vecteur import Vecteur
from secondaires.navigation.constantes import *
from secondaires.navigation.equipage.objectif import Objectif

class Rejoindre(Objectif):

    """Objectif rejoindre.

    Cet objectif demande à un équipage de rejoindre un point précisé
    en coordonnées. Le point indiqué doit être statique (il existe un
    objectif particulier pour les points mobiles, comme les navires, qui
    intègrent leur propre calcul).

    Cet objectif est responsable de trouver un chemin entre le point
    actuel et le point visé. Cela inclut le choix de chemins
    détournés si le chemin direct ne peut être pris avec des calculs qui
    peuvent être assez complexes pour déterminer la vitesse et direction
    des chemins intermédiaires.

    """

    def __init__(self, equipage, x=None, y=None, vitesse=1):
        Objectif.__init__(self, equipage, x, y, vitesse)
        self.x = x
        self.y = y
        self.vitesse = vitesse

    def afficher(self):
        """Méthode à redéfinir retournant l'affichage de l'objectif."""
        navire = self.navire
        position = navire.opt_position
        o_x = position.x
        o_y = position.y
        d_x = self.x
        d_y = self.y
        distance = Vecteur(d_x - o_x, d_y - o_y, 0)
        direction = (distance.direction - 90) % 360
        nb_brasses = round(distance.norme * CB_BRASSES)

        # On a plusieurs unités possibles
        if nb_brasses > 100000: # Très grande distance
            msg_dist = "plus de cent milles"
        elif nb_brasses > 50000:
            msg_dist = "plus de cinquante milles"
        elif nb_brasses > 10000:
            nb = round(nb_brasses / 10000) * 10
            msg_dist = "près de {} milles".format(nb)
        elif nb_brasses > 2000:
            nb = round(nb_brasses / 1000)
            msg_dist = "près de {} milles".format(nb)
        elif nb_brasses > 1000:
            msg_dist = "près d'un mille"
        elif nb_brasses > 200:
            nb = round(nb_brasses / 100)
            msg_dist = "près de {} encablures".format(nb)
        elif nb_brasses > 100:
            msg_dist = "près d'une encablure"
        elif nb_brasses > 50:
            nb = round(nb_brasses / 10) * 10
            msg_dist = "près de {} brasses".format(nb)
        elif nb_brasses > 20:
            nb = round(nb_brasses / 5) * 5
            msg_dist = "près de {} brasses".format(nb)
        elif nb_brasses > 10:
            nb = round(nb_brasses / 2) * 2
            msg_dist = "près de {} brasses".format(nb)
        else:
            msg_dist = "près d'une brasse"

        return "Cap sur {}°, à {}".format(direction, msg_dist)

    def get_distance(self):
        """Retourne la distance (Vecteur) entre le navire et la destination.

        Cette méthode crée un vecteur (class Vecteur définie dans
        le module primaire vehicule) qui représente la distance entre
        la position du navire et la destination.

        """
        navire = self.navire
        position = navire.opt_position
        o_x = position.x
        o_y = position.y
        d_x = self.x
        d_y = self.y
        distance = Vecteur(d_x - o_x, d_y - o_y, 0)
        return distance

    def transmettre_controles(self):
        """Donne les contrôles indiqués (vitesse et direction)."""
        equipage = self.equipage
        navire = self.navire
        distance = self.get_distance()
        direction = round(distance.direction)

        # Crée ou modifie les contrôles
        if equipage.controles.get("direction"):
            equipage.controles["direction"].direction = direction
        else:
            equipage.controler("direction", direction)

        if equipage.controles.get("vitesse"):
            equipage.controles["vitesse"].vitesse = self.vitesse
        else:
            equipage.controler("vitesse", self.vitesse)

    def creer(self):
        """L'objectif est créé.

        On crée les contrôles associés pour atteindre l'objectif
        visé, à savoir, rejoindre le point (x, y), sans s'inquiéter
        des obstacles éventuels.

        """
        equipage = self.equipage
        commandant = self.commandant
        if commandant is None:
            return

        self.transmettre_controles()

    def verifier(self, prioritaire):
        """Vérifie que l'objectif est toujours valide.

        Dans cette méthode, on vérifie :
            Qu'il n'y a aucun obstacle sur la trajectoire assignée
            Que le cap est toujours maintenu (si prioritaire)

        """
        pass

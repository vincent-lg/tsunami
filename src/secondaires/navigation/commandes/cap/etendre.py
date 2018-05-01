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


"""Package contenant le paramètre 'étendre' de la commande 'cap'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmEtendre(Parametre):

    """Paramètre 'étendre de la commande 'cap'"""

    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "étendre", "extend")
        self.schema = "<cle>"
        self.aide_courte = "ajoute un point au cap"
        self.aide_longue = \
            "Cette commande permet d'étendre le cap dont la clé est " \
            "passée en paramètre. Vous devez vous trouver sur un " \
            "navire : les coordonnées du navire seront considérées " \
            "comme les coordonnées du point à ajouter. Le trajet " \
            "entre le point de départ (ou le dernier point intermédiaire " \
            "actuel) et le nouveau point sera ajouté."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        cle = dic_masques["cle"].cle
        if cle not in importeur.navigation.trajets:
            personnage << "|err|Cette clé de cap n'existe pas.|ff|"
            return

        salle = personnage.salle
        if not hasattr(salle, "navire") or salle.navire is None:
            personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
            return

        navire = salle.navire
        if getattr(navire, "etendue", None) is None:
            personnage << "|err|Ce navire n'est pas dans une étendue " \
                    "d'eau.|ff|"
            return

        x = round(navire.position.x)
        y = round(navire.position.y)
        trajet = importeur.navigation.trajets[cle]
        if (x, y) in trajet.points:
            personnage << "|err|Ces points existent déjà dans ce cap.|ff|"
            return

        if trajet.point_depart == (x, y):
            personnage << "|err|Ces coordonnées sont définies en " \
                    "tant que point de départ du cap.|ff|"
            return

        a_x, a_y = trajet.point_depart
        if trajet.points:
            a_x, a_y = trajet.point_arrivee

        trajet.points[(a_x, a_y)] = (x, y)
        personnage << "Le cap {} a bien été étendu avec x={} et y={}.".format(
                repr(cle), x, y)

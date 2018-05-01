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


"""Fichier contenant le paramètre 'voir' de la commande 'cap'."""

from primaires.interpreteur.masque.parametre import Parametre
from primaires.vehicule.vecteur import Vecteur
from secondaires.navigation.constantes import get_nom_distance

class PrmVoir(Parametre):

    """Commande 'cap voir'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "voir", "view")
        self.schema = "<cle>"
        self.aide_courte = "affiche le détail d'un cap"
        self.aide_longue = \
            "Cette commande permet d'obtenir plus d'informations sur " \
            "un cap maritime : son point de départ, ses points " \
            "intermédiaires et son point d'arrivée."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        cle = dic_masques["cle"].cle
        if cle not in importeur.navigation.trajets:
            personnage << "|err|Ce cap n'existe pas.|ff|"
            return

        trajet = importeur.navigation.trajets[cle]

        # On réunit les informations à afficher
        etendue = trajet.etendue and trajet.etendue.cle or "|att|inconnue|ff|"
        depart = trajet.point_depart
        if depart is None:
            depart = "|att|inconnu|ff|"
        else:
            depart = "x={} y={}".format(*depart)

        msg = "Détail sur le cap {} :".format(cle)
        msg += "\nÉtendue : {}".format(etendue)
        msg += "\nDépart : {}".format(depart)
        if not trajet.points:
            msg += "\n  |att|Ce cap n'a pas de point d'arrivée.|ff|"
        else:
            x, y = trajet.point_depart
            msg += "\n  Points du cap :"
            for point in trajet.points.values():
                distance = Vecteur(point[0] - x, point[1] - y, 0)
                direction = round((distance.direction + 90) % 360)
                nom_direction = distance.nom_direction
                nom_distance = get_nom_distance(distance)
                msg += "\n    Vers x={} y={}, cap sur {}° ({}), {}".format(
                        point[0], point[1], direction, nom_direction,
                        nom_distance)
                x, y = point

            if trajet.point_depart == trajet.point_arrivee:
                msg += "\n  Ce trajet est refermé, donc circulaire."

        personnage << msg

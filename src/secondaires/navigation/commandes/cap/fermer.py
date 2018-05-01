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


"""Package contenant le paramètre 'fermer' de la commande 'cap'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmFermer(Parametre):

    """Paramètre 'fermer de la commande 'cap'"""

    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "fermer", "close")
        self.schema = "<cle>"
        self.aide_courte = "referme le cap"
        self.aide_longue = \
            "Cette commande permet de fermer un cap pour le rendre " \
            "circulaire (ou infini). Le dernier point du trajet " \
            "(considéré comme le point d'arrivée) sera relié au " \
            "point de départ pour créer une forme de boucle. Un " \
            "équipage ayant pour but de suivre un trajet fermé va " \
            "\"tourner en rond\", allant du point A au point B au " \
            "point C... pour finalement revenir au point A et " \
            "recommencer depuis le début."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        cle = dic_masques["cle"].cle
        if cle not in importeur.navigation.trajets:
            personnage << "|err|Cette clé de cap n'existe pas.|ff|"
            return

        trajet = importeur.navigation.trajets[cle]
        if not trajet.points:
            personnage << "|err|Ce cap n'a qu'un point de départ " \
                    "et ne peut être refermé.|ff|"
            return

        o_x, o_y = trajet.point_depart
        d_x, d_y = trajet.point_arrivee
        if (o_x, o_y) == (d_x, d_y):
            personnage << "|err|Ce cap est visiblement déjà refermé.|ff|"
            return

        trajet.points[(d_x, d_y)] = (o_x, o_y)
        personnage << "Le cap {} a bien été refermé.".format(repr(cle))

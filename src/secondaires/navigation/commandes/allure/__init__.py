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


"""Package contenant la commande 'allure'."""

from primaires.interpreteur.commande.commande import Commande
from primaires.vehicule.vecteur import get_direction
from secondaires.navigation.constantes import *

class CmdAllure(Commande):

    """Commande 'allure'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "allure", "trim")
        self.nom_categorie = "navire"
        self.aide_courte = "estime l'allure du navire"
        self.aide_longue = \
            "Cette commande permet d'estimer l'allure du navire. " \
            "Par allure, on n'entend pas sa vitesse mais l'angle " \
            "existant entre sa marche et la direction du vent. Ainsi, " \
            "cette commande est aussi utile pour estimer la direction " \
            "du vent. Cette direction est relative par rapport à " \
            "la direction du navire. Autrement dit, vous ne pourrez " \
            "pas dire que le vent vient du nord avec cette seule " \
            "commande, vous devrez utiliser une boussole pour ce faire."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        salle = personnage.salle
        if not hasattr(salle, "navire") or salle.navire is None:
            personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
            return

        navire = salle.navire

        # On récupère les directions
        nav_direction = navire.direction.direction
        vent = navire.vent

        if vent.mag == 0:
            personnage << "|err|Vous ne ressentez aucun souffle de vent.|ff|"
            return

        ven_direction = get_direction(vent)
        angle = (nav_direction - ven_direction) % 360
        precision = 10 # précision en degré
        angle = round(angle / precision) * precision
        tribord = True
        if angle > 180:
            angle = (180 - angle) % 180
            tribord = False

        cote = "tribord" if tribord else "bâbord"
        if angle == 0:
            msg_vent = "Le vent souffle directement sur l'arrière du navire."
        elif angle < 50:
            msg_vent = "Le vent souffle sur l'arrière et à {cote} " \
                    "du navire ({angle}°)."
        elif angle < 130:
            msg_vent = "Le vent souffle sur la hanche {cote} " \
                    "du navire ({angle}°)."
        elif angle < 180:
            msg_vent = "Le vent souffle sur l'avant et à {cote} " \
                    "du navire ({angle}°)."
        else:
            msg_vent = "Le vent souffle directement face au navire."


        angle_contraire = (-angle) % 180
        msg_vent = msg_vent.format(cote=cote, angle=angle_contraire)

        # Allure
        if angle > ALL_DEBOUT:
            msg_allure = "Le navire est au vent debout."
        elif angle > ALL_PRES:
            msg_allure = "Le navire est au près face au vent."
        elif angle > ALL_BON_PLEIN:
            msg_allure = "Le navire est au bon plein."
        elif angle > ALL_LARGUE:
            msg_allure = "Le navire est au largue, le vent portant par " \
                    "le travers."
        elif angle > ALL_GRAND_LARGUE:
            msg_allure = "Le navire est au grand largue."
        else:
            msg_allure = "Le navire est vent arrière."

        personnage << msg_vent + "\n" + msg_allure

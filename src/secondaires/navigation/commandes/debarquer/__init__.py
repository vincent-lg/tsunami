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


"""Package contenant la commande 'débarquer'."""

from math import sqrt

from primaires.interpreteur.commande.commande import Commande
from secondaires.navigation.constantes import *

class CmdDebarquer(Commande):

    """Commande 'debarquer'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "debarquer", "debark")
        self.nom_categorie = "navire"
        self.aide_courte = "débarque du navire"
        self.aide_longue = \
            "Cette commande permet de débarquer du navire sur lequel " \
            "on se trouve. On doit se trouver assez prêt d'une côte " \
            "pour débarquer dessus."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        salle = personnage.salle
        if not hasattr(salle, "navire") or salle.navire is None:
            personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
            return

        navire = salle.navire
        if navire.etendue is None:
            personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
            return

        personnage.agir("bouger")
        # On va chercher la salle la plus proche
        etendue = navire.etendue

        # On cherche la salle de nagvire la plus proche
        d_salle = None # la salle de destination
        distance = 2
        x, y, z = salle.coords.tuple()
        for t_salle in etendue.cotes.values():
            if t_salle.coords.z == z:
                t_x, t_y, t_z = t_salle.coords.tuple()
                t_distance = sqrt((x - t_x) ** 2 + (y - t_y) ** 2)
                if t_distance < distance and t_salle.nom_terrain in \
                        TERRAINS_ACCOSTABLES:
                    d_salle = t_salle
                    distance = t_distance

        if d_salle is None:
            personnage << "|err|Aucun quai n'a pu être trouvé à " \
                    "proximité.|ff|"
            return

        personnage.salle = d_salle
        personnage << "Vous sautez sur {}.".format(
                d_salle.titre.lower())
        personnage << d_salle.regarder(personnage)
        d_salle.envoyer("{{}} arrive en sautant depuis {}.".format(
                navire.nom), personnage)
        salle.envoyer("{{}} saute sur {}.".format(
                d_salle.titre.lower()), personnage)
        importeur.hook["personnage:deplacer"].executer(
                personnage, d_salle, None, 0)
        if not hasattr(d_salle, "navire") or d_salle.navire is None:
            personnage.envoyer_tip("N'oubliez pas d'amarrer votre navire " \
                    "avec %amarre% %amarre:attacher%.")

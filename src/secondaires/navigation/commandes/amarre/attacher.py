# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   raise of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this raise of conditions and the following disclaimer in the documentation
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


"""Fichier contenant le paramètre 'attacher' de la commande 'amarre'."""

from math import sqrt

from primaires.interpreteur.masque.parametre import Parametre
from secondaires.navigation.constantes import *

class PrmAttacher(Parametre):

    """Commande 'amarre attacher'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "attacher", "tide")
        self.aide_courte = "attache les amarres"
        self.aide_longue = \
            "Cette commande permet d'attacher les amarres d'un navire " \
            "proche. Vous ne devez pas l'entrer sur le navire, mais " \
            "sur le quai là où le navire doit être amarré."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        salle = personnage.salle
        if hasattr(salle, "navire"):
            personnage << "|err|Vous ne pouvez manipuler les amarres d'ici.|ff|"
            return

        # On va chercher le navire le plus proche
        etendue = salle.etendue
        if etendue is None or salle.coords.z != etendue.altitude or \
                salle.nom_terrain not in TERRAINS_QUAI:
            personnage << "|err|Vous n'êtes pas sur un quai.|ff|"
            return

        navires = [n for n in importeur.navigation.navires.values() if \
                n.etendue is etendue]

        # On cherche la salle de nagvire la plus proche
        d_salle = None # la salle de destination
        navire = None
        distance = 2
        x, y, z = salle.coords.tuple()
        for t_navire in navires:
            for t_salle in t_navire.salles.values():
                if t_salle.amarre and t_salle.amarre.attachee is salle:
                    personnage << "|err|Un navire est déjà amarré ici.|ff|"
                    return

                if t_salle.amarre and t_salle.amarre.attachee is None:
                    t_x, t_y, t_z = t_salle.coords.tuple()
                    t_distance = sqrt((x - t_x) ** 2 + (y - t_y) ** 2)
                    if t_distance < distance:
                        navire = t_navire
                        d_salle = t_salle
                        distance = t_distance

        if d_salle is None:
            personnage << "|err|Aucun navire n'a pu être trouvé à " \
                    "proximité.|ff|"
            return

        d_salle.amarre.attachee = salle
        navire.immobilise = True
        navire.vitesse.x = 0
        navire.vitesse.y = 0
        navire.vitesse.z = 0
        navire.acceleration.x = 0
        navire.acceleration.y = 0
        navire.acceleration.z = 0
        personnage << "Vous attachez solidement {} au quai.".format(
                navire.nom)
        salle.envoyer("{{}} attache solidement {} au quai.".format(
                navire.nom), personnage)

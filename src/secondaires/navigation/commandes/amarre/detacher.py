# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Fichier contenant le paramètre 'détacher' de la commande 'amarre'."""

from primaires.interpreteur.masque.parametre import Parametre
from secondaires.navigation.constantes import *

class PrmDetacher(Parametre):

    """Commande 'amarre detacher'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "détacher", "untide")
        self.aide_courte = "détache les amarres"
        self.aide_longue = \
            "Cette commande permet de détacher les amarres retenant un " \
            "navire. Vous ne devez pas l'entrer sur le navire-même " \
            "mais dans la salle où l'amarre est fixée, sur le quai."

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

        d_salle = None
        for t_navire in navires:
            for t_salle in t_navire.salles.values():
                if t_salle.amarre and t_salle.amarre.attachee is salle:
                    d_salle = t_salle
                    break

        if d_salle is None:
            personnage << "|err|Aucun navire n'est amarré ici.|ff|"
            return

        navire = d_salle.navire
        if navire.propreitaire and not navire.a_le_droit(personnage,
                si_present=True):
            personnage << "|err|Vous ne pouvez désamarrer ce " \
                    "navire.|ff|"
            return

        d_salle.amarre.attachee = None
        d_salle.navire.immobilise = False
        personnage << "Vous détachez l'amarre retenant {}.".format(
                d_salle.navire.nom)
        salle.envoyer("{{}} détache l'amarre retenant {}.".format(
                d_salle.navire.nom), personnage)

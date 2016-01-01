# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 LE GOFF Vincent
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


"""Fichier contenant le paramètre 'zéro' de la commande 'navire'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmZero(Parametre):

    """Commande 'navire zéro'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "zéro", "zero")
        self.schema = "(<cle_navire>)"
        self.aide_courte = "remet le compteur du navire à 0"
        self.aide_longue = \
            "Cette commande remet tout simplement le compteur du " \
            "navire à 0. Le compteur peut être utile pour estimer la " \
            "distance parcourue par un navire (que ce soit un navire " \
            "de joueur ou un navire automatique). Le compteur est " \
            "visible dans la commande %navire% %navire:info%."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        navire = dic_masques["cle_navire"]
        salle = personnage.salle
        if navire is None:
            if not hasattr(salle, "navire") or salle.navire is None:
                personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
                return

            navire = salle.navire
        else:
            navire = navire.navire

        navire.compteur = 0
        personnage << "Le compteur du navire {} a bien été mis à zéro.".format(
                navire.cle)

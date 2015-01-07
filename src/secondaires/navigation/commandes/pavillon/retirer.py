# -*-coding:Utf-8 -*

# Copyright (c) 2014 LE GOFF Vincent
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


"""Fichier contenant le paramètre 'retirer' de la commande 'pavillon'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmRetirer(Parametre):

    """Commande 'pavillon retirer'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "retirer", "down")
        self.aide_courte = "amène le pavillon"
        self.aide_longue = \
            "Cette commande permet de baisser le pavillon actuel " \
            "du navire. Elle ne prend aucun argument. Le pavillon " \
            "sera amené par le personnage entrant la commande."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        salle = personnage.salle
        if not hasattr(salle, "navire") or salle.navire is None or \
                salle.navire.etendue is None:
            personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
            return

        navire = salle.navire
        pavillon = navire.pavillon
        if pavillon is None:
            personnage << "|err|Aucun pavillon n'est actuellement hissé.|ff|"
            return

        navire.pavillon = None
        pavillon = importeur.objet.creer_objet(pavillon)
        navire.envoyer("{} est amené.".format(
                pavillon.get_nom().capitalize()))
        navire.envoyer_autour("{} amène {}.".format(
                navire.desc_survol, pavillon.get_nom().capitalize()), 35)
        personnage.ramasser_ou_poser(pavillon)

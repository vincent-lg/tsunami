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


"""Fichier contenant le paramètre 'tenir' de la commande 'gouvernail'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmTenir(Parametre):

    """Commande 'gouvernail tenir'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "tenir", "hold")
        self.aide_courte = "fait tenir le gouvernail"
        self.aide_longue = \
            "Cette commande permet de tenir le gouvernail. Il est " \
            "obligatoire de tenir un gouvernail pour virer. En outre, " \
            "un gouvernail qui n'est pas tenu ne sera pas du tout " \
            "stable et le navire pourra faire des embardées."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        salle = personnage.salle
        if not hasattr(salle, "navire") or salle.navire is None or \
                salle.navire.etendue is None:
            personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
            return

        navire = salle.navire
        gouvernail = salle.gouvernail
        if not gouvernail:
            personnage << "|err|Il n'y a pas de gouvernail ici.|ff|"
            return

        if gouvernail.tenu:
            if gouvernail.tenu is personnage:
                personnage << "|err|Vous tenez déjà ce gouvernail.|ff|"
            else:
                personnage << "|err|Ce gouvernail est déjà tenu par " \
                        "quelqu'un d'autre.|ff|"
        else:
            gouvernail.tenir(personnage)

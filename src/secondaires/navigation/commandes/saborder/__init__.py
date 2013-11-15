# -*-coding:Utf-8 -*

# Copyright (c) 2013 LE GOFF Vincent
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


"""Package contenant la commande 'saborder'."""

from primaires.interpreteur.commande.commande import Commande

class CmdSaborder(Commande):

    """Commande 'saborder'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "saborder", "scupper")
        self.tronquer = False
        self.nom_categorie = "navire"
        self.aide_courte = "saborde le navire sur lequel vous êtes"
        self.aide_longue = \
            "Cette commande permet de saborder le navire sur lequel vous " \
            "vous trouvez : si vous êtes dans une salle proche ou sous " \
            "la ligne de flotaison, vous pouvez créer une brèche qui, " \
            "avec un peu de temps (le temps nécessaire pour évaquer " \
            "le navire) fera sombrer l'embarquation."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        salle = personnage.salle
        if not hasattr(salle, "navire") or salle.navire is None:
            personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
            return

        navire = salle.navire
        if not salle.noyable:
            personnage << "|err|Vous ne pouvez ouvrir de brèche dans la " \
                    "coque ici.|ff|"
            return

        salle.noyer(30)
        personnage << "Vous créez une brèche dans la coque par laquelle " \
                "l'eau s'engouffre... ne restez pas là !"

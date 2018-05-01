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


"""Fichier contenant le paramètre 'lister' de la commande 'attitudes'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmLister(Parametre):

    """Commande 'attitudes lister'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "lister", "list")
        self.schema = ""
        self.aide_courte = "liste les attitudes existantes"
        self.aide_longue = \
            "Cette sous-commande offre une liste des attitudes existantes."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        attitudes = None
        if personnage.est_immortel():
            attitudes = type(self).importeur.communication.attitudes.values()
        else:
            attitudes = type(self).importeur.communication.attitudes_jouables
        if not attitudes:
            res = "|err|Il n'y a aucune attitude pour l'instant.|ff|"
        else:
            res = "+" + "-" * 77 + "+\n"
            res += "| |tit|" + "Attitudes en jeu".ljust(76) + "|ff||\n"
            res += "+" + "-" * 77 + "+\n"
            # On détermine la taille du tableau
            taille = 0
            liste_attitudes = []
            i = 0
            for att in sorted([att.cle for att in attitudes]):
                if i == 0:
                    liste_attitudes.append(att.ljust(19))
                    i += 1
                elif i == 3:
                    liste_attitudes[-1] += att.ljust(19) + "|"
                    i = 0
                else:
                    liste_attitudes[-1] += att.ljust(18)
                    i += 1
            if liste_attitudes[-1][-1] != "|":
                liste_attitudes[-1] = \
                        liste_attitudes[-1].ljust(74) + "|"
            res += "|   " + "\n|   ".join(liste_attitudes)
            res += "\n+".ljust(79, "-") + "+"
        personnage << res

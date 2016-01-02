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


"""Package contenant la commande 'qui'.

"""

from primaires.interpreteur.commande.commande import Commande
from primaires.format.fonctions import format_nb, supprimer_accents

class CmdQui(Commande):

    """Commande 'qui'.

    """

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "qui", "who")
        self.schema = ""
        self.aide_courte = "affiche les joueurs connectés"
        self.aide_longue = \
            "Cette commande permet d'afficher la liste des joueurs " \
            "actuellement connectés au MUD."

    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande"""
        joueurs = type(self).importeur.connex.joueurs_connectes
        if not joueurs:
            personnage.envoyer("Aucun joueur ne semble être présent, mais " \
                    "qui es-tu alors ?")
        else:
            noms_joueurs = {}
            for joueur in joueurs:
                imm = 0
                if joueur.est_immortel():
                    nom = "|cyc|~ " + joueur.nom + " ~|ff|"
                    imm = 9
                else:
                    nom = "  " + joueur.nom
                if joueur.afk:
                    raison = ""
                    if joueur.afk is not "afk":
                        raison = " '" + joueur.afk + "'"
                    nom += " (|rgc|AFK" + raison + "|ff|)"
                    noms_joueurs[joueur] = nom.ljust(48 + imm) + "|"
                else:
                    noms_joueurs[joueur] = nom.ljust(39 + imm) + "|"
            res = "+" + "-" * 40 + "+\n"
            res += "| |tit|Joueurs présents|ff|".ljust(50) + "|\n"
            res += "+" + "-" * 40 + "+"
            for j, nom in sorted(noms_joueurs.items(),
                    key=lambda c: supprimer_accents(c[0].nom)):
                res += "\n| " + nom
            res += "\n+" + "-" * 40 + "+\n"
            nb_joueurs = len(joueurs)
            nb_imms = len([j for j in noms_joueurs.keys() if j.est_immortel()])
            imms = ""
            if nb_imms > 0:
                s = "s" if nb_imms > 1 else ""
                nb = "un" if nb_imms == 1 else str(nb_imms)
                imms = ", dont |jn|{nb} immortel{s}|ff|".format(nb=nb, s=s)
            res += format_nb(nb_joueurs,
                    "{{nb}} joueur{{s}} connecté{{s}}{}.".format(imms))
            personnage << res

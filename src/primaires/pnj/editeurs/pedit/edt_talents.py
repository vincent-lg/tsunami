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


"""Ce fichier définit le contexte-éditeur EdtTalents."""

from primaires.interpreteur.editeur import Editeur
from primaires.format.fonctions import supprimer_accents

class EdtTalents(Editeur):

    """Contexte-éditeur d'édition des talents du PNJ."""

    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)

    def accueil(self):
        """Message d'accueil du contexte"""
        prototype = self.objet
        msg = "| |tit|" + "Édition des talents de {}".format(
                prototype).ljust(64)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += self.aide_courte
        msg += "Talents définis :\n"

        # Parcours des talents
        for cle_talent, niveau in sorted(prototype.talents.items()):
            talent = importeur.perso.talents.get(cle_talent)
            if talent is None:
                continue

            msg += "\n  " + talent.nom.capitalize().ljust(25)
            msg += " : " + str(niveau).rjust(3) + "%"

        if not prototype.talents:
             msg += "\n  Aucun."

        return msg

    def interpreter(self, msg):
        """Interprétation de l'éditeur."""
        prototype = self.objet
        arguments = msg.split(" ")
        if not arguments:
            return

        if len(arguments) < 2:
            self.pere << "|err|Entrez le nom du talent, un espace et " \
                    "le niveau.|ff|\nPar exemple |ent|maniement de " \
                    "l'épée 80|ff|"
        nom_talent = supprimer_accents(" ".join(arguments[:-1])).lower()
        niveau_talent = arguments[-1]

        try:
            niveau_talent = int(niveau_talent)
            assert 0 <= niveau_talent <= 100
        except (ValueError, AssertionError):
            self.pere << "|err|Valeur invalide.|ff|"
            return

        # On cherche le talent correspondant
        talent = None
        for t_talent in importeur.perso.talents.values():
            if supprimer_accents(t_talent.nom).lower() == nom_talent:
                talent = t_talent
                break

        if talent is None:
            self.pere << "|err|Talent introuvable : {}.|ff|".format(nom_talent)
            return

        if niveau_talent == 0:
            if talent.cle in prototype.talents:
                del prototype.talents[talent.cle]
                self.actualiser()
            else:
                self.pere << "|err|Ce talent n'est pas défini pour " \
                        "ce prototype de PNJ.|ff|"
                return
        else:
            prototype.talents[talent.cle] = niveau_talent
            self.actualiser()

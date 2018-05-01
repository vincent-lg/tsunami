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


"""Ce fichier définit le contexte-éditeur EdtSorts."""

from primaires.interpreteur.editeur import Editeur
from primaires.format.fonctions import supprimer_accents

class EdtSorts(Editeur):

    """Contexte-éditeur d'édition des sorts du PNJ."""

    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)

    def accueil(self):
        """Message d'accueil du contexte"""
        prototype = self.objet
        msg = "| |tit|" + "Édition des sorts de {}".format(
                prototype).ljust(64)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += self.aide_courte
        msg += "Sorts définis :\n"

        # Parcours des sorts
        for cle_sort, niveau in sorted(prototype.sorts.items()):
            sort = importeur.magie.sorts.get(cle_sort)
            if sort is None:
                continue

            msg += "\n  " + sort.nom.capitalize().ljust(25)
            msg += " : " + str(niveau).rjust(3) + "%"

        if not prototype.sorts:
             msg += "\n  Aucun."

        return msg

    def interpreter(self, msg):
        """Interprétation de l'éditeur."""
        prototype = self.objet
        arguments = msg.split(" ")
        if not arguments:
            return

        if len(arguments) < 2:
            self.pere << "|err|Entrez le nom du sort, un espace et " \
                    "le niveau.|ff|\nPar exemple |ent|boule de " \
                    "glace 80|ff|"
        nom_sort = supprimer_accents(" ".join(arguments[:-1])).lower()
        niveau_sort = arguments[-1]

        try:
            niveau_sort = int(niveau_sort)
            assert 0 <= niveau_sort <= 100
        except (ValueError, AssertionError):
            self.pere << "|err|Valeur invalide.|ff|"
            return

        # On cherche le sort correspondant
        sort = None
        for t_sort in importeur.magie.sorts.values():
            if supprimer_accents(t_sort.nom).lower() == nom_sort:
                sort = t_sort
                break

        if sort is None:
            self.pere << "|err|Sort introuvable : {}.|ff|".format(nom_sort)
            return

        if niveau_sort == 0:
            if sort.cle in prototype.sorts:
                del prototype.sorts[sort.cle]
                self.actualiser()
            else:
                self.pere << "|err|Ce sort n'est pas défini pour " \
                        "ce prototype de PNJ.|ff|"
                return
        else:
            prototype.sorts[sort.cle] = niveau_sort
            self.actualiser()

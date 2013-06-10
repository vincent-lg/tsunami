# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   mine of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this mine of conditions and the following disclaimer in the documentation
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


"""Package contenant la commande 'sorts miens'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmMiens(Parametre):

    """Commande 'sorts miens'.

    """

    def __init__(self):
        """Constructeur de la commande"""
        Parametre.__init__(self, "miens", "mine")
        self.aide_courte = "liste vos sorts"
        self.aide_longue = \
            "Cette commande vous permet de consulter votre niveau actuel " \
            "dans chacun des sorts que vous connaissez."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        ret = "Vos sorts :\n"
        sorts = {}
        for cle, niveau in personnage.sorts.items():
            try:
                sort = importeur.magie.sorts[cle]
            except KeyError:
                continue

            if cle not in personnage.sorts_verrouilles:
                sorts[sort.nom] = niveau
            else:
                sorts[sort.nom + " (verrouillé)"] = niveau

        for nom, niveau in sorted(sorts.items()):
            ret += "\n  {:<35} - {:>3}%".format(nom, niveau)

        if not sorts:
            ret = "Vous ne connaissez aucun sort... pour l'instant."

        personnage << ret

# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Fichier contenant le paramètre 'mien' de la commande 'rapport'."""

from primaires.interpreteur.masque.parametre import Parametre
from primaires.format.fonctions import couper_phrase

class PrmMien(Parametre):

    """Commande 'rapport mien'
    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "mien", "mine")
        self.schema = ""
        self.groupe = "administrateur"
        self.aide_courte = "renvoie vos rapports assignés"
        self.aide_longue = \
            "Cette commande liste les rapports qui vous sont assignés."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        rapports = [r for r in list(importeur.rapport.rapports.values()) \
                if r.ouvert and r.assigne_a is personnage]
        if not rapports:
            personnage << "|err|Aucun rapport ne vous est assigné.|ff|"
            return
        l_id = max([len(str(r.id)) for r in rapports] + [2])
        l_createur = max([len(r.createur.nom) if r.createur else 7 \
                for r in rapports] + [8])
        l_titre = max([len(r.titre) for r in rapports] + [5])
        l_titre_max = 70 - l_createur - l_id # longueur max d'un titre
        ljust_titre = min(l_titre_max, l_titre)
        lignes = [
            "+" + "-" * (l_id + l_createur + ljust_titre + 8) + "+",
            "| |tit|" + "ID".ljust(l_id) + "|ff| | |tit|" \
                    + "Créateur".ljust(l_createur) + "|ff| | |tit|" \
                    + "Titre".ljust(ljust_titre) + "|ff| |",
            "+" + "-" * (l_id + l_createur + ljust_titre + 8) + "+",
        ]
        for rapport in rapports:
            if l_titre_max < l_titre:
                titre = couper_phrase(rapport.titre, l_titre_max)
            else:
                titre = rapport.titre
            createur = rapport.createur and rapport.createur.nom or \
                    "inconnu"
            lignes.append("| |vrc|" + str(rapport.id).ljust(l_id) \
                    + "|ff| | " + createur.ljust(l_createur) + " | " \
                    + titre.ljust(ljust_titre) + " |")
        lignes.append(
            "+" + "-" * (l_id + l_createur + ljust_titre + 8) + "+")
        personnage << "\n".join(lignes)

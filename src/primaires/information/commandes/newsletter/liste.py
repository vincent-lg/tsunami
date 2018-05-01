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


"""Fichier contenant le paramètre 'liste' de la commande 'newsletter'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmListe(Parametre):

    """Commande 'newsletter liste'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "liste", "list")
        self.aide_courte = "liste les news letters existantes"
        self.aide_longue = \
            "Cette commande liste les news letters existantes ainsi que " \
            "leur statut."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre."""
        newsletters = list(importeur.information.newsletters)
        if len(newsletters) == 0:
            personnage << "Aucune news letter n'a été créé pour l'instant."
            return

        lignes = [
            "+----|------------+------------+---------------------------|",
            "| ID | Date       | Statut     | Sujet                     |",
        ]
        lignes.append(lignes[0])
        nid = 1
        for newsletter in newsletters:
            date = str(newsletter.date_creation.date())
            statut = newsletter.statut
            sujet = newsletter.sujet
            if len(sujet) > 25:
                sujet = sujet[:22] + "..."

            lignes.append("| {:>2} | {} | {:<10} | {:<25} |".format(
                    nid, date, statut, sujet))
            nid += 1

        lignes.append(lignes[0])
        personnage << "\n".join(lignes)

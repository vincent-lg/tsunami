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


"""Package contenant la commande 'auberge liste'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmListe(Parametre):

    """Commande 'auberge liste'"""

    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "liste", "list")
        self.aide_courte = "affiche les auberges existantes"
        self.aide_longue = \
            "Cette commande permet de lister les auberges existantes."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande."""
        auberges = sorted([a for a in importeur.auberge.auberges.values()],
                key=lambda a: a.cle)
        if auberges:
            en_tete = "+-" + "-" * 15 + "-+-" + "-" * 25 + "-+-" + \
                    "-" * 8 + "-+-" + "-" * 6 + "-+"
            msg = en_tete + "\n"
            msg += "| Clé             | Salle                    | " \
                    "Chambres | Occupé |\n"
            msg += en_tete
            for auberge in auberges:
                cle = auberge.cle
                ident = auberge.ident_comptoir
                nb_chambres = len(auberge.chambres)
                pct_occupation = auberge.pct_occupation
                msg += "\n| {:<15} | {:<25} | {:>8} | {:>5}% |".format(
                        cle, ident, nb_chambres, pct_occupation)

            msg += "\n" + en_tete
            personnage << msg
        else:
            personnage << "Aucune auberge n'existe pour l'heure."

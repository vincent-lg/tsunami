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


"""Ce fichier définit le contexte-éditeur EdtAptitudes."""

from primaires.format.fonctions import supprimer_accents
from primaires.interpreteur.editeur import Editeur
from primaires.format.fonctions import supprimer_accents
from secondaires.navigation.equipage.constantes import *

class EdtAptitudes(Editeur):

    """Contexte-éditeur d'édition des aptitudes d'un matelot."""

    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)

    def accueil(self):
        """Message d'accueil du contexte"""
        fiche = self.objet
        aptitudes = []
        for cle, niveau in fiche.aptitudes.items():
            nom = NOMS_APTITUDES[cle]
            niveau = NOMS_NIVEAUX[niveau]
            aptitudes.append((nom, niveau))

        aptitudes.sort()
        msg = "| |tit|" + "Édition des aptitudes du matelot {}".format(
                fiche.cle).ljust(64)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += "Entrez un nom d'aptitude, un espace et le niveau, " \
                "entre |cmd|1|ff|\n(médiocre) et |cmd|6|ff| " \
                "(excellent). Pour connaître la liste\ndes aptitudes, " \
                "entrez |cmd|?|ff|. Pour supprimer une aptitude,\n" \
                "précisez |cmd|0|ff| en niveau.\n\n"
        msg += "Aptitudes actuelles :"
        if aptitudes:
            for nom, niveau in aptitudes:
                msg += "\n  " + nom.ljust(15) + " (" + niveau + ")"
        else:
            msg += "\n  |att|Aucune|ff|"

        return msg

    def interpreter(self, msg):
        """Interprétation de l'éditeur."""
        fiche = self.objet
        if msg == "?":
            self.pere.envoyer(self.afficher_aptitudes())
            return

        couple = msg.split()
        nom = couple[:-1]
        niveau = couple[-1]
        nom = " ".join(nom)
        if not nom:
            self.pere << "|err|Précisez un nom d'aptitude (entrez " \
                    "|cmd|?|err| si vous ne les connaissez pas).|ff|"
            return

        try:
            cle = CLES_APTITUDES[supprimer_accents(nom).lower()]
        except KeyError:
            self.pere << "|err|Aptitude inconnue. Entrez |cmd|?|err| " \
                    "pour connaître la liste.|ff|"
            return

        try:
            niveau = int(niveau)
            assert niveau >= 0 and niveau < 7
        except (ValueError, AssertionError):
            self.pere << "|err|Niveau invalide.|ff|"
            return

        if niveau == 0:
            if cle in fiche.aptitudes:
                del fiche.aptitudes[cle]
        else:
            fiche.aptitudes[cle] = niveau

        self.actualiser()

    def afficher_aptitudes(self):
        """Retourne une chaîne représentant les aptitudes."""
        aptitudes = []
        for nom in NOMS_APTITUDES.values():
            aptitudes.append(nom)

        msg = "Liste des aptitudes possibles :\n  "
        msg += "\n  ".join(sorted(aptitudes))
        return msg

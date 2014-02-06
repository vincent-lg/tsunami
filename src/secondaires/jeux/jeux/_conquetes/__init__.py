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


"""Jeu conquêtes (stratégie)."""

import re
from random import *

from .. import BaseJeu

# Constantes
RE_CASE = re.compile(r" +([A-Za-z][0-9]{1,2})$")

class Jeu(BaseJeu):

    """Ce jeu définit le jeu de conquêtes, un jeu de stratégie.

    Les joueurs peuvent évoluer sur une carte plus ou moins grande
    (minime par défaut). Les différentes ressources sont obtenues
    naturellement ou produites par des bâtiments. Les joueurs peuvent
    également créer des unités qui servent à la défense du territoire
    ou à l'attaque d'ennemis. Quand un joueur n'a plus de ressource,
    il a perdu. Le dernier restant remporte la partie.

    """

    nom = "conquetes"
    def init(self):
        """Construction du jeu."""
        self.nb_joueurs_min = 2
        self.nb_joueurs_max = 6
        self.tour = 1
        self.perdus = []

    def peut_commencer(self):
        """La partie peut-elle commencer ?"""
        if not self.partie.en_cours:
            self.partie.envoyer(
                    "|err|La partie n'a pas encore commencée.|ff|")
            return False

        return True

    def peut_jouer(self, personnage):
        """Le personnage peut-il jouer ?"""
        if personnage in self.perdus:
            personnage << "Vous passez votre tour."
            return False

        return True

    def jouer(self, personnage, msg):
        """Joue au jeu.

        Les possibilités sont :
            p : passer son tour

        """
        if msg.lower() == "p":
            return True

        personnage.envoyer(
                "|err|Utilisez la commande |cmd|p|err| pour passer " \
                "votre tour.|ff|")
        return False

    def trouver_case(self, personnage, reste):
        """Retourne la case précisé (ou non) dans le reste.

        Si la case n'est pas précisée dans le reste et si il n'y a
        qu'une seule case disponible, la retourne.

        """
        exp = RE_CASE.search(reste)
        if exp:
            coords = exp.groups()[0].capitalize()
            if coords not in self.plateau.cases:
                personnage << "|err|Coordonnées '{}' inconnues.|ff|".format(
                        coords))
                return

            case = self.plateau.cases[coords]
            reste = reste[:-len(coords)].rstrip()
            return reste, case

        if len(self.plateau.cases) == 1:
            return reste, tuple(self.plateau.cases.values())[0]

        personnage << "|err|Précisez les coordonnées de la case visée.|ff|"
        return reste, None

    def opt_c(self, personnage, reste):
        """Permet de construire un bâtiment sur une case.

        Format possible du reste:
            [<nombre>) <nom du bâtiment> (<case>)

        La case n'a pas besoin d'être mentionnée si il n'y en a qu'une.

        """
        if not reste:
            personnage << "|err|Précisez au moins un nom de bâtiment.|ff|"
            return

        nombre = reste.split(" ")[0]
        if nombre.isdigit:
            nombre = int(nombre)
            reste = " ".join(reste.split(" ")[1:])
        else:
            nombre = 1

        if nombre <= 0:
            personnage << "|err|Le nombre de bâtiments précisé est " \
                    "négatif ou nul.")
            return

        reste, case = self.trouver_case(personnage, reste)

        if not reste:
            personnage << "|err|Précisez un nom de bâtiment.|ff|"
            return

        if case:
            case.construire_batiment(personnage, reste)

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


"""Jeu de l'oie."""

from random import randint

from .. import BaseJeu

class Jeu(BaseJeu):

    """Ce jeu définit le jeu de l'oie.

    Il est rattaché au plateau l'oie.

    """

    nom = "jeu de l'oie"
    def init(self):
        """Construction du jeu."""
        self.nb_joueurs_min = 2
        self.nb_joueurs_max = 6
        self.joueurs = {}
        self.hotellerie = {}
        self.puits = None
        self.prison = None
        self.pions = {}

    def peut_commencer(self):
        """La partie peut-elle commencer ?"""
        pions = list(self.pions.keys())
        joueurs = list(self.partie.joueurs)
        if len(pions) == len(joueurs):
            return True
        else:
            self.partie.envoyer("|err|Tous les joueurs n'ont pas choisis " \
                    "leur pion.|ff|")
            return False

    def peut_jouer(self, personnage):
        """Le personnage peut-il jouer ?"""
        pion = self.pions[personnage]
        if personnage in self.hotellerie.keys():
            self.partie.envoyer("|err|Le pion {} passe son tour.|ff|".format(
                    pion.couleur))
            self.hotellerie[personnage] = self.hotellerie[personnage] - 1
            if self.hotellerie[personnage] <= 0:
                del self.hotellerie[personnage]
            return False
        elif personnage is self.puits:
            self.partie.envoyer("|err|Le pion {} est dans le " \
                    "puits.|ff|".format(pion.couleur))
            return False
        elif personnage is self.prison:
            self.partie.envoyer("|err|Le pion {} est en " \
                    "prison.|ff|".format(pion.couleur))
            return False

        return True

    def jouer(self, personnage, msg):
        """Joue au jeu.

        On entre simplement la lettre L pour jouer.

        """
        if msg.lower() == "l":
            de = randint(1, 6)
            personnage << "Vous lancez les dés et obtenez {}.".format(de)
            self.partie.envoyer(
                    "{{}} lance les dés et obtient {}.".format(
                    de), personnage)
            self.avancer(personnage, de)
            return True
        else:
            personnage << "|err|Coup invalide.|ff|"
            return False

    def get_position(self, personnage):
        """Retourne la position du personnage."""
        return self.joueurs.get(personnage, 0)

    def avancer(self, personnage, x):
        """Avance de x cases."""
        pos = self.get_position(personnage)
        rec = 0
        if pos + x >= len(self.plateau.cases):
            rec = x - (len(self.plateau.cases) - 1 - pos)
            x -= rec

        msg = "Vous avancez d"
        pion = self.pions[personnage]
        msg_a = "Le pion {} avance d".format(pion.couleur)
        if x == 1:
            msg += "'une case"
            msg_a += "'une case"
        else:
            msg += "e {} cases".format(x)
            msg_a += "e {} cases".format(x)

        if rec == 0:
            msg += "."
            msg_a += "."
        elif rec == 1:
            msg += " et reculez d'une case."
            msg_a += " et reculez d'une case."
        else:
            msg += " et reculez de {} cases.".format(rec)
            msg_a += " et reculez de {} cases.".format(rec)

        personnage << msg
        self.partie.envoyer(msg_a, personnage)
        self.placer(personnage, pos + x - rec, x + rec)

    def placer(self, personnage, position, coup=0):
        """Place le personnage sur la case."""
        self.joueurs[personnage] = position
        self._enregistrer()
        case = self.plateau.cases[self.get_position(personnage)]
        case.arrive(self, self.plateau, self.partie, personnage, coup)

    # la méthode opt_p
    def opt_p(self, personnage, message):
        """Choisit un pion."""
        message = message.strip()
        partie = self.partie
        if partie.en_cours:
            personnage << "|err|La partie a commencé.|ff|"
            return

        if message:
            pion = self.plateau.pions.get(message)
            if pion is None:
                personnage << "|err|Ce pion n'existe pas.|ff|"
            elif pion in self.pions.values():
                personnage << "|err|Ce pion est déjà pris.|ff|"
            else:
                self.pions[personnage] = pion
                self._enregistrer()
                personnage << "Vous choisissez le pion {}.".format(
                        pion.couleur)
                partie.envoyer("{{}} choisit le pion {}.".format(pion.couleur),
                        personnage)
        else:
            pions = ["{}  {}".format(p.numero, p.couleur) for p in \
                    self.plateau.pions.values() if p not in \
                    self.pions.values()]
            pions.sort()
            personnage << "Pions disponibles :\n\n  " + "\n  ".join(pions)

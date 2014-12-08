# -*-coding:Utf-8 -*

# Copyright (c) 2014 LE GOFF Vincent
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


import unittest

from test.primaires.connex.static.commande import TestCommande
from test.primaires.joueur.static.joueur import ManipulationJoueur
from test.primaires.scripting.static.scripting import ManipulationScripting

class TestTrier(TestCommande, ManipulationJoueur, ManipulationScripting,
        unittest.TestCase):

    """Tests unitaires de l'action scripting 'trier'."""

    def test_nombres(self):
        """Trie d'une liste de nombres."""
        joueur = self.creer_joueur("simple", "Kredh")
        with self.scripter(joueur.salle, "dit") as test:
            test.ajouter_instructions("""
                nombres = liste(8, -2, -10, 1)
                trier nombres
                indice1 = indice(-10, nombres)
                indice2 = indice(1, nombres)
                dire personnage "${indice1} ${indice2}"
            """)
            msg = self.entrer_commande(joueur, "dire hey oh")
            self.assertEqual(msg, "Vous dites : hey oh\n1 3")

        self.supprimer_joueur(joueur)

    def test_inverse(self):
        """Trie inverse d'une liste de nombres."""
        joueur = self.creer_joueur("simple", "Kredh")
        with self.scripter(joueur.salle, "dit") as test:
            test.ajouter_instructions("""
                nombres = liste(8, -2, -10, 1)
                trier nombres "inverse"
                indice1 = indice(-10, nombres)
                indice2 = indice(1, nombres)
                dire personnage "${indice1} ${indice2}"
            """)
            msg = self.entrer_commande(joueur, "dire hey oh")
            self.assertEqual(msg, "Vous dites : hey oh\n4 2")

        self.supprimer_joueur(joueur)

    def test_alphabetique(self):
        """Trie de mots."""
        joueur = self.creer_joueur("simple", "Kredh")
        with self.scripter(joueur.salle, "dit") as test:
            test.ajouter_instructions("""
                mots = liste("placard", "oiseau", "tracteur", "aquarium")
                trier mots
                indice1 = indice("aquarium", mots)
                indice2 = indice("tracteur", mots)
                dire personnage "${indice1} ${indice2}"
            """)
            msg = self.entrer_commande(joueur, "dire hey oh")
            self.assertEqual(msg, "Vous dites : hey oh\n1 4")

        self.supprimer_joueur(joueur)

    def test_complexe(self):
        """Trie d'une liste contenant plusieurs données."""
        joueur = self.creer_joueur("simple", "Kredh")
        with self.scripter(joueur.salle, "dit") as test:
            test.ajouter_instructions("""
                donnees = liste()
                ajouter liste(1, "flacon") donnees
                ajouter liste(-8, "bouteille") donnees
                trier donnees
                dire personnage "Sans erreur"
            """)
            msg = self.entrer_commande(joueur, "dire hey oh")
            self.assertEqual(msg, "Vous dites : hey oh\nSans erreur")

        self.supprimer_joueur(joueur)

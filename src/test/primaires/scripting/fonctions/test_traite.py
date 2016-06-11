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


import unittest

from test.primaires.connex.static.commande import TestCommande
from test.primaires.joueur.static.joueur import ManipulationJoueur
from test.primaires.scripting.static.scripting import ManipulationScripting

class TestTraite(TestCommande, ManipulationJoueur, ManipulationScripting,
        unittest.TestCase):

    """Tests unitaires de la fonction scripting 'traite'."""

    def test_majuscule(self):
        """Teste la mise en majuscule."""
        joueur = self.creer_joueur("simple", "Kredh")
        with self.scripter(joueur.salle, "dit") as test:
            test.ajouter_instructions("""
                essai = "essai"
                essai = traite(essai, "majuscule")
                dire personnage essai
            """)
            msg = self.entrer_commande(joueur, "dire k")
            self.assertEqual(msg, "Vous dites : k\nESSAI")

        self.supprimer_joueur(joueur)

    def test_minuscule(self):
        """Teste la mise en minuscule."""
        joueur = self.creer_joueur("simple", "Kredh")
        with self.scripter(joueur.salle, "dit") as test:
            test.ajouter_instructions("""
                essai = "ESSAI"
                essai = traite(essai, "minuscule")
                dire personnage essai
            """)
            msg = self.entrer_commande(joueur, "dire k")
            self.assertEqual(msg, "Vous dites : k\nessai")

        self.supprimer_joueur(joueur)

    def test_capital(self):
        """Teste la mise en capital."""
        joueur = self.creer_joueur("simple", "Kredh")
        with self.scripter(joueur.salle, "dit") as test:
            test.ajouter_instructions("""
                essai = "on y peut rien"
                essai = traite(essai, "capital")
                dire personnage essai
            """)
            msg = self.entrer_commande(joueur, "dire k")
            self.assertEqual(msg, "Vous dites : k\nOn Y Peut Rien")

        self.supprimer_joueur(joueur)

    def test_sans_accents(self):
        """Teste la suppression d'accents."""
        joueur = self.creer_joueur("simple", "Kredh")
        with self.scripter(joueur.salle, "dit") as test:
            test.ajouter_instructions("""
                essai = "une chaîne accentuée"
                essai = traite(essai, "sans_accents")
                dire personnage essai
            """)
            msg = self.entrer_commande(joueur, "dire k")
            self.assertEqual(msg, "Vous dites : k\nune chaine accentuee")

        self.supprimer_joueur(joueur)

    def test_lisser(self):
        """Teste le lissage de chaîne."""
        joueur = self.creer_joueur("simple", "Kredh")
        with self.scripter(joueur.salle, "dit") as test:
            test.ajouter_instructions("""
                essai = "Une porte de acier."
                essai = traite(essai, "lisser")
                dire personnage essai
            """)
            msg = self.entrer_commande(joueur, "dire k")
            self.assertEqual(msg, "Vous dites : k\nUne porte d'acier.")

        self.supprimer_joueur(joueur)

    def test_multiple(self):
        """Teste d'opérations multiples."""
        joueur = self.creer_joueur("simple", "Kredh")
        with self.scripter(joueur.salle, "dit") as test:
            test.ajouter_instructions("""
                essai = "une chaîne de caractères"
                essai = traite(essai, "capital sans_accents")
                dire personnage essai
            """)
            msg = self.entrer_commande(joueur, "dire k")
            self.assertEqual(msg, "Vous dites : k\nUne Chaine De Caracteres")

        self.supprimer_joueur(joueur)

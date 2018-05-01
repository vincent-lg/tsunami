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


import unittest

from test.primaires.connex.static.commande import TestCommande
from test.primaires.joueur.static.joueur import ManipulationJoueur
from test.primaires.scripting.static.scripting import ManipulationScripting

class TestSalles(TestCommande, ManipulationJoueur, ManipulationScripting,
        unittest.TestCase):

    """Tests unitaires de la fonction scripting 'salles'."""

    def test_toutes_salles(self):
        """Teste la récupération de toutes les salles."""
        joueur = self.creer_joueur("simple", "Kredh")
        with self.scripter(joueur.salle, "dit") as test:
            test.ajouter_instructions("""
                salles = salles()
                taille = longueur(salles)
                si taille > 3:
                    dire personnage "Plus de 3."
                sinon:
                    dire personnage "Moins de 3."
                finsi
            """)
            msg = self.entrer_commande(joueur, "dire k")
            self.assertEqual(msg, "Vous dites : k\nPlus de 3.")

        self.supprimer_joueur(joueur)

    def test_zone_salles(self):
        """Teste la récupération des salles d'une zone."""
        joueur = self.creer_joueur("simple", "Kredh")
        with self.scripter(joueur.salle, "dit") as test:
            test.ajouter_instructions("""
                salles = salles("autre")
                taille = longueur(salles)
                dire personnage "${taille}"
            """)
            msg = self.entrer_commande(joueur, "dire k")
            self.assertEqual(msg, "Vous dites : k\n3")

        self.supprimer_joueur(joueur)

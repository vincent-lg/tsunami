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


"""Fichier définissant les unittest de membres de guilde."""

import unittest

from secondaires.crafting.guilde import *
from test.primaires.joueur.static.joueur import ManipulationJoueur

class TestMembre(ManipulationJoueur, unittest.TestCase):

    """Unittest des membres de guilde."""

    def test_creation(self):
        """Test l'ajout de membres à des guildes vides."""
        joueur = self.creer_joueur("simple", "Fiche")
        guilde = importeur.crafting.creer_guilde("forgerons")
        with self.assertRaises(GuildeSansRang):
            guilde.rejoindre(joueur)

        importeur.crafting.supprimer_guilde("forgerons")
        self.supprimer_joueur(joueur)

    def test_doublon(self):
        """Test l'ajout du même membre deux fois."""
        joueur = self.creer_joueur("simple", "Kredh")
        guilde = importeur.crafting.creer_guilde("forgerons")
        guilde.ajouter_rang("apprenti")
        guilde.rejoindre(joueur)
        with self.assertRaises(DejaMembre):
            guilde.rejoindre(joueur)

        importeur.crafting.supprimer_guilde("forgerons")
        self.supprimer_joueur(joueur)

    def test_points_insuffisants(self):
        """Test l'ajout d'un membre qui n'a pas assez de points."""
        # On a 10 points disponibles mais le rang à créer en demandera 15
        importeur.crafting.membres.points_guilde = 10

        joueur = self.creer_joueur("simple", "Kredh")
        guilde = importeur.crafting.creer_guilde("forgerons")
        rang = guilde.ajouter_rang("apprenti")
        rang.points_guilde = 15

        with self.assertRaises(PointsGuildeInsuffisants):
            guilde.rejoindre(joueur)

        importeur.crafting.supprimer_guilde("forgerons")
        self.supprimer_joueur(joueur)

    def test_points_consommes(self):
        """Test la bonne consommation des points de guilde."""
        importeur.crafting.membres.points_guilde = 10

        joueur = self.creer_joueur("simple", "Kredh")
        guilde = importeur.crafting.creer_guilde("forgerons")
        rang = guilde.ajouter_rang("apprenti")
        rang.points_guilde = 5
        avant = importeur.crafting.get_points_guilde_disponibles(joueur)
        guilde.rejoindre(joueur)
        apres = importeur.crafting.get_points_guilde_disponibles(joueur)
        self.assertEqual(avant, 10)
        self.assertEqual(apres, 5)
        importeur.crafting.supprimer_guilde("forgerons")
        self.supprimer_joueur(joueur)

    def test_promotion_sans_rang(self):
        """Essaye de promouvoir un joueur quand il n'y a qu'un rang."""
        joueur = self.creer_joueur("simple", "Kredh")
        guilde = importeur.crafting.creer_guilde("forgerons")
        rang = guilde.ajouter_rang("apprenti")
        rang.points_guilde = 5
        guilde.rejoindre(joueur)
        with self.assertRaises(RangIntrouvable):
            guilde.promouvoir(joueur)

        importeur.crafting.supprimer_guilde("forgerons")
        self.supprimer_joueur(joueur)

    def test_promotion_avec_rang(self):
        """Essaye de promouvoir un joueur sans erreur."""
        importeur.crafting.membres.points_guilde = 10

        joueur = self.creer_joueur("simple", "Kredh")
        guilde = importeur.crafting.creer_guilde("forgerons")
        apprenti = guilde.ajouter_rang("apprenti")
        apprenti.points_guilde = 2
        artisan = guilde.ajouter_rang("artisan")
        artisan.points_guilde = 4

        # On fait rejoindre et promouvoir le joueur
        avant = importeur.crafting.get_points_guilde_disponibles(joueur)
        guilde.rejoindre(joueur)
        a_apprenti = importeur.crafting.get_points_guilde_disponibles(joueur)
        guilde.promouvoir(joueur)
        a_artisan = importeur.crafting.get_points_guilde_disponibles(joueur)
        guilde.quitter(joueur)
        apres = importeur.crafting.get_points_guilde_disponibles(joueur)

        # Le joueur devait avoir 10 points
        # Puis 8 en devenant apprenti
        # Puis 4 en devenant artisan
        # Puis 9 (10 - 1 de malus)
        self.assertEqual(avant, 10)
        self.assertEqual(a_apprenti, 8)
        self.assertEqual(a_artisan, 4)
        self.assertEqual(apres, 9)

        importeur.crafting.supprimer_guilde("forgerons")
        self.supprimer_joueur(joueur)

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


"""Fichier définissant les unittest de talents de guilde."""

import unittest

from test.primaires.joueur.static.joueur import ManipulationJoueur

class TestTalent(ManipulationJoueur, unittest.TestCase):

    """Unittest des talents de guilde."""

    def test_creation(self):
        """Test l'ajout de talents à des guildes vides."""
        joueur = self.creer_joueur("simple", "Fiche")

        # Création d'une guilde avec deux talents
        guilde = importeur.crafting.creer_guilde("forgerons")
        guilde.ajouter_rang("apprenti")
        guilde.ajouter_talent("forge", "talent de la forge", False)
        guilde.ajouter_talent("ciseau", "art du ciseau", False)
        guilde.ouvrir()
        avant = joueur.points_apprentissage_max

        # Rejoindre la guilde devrait donner 100 points d'apprentissage de plus
        guilde.rejoindre(joueur)
        apres = joueur.points_apprentissage_max
        self.assertEqual(avant + 100, apres)

        # Nettoyage après le test
        importeur.crafting.supprimer_guilde("forgerons")
        self.supprimer_joueur(joueur)

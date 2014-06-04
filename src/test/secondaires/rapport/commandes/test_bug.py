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


"""Tests de la commande bug."""

import re
import unittest

from test.primaires.connex.static.commande import TestCommande
from test.primaires.joueur.static.joueur import ManipulationJoueur

class TestBug(TestCommande, ManipulationJoueur, unittest.TestCase):

    """Tests unitaires de la commande 'bug'."""

    def test_simple(self):
        """Rapporte un bug."""
        joueur = self.creer_joueur("simple", "Kredh")
        description = "Voici un bug très problématique"
        msg = self.entrer_commande(joueur,
                "bug {}".format(description))

        # On vérifie que le rapport a bien été créé
        no = re.search(r"^Le rapport sans titre \#(\d+) a bien été envoyé\.$",
                msg)
        self.assertIsNotNone(no)
        no = int(no.groups()[0])
        rapport = importeur.rapport.rapports[no]
        self.assertEqual(str(rapport.description), description)
        self.supprimer_joueur(joueur)

    def test_court(self):
        """Essaye de rapport quand le message est trop court."""
        joueur = self.creer_joueur("simple", "Kredh")
        nb_rapports = len(importeur.rapport.rapports)
        msg = self.entrer_commande(joueur,
                "bug liste")
        self.assertEqual(msg,
                "|err|Cette description de bug est trop courte.|ff|")
        self.assertEqual(len(importeur.rapport.rapports), nb_rapports)
        self.supprimer_joueur(joueur)

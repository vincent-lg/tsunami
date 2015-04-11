# -*-coding:Utf-8 -*

# Copyright (c) 2015 LE GOFF Vincent
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


"""Fichier définissant les unittest des extensions crafting."""

import unittest

class TestExtensions(unittest.TestCase):

    """Unittest des extensions d'éditeurs du crafting."""

    def test_chaine(self):
        """Test le type chaîne."""
        guilde = importeur.crafting.creer_guilde("forgerons")
        extension = guilde.ajouter_extension("salle", "minerais")
        extension.type = "chaine"
        self.assertEqual(extension.type, "chaîne")
        extension.type = "chaîne"
        self.assertEqual(extension.type, "chaîne")
        importeur.crafting.supprimer_guilde("forgerons")

    def test_entier(self):
        """Test le type entier."""
        guilde = importeur.crafting.creer_guilde("forgerons")
        extension = guilde.ajouter_extension("salle", "minerais")
        extension.type = "entier"
        self.assertEqual(extension.type, "entier")
        self.assertEqual(extension.sup, {
                "signe": None, "min": None, "max": None})
        extension.type = "entier négatif"
        self.assertEqual(extension.type, "entier")
        self.assertEqual(extension.sup, {
                "signe": "negatif", "min": None, "max": None})
        extension.type = "entier positif ou nul"
        self.assertEqual(extension.type, "entier")
        self.assertEqual(extension.sup, {
                "signe": "positif ou nul", "min": None, "max": None})
        extension.type = "entier négatif ou nul"
        self.assertEqual(extension.type, "entier")
        self.assertEqual(extension.sup, {
                "signe": "negatif ou nul", "min": None, "max": None})
        extension.type = "entier positif entre 40 et 200"
        self.assertEqual(extension.type, "entier")
        self.assertEqual(extension.sup, {
                "signe": "positif", "min": "40", "max": "200"})
        importeur.crafting.supprimer_guilde("forgerons")

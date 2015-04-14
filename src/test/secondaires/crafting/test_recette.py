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


"""Fichier définissant les unittest de recettes de guilde."""

import unittest

class TestRecette(unittest.TestCase):

    """Unittest des recettes de guilde."""

    def test_ajout(self):
        """Ajout d'une recette."""
        guilde = importeur.crafting.creer_guilde("forgerons")
        rang = guilde.ajouter_rang("apprenti")
        recette = rang.ajouter_recette("epee")
        self.assertEqual(recette.resultat, "epee")

        # Ajout et suppression de types
        recette.ajouter_type("chaussure")
        self.assertIn("chaussure", recette.ingredients_types)
        recette.retirer_type("chaussure")
        self.assertNotIn("chaussure", recette.ingredients_types)

        # Ajout et suppression d'objets
        recette.ajouter_objet("peau_lapin")
        self.assertIn("peau_lapin", recette.ingredients_objets)
        recette.retirer_objet("peau_lapin")
        self.assertNotIn("peau_lapin", recette.ingredients_objets)

        importeur.crafting.supprimer_guilde("forgerons")

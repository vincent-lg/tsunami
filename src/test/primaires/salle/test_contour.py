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


"""Fichier définissant les unittest des contours d'étendue."""

import unittest

CONTOUR_CARRE = [
    (10, 10),
    (11, 10),
    (12, 10),
    (13, 10),
    (14, 10),
    (14, 11),
    (14, 12),
    (14, 13),
    (14, 14),
    (13, 14),
    (12, 14),
    (11, 14),
    (10, 14),
    (10, 13),
    (10, 12),
    (10, 11),
]

CONTOUR_COMPLEXE = [
    (20, 20),
    (21, 20),
    (22, 20),
    (23, 20),
    (24, 20),
    (25, 20),
    (25, 21),
    (25, 22),
    (25, 23),
    (25, 24),
    (24, 24),
    (23, 24),
    (23, 25),
    (23, 26),
    (24, 26),
    (24, 27),
    (24, 28),
    (23, 28),
    (22, 28),
    (21, 28),
    (20, 28),
    (19, 28),
    (18, 28),
    (17, 28),
    (17, 27),
    (17, 26),
    (18, 26),
    (19, 26),
    (19, 25),
    (20, 25),
    (20, 24),
    (20, 23),
    (20, 22),
    (20, 21),
]

class TestContour(unittest.TestCase):

    """Unittest des contours.

    Le but et de détecter les contours d'étendues, c'est-à-dire les
    points qui entourent cette étendue mais pas ceux qui se trouvent
    à l'intérieur.

    """

    def test_carre(self):
        """Essaye d'obtenir le contour du carré."""
        carre = importeur.salle.etendues["carre"]
        contour = carre.contour
        self.assertEqual(contour, CONTOUR_CARRE)

    def test_complexe(self):
        """Essaye d'obtenir le contour de l'étendue complexe.

        Cette étendue est un peu plus grande que le carré et sa forme
        est très anarchique. Elle comporte également une branche à
        un moment, qui permet de vérifier si l'algorithme cherchant
        bien le contour est fonctionnel.

        """
        complexe = importeur.salle.etendues["complexe"]
        contour = complexe.contour
        self.assertEqual(contour, CONTOUR_COMPLEXE)

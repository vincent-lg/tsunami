# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 DAVY Guillaume
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


"""Plateau solitaire."""

from .. import BasePlateau
from .bille import Bille
from .vide import CaseVide

class Plateau(BasePlateau):

    """Plateau de solitaire.

    Il est utilisé pour jouer au... solitaire.

    """

    jeux = ["solitaire"]
    nom = "solitaire"

    def init(self):
        """Initialisation du plateau."""
        self.cases = {
            "C1": Bille(),
            "D1": Bille(),
            "E1": Bille(),
            "B2": Bille(),
            "C2": Bille(),
            "D2": Bille(),
            "E2": Bille(),
            "F2": Bille(),
            "A3": Bille(),
            "B3": Bille(),
            "C3": Bille(),
            "D3": Bille(),
            "E3": Bille(),
            "F3": Bille(),
            "G3": Bille(),
            "A4": Bille(),
            "B4": Bille(),
            "C4": Bille(),
            "D4": CaseVide(),
            "E4": Bille(),
            "F4": Bille(),
            "G4": Bille(),
            "A5": Bille(),
            "B5": Bille(),
            "C5": Bille(),
            "D5": Bille(),
            "E5": Bille(),
            "F5": Bille(),
            "G5": Bille(),
            "B6": Bille(),
            "C6": Bille(),
            "D6": Bille(),
            "E6": Bille(),
            "F6": Bille(),
            "C7": Bille(),
            "D7": Bille(),
            "E7": Bille(),
        }

    def afficher(self, personnage, jeu, partie):
        """Affiche la partie en cours au personnage."""
        plateau = \
            "  A B C D E F G\n" \
            "1     {C1} {D1} {E1}  \n" \
            "2   {B2} {C2} {D2} {E2} {F2}  \n" \
            "3 {A3} {B3} {C3} {D3} {E3} {F3} {G3}\n" \
            "4 {A4} {B4} {C4} {D4} {E4} {F4} {G4}\n" \
            "5 {A5} {B5} {C5} {D5} {E5} {F5} {G5}\n" \
            "7   {B6} {C6} {D6} {E6} {F6}  \n" \
            "8     {C7} {D7} {E7}  "

        return plateau.format(**self.cases)

    def detruire(self):
        """Destruction du plateau."""
        BaseObj.detruire(self)
        for case in self.cases.values():
            if case:
                case.detruire()

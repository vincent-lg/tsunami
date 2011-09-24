# -*-coding:Utf-8 -*

# Copyright (c) 2010 DAVY Guillaume
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

from abstraits.obase import BaseObj
from .bille import Bille
from .vide import CaseVide

class Plateau(BaseObj):
    
    """Plateau solitaire.
    
    Il est utilisé pour jouer au solitaire.
    
    """
    
    jeux = ["solitaire"]
    nom = "solitaire"
    
    def __init__(self):
        """Initialisation du plateau."""
        BaseObj.__init__(self)
        self.nb_joueurs_max = 1
        self.cases = {
            "C1": Bille(),
            "D1": Bille(),
            "E1": Bille(),
            "F1": Bille(),
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
            "H3": Bille(),
            "A4": Bille(),
            "B4": Bille(),
            "C4": Bille(),
            "D4": Bille(),
            "E4": CaseVide(),
            "F4": Bille(),
            "G4": Bille(),
            "H4": Bille(),
            "A5": Bille(),
            "B5": Bille(),
            "C5": Bille(),
            "D5": Bille(),
            "E5": Bille(),
            "F5": Bille(),
            "G5": Bille(),
            "H5": Bille(),
            "A6": Bille(),
            "B6": Bille(),
            "C6": Bille(),
            "D6": Bille(),
            "E6": Bille(),
            "F6": Bille(),
            "G6": Bille(),
            "H6": Bille(),
            "C7": Bille(),
            "D7": Bille(),
            "E7": Bille(),
            "F7": Bille(),
            "C8": Bille(),
            "D8": Bille(),
            "E8": Bille(),
            "F8": Bille(),
        }
        self._construire()
    
    def __getnewargs__(self):
        return ()
    
    def afficher(self, personnage):
        """Affiche la partie en cours au personnage."""
        plateau = \
            "  ABCDEFGH\n" \
            "1   {C1}{D1}{E1}{F1}  \n" \
            "2   {C2}{D2}{E2}{F2}  \n" \
            "3 {A3}{B3}{C3}{D3}{E3}{F3}{G3}{H3}\n" \
            "4 {A4}{B4}{C4}{D4}{E4}{F4}{G4}{H4}\n" \
            "5 {A5}{B5}{C5}{D5}{E5}{F5}{G5}{H5}\n" \
            "6 {A6}{B6}{C6}{D6}{E6}{F6}{G6}{H6}\n" \
            "7   {C7}{D7}{E7}{F7}  \n" \
            "8   {C8}{D8}{E8}{F8}  "
        
        return plateau.format(**self.cases)

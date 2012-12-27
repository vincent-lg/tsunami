# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Plateau du poqueer."""

from .. import BasePlateau
from .piece import Piece

class Plateau(BasePlateau):
    
    """Plateau du poquiir.
    
    Il est utilisé pour jouer au poquiir
    Il définit les différentes pièces.
    
    """
    
    jeux = ["poquiir"]
    nom = "poquiir"
    
    def init(self):
        """Préparation des pièces."""
        self.pieces = []
        couleurs = ["noir{e}", "rouge", "vert{e}", "gris{e}"]
        noms_pieces = [
            ("chien", False),
            ("mandiant", False),
            ("voleur", False),
            ("page", False),
            ("troubadour", False),
            ("druide", False),
            ("sorcière", True),
            ("fantassin", False),
            ("cavalier", False),
            ("laquais", False),
            ("courtisane", True),
            ("roi", False),
            ("immortel", False),
        ]
        for couleur in couleurs:
            points = 1
            for nom, fem in noms_pieces:
                piece = Piece(nom, couleur, points, fem=fem)
                self.pieces.append(piece)
                points += 1
    
    def afficher(self, personnage, jeu, partie):
        """Affiche la partie en cours au personnage."""
        en_main = jeu.en_main.get(personnage)
        tableau = jeu.tableau
        if en_main:
            msg = "Dans votre main, vous avez {} et {}.".format(
                    en_main[0].nom_complet_indefini,
                    en_main[1].nom_complet_indefini)
        else:
            msg = "Vous n'avez encore rien dans votre main."
        
        if tableau:
            tableau = [piece.nom_complet_indefini for piece in tableau]
            aff_tableau = ", ".join(tableau[:-1]) + " et " + tableau[-1]
            msg += "\nSur le tableau se trouve {}.".format(aff_tableau)

        if partie.tour is personnage:
            msg += "\nC'est votre tour."
        
        return msg

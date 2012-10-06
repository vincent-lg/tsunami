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


"""Jeu de poquiir."""

from random import *

from .. import BaseJeu
from .combinaisons import combinaisons

class Jeu(BaseJeu):
    
    """Ce jeu définit le jeu de poquiir.
    
    Il est rattaché au plateau poquiir.
    
    """
    
    nom = "poquiir"
    def init(self):
        """Construction du jeu."""
        self.nb_joueurs_min = 2
        self.nb_joueurs_max = 6
        self.en_main = {}
        self.tableau = []
        self.non_distribuees = list(self.plateau.pieces)
        self.combinaisons = {}
        self.abandons = []
        self.petite_blinde = 0
    
    @property
    def grande_blinde(self):
        """Retourne le montant de la grande blinde."""
        return self.petite_blinde * 2
    
    def peut_commencer(self):
        """La partie peut-elle commencer ?"""
        if self.petite_blinde == 0:
            self.partie.envoyer("Le montant de la petite blinde n'a pas " \
                    "été fixé.")
        return True
    
    def peut_jouer(self, personnage):
        """Le personnage peut-il jouer ?"""
        if personnage in self.abandons:
            personnage << "Vous avez abandonné cette manche."
            return False
        
        return True
    
    def jouer(self, personnage, msg):
        """Joue au jeu.
        
        Les possibilités sont :
            m <montant> : pour miser davantage
            s : suivre (check) sans miser davantage
            ab : abandonner
        
        """
        possibilites = \
            "Les possibilités sont :\n\n" \
            " |cmd|m <montant>|ff| pour miser davantage (exemple " \
            "|cmd|m 200|ff|\n)" \
            " |cmd|s|ff| pour suivre sans miser davantage\n" \
            " |cmd|ab|ff| pour abandonner la manche\n\n" \
            "|att|Les montants sont toujours donnés en pièces de bronze.|ff|"
        
        if msg:
            opt = msg.split(" ")[0].lower()
            reste = msg[len(msg):]
            if opt == "m":
                try:
                    montant = int(reste)
                except ValueError:
                    personnage << "|err|Montant {} invalide|ff|.".format(
                            reste)
                    return False
                else:
                    return self.monter(personnage, reste)
            elif opt == "s":
                return self.suivre(personnage)
            elif opt == "ab":
                self.abandonner(personnage)
                return True
            else:
                personnage << possibilites
                return False

        return False
    
    def get_combinaison(self, personnage):
        """Retourne la combinaison ou None si aucune."""
        pieces = self.en_main.get(personnage)
        if pieces is None:
            return None
        
        pieces.extend(self.tableau)
        
        # On tri les pièces
        d_pieces = {}
        for piece in pieces:
            points = piece.points
            liste = d_pieces.get(points, [])
            liste.append(piece)
            d_pieces[points] = liste
        
        pieces = sorted([liste for liste in d_pieces.values()],
                key=lambda liste: liste[0].points, reverse=True)
        
        essai = None
        for combinaison in combinaisons:
            essai = combinaison.forme(pieces)
            if essai:
                break
        
        return essai
    
    def choisir_piece(self):
        """Choisit et retourne une pièce parmi les non distribuées.
        
        La pièce retournée est considérée comme distribuée, on ne sait pas
        si c'est sur le tableau ou à un personnage, mais on la retire des
        pièces distribuées et on recalcul les combinaisons de chacun.
        
        """
        piece = choice(self.non_distribuees)
        self.non_distribuees.remove(piece)
        for joueur, pieces in self.en_main.items():
            combinaison = self.get_combinaison(joueur)
            if combinaison:
                self.combinaisons[joueur] = combinaison
        
        return piece
    
    def tour_1(self):
        """Commence une manche.
        
        On distribue les pièces des joueurs.
        
        """
        for joueur in self.partie.joueurs:
            piece_1 = self.choisir_piece()
            piece_2 = self.choisir_piece()
            self.en_main[joueur] = [piece_1, piece_2]
            joueur << "Vous recevez {} et {}.".format(
                    piece_1.nom_complet_indefini, piece_2.nom_complet_indefini)
    
    def tour_2(self):
        """On pose le flop (les trois premières cases sur le tableau)."""
        p1 = self.choisir_piece()
        p2 = self.choisir_piece()
        p3 = self.choisir_piece()
        self.tableau = [p1, p2, p3]
        noms = [p.nom_complet_indefini for p in (p1, p2, p3)]
        noms = noms[0] + ", " + noms[1] + " et " + noms[2]
        self.partie.envoyer("Trois pièces sont retournées face " \
                "visible sur le tableau :\n- {}".format(noms))
    
    def tour_3(self):
        """On ne retourne qu'une pièce."""
        piece = self.choisir_piece()
        self.tableau.append(piece)
        self.envoyer("On retourne {} face visible sur le tableau.".format(
                piece.nom_complet_indefini))
    def tour_4(self):
        """On ne retourne qu'une pièce."""
        piece = self.choisir_piece()
        self.tableau.append(piece)
        self.envoyer("On retourne {} face visible sur le tableau.".format(
                piece.nom_complet_indefini))
    
    def tour_5(self):
        """On détermine le ou les vainqueurs de la manche."""
        # à compléter

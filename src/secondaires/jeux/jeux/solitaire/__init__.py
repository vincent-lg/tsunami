# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 DAVY Guillaume
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


"""Jeu de solitaire."""

from math import fabs

from .. import BaseJeu
from secondaires.jeux.plateaux.solitaire.vide import CaseVide

def abs(valeur):
    """Retourne la valeur entière absolue de valeur."""
    return int(fabs(valeur))

class Jeu(BaseJeu):
    
    """Ce jeu définit le solitaire.
    
    Il est rattaché au plateau solitaire.
    
    """
    
    nom = "solitaire"
    
    def init(self):
        """Construction du jeu."""
        pass
    
    @property
    def personnage(self):
        """Retourne le personnage jouant au jeu."""
        return self.partie.personnage
    
    def jouer(self, personnage, msg):
        """Joue au jeu.
        
        On doit entrer deux coordonnées séparées par un espace.
        
        La première est la coordonnée de la case possédant une boule.
        
        La seconde est la coordonnée n'en possédant pas.
        
        """
        plateau = self.plateau
        partie = self.partie
        try:
            coord_de, coord_a = msg.split(" ")
        except ValueError:
            personnage << "|err|Précisez deux coordonnées séparées " \
                    "par un espace (|cmd|A1 A3|err| par exemple).|ff|"
        else:
            coord_de = self.get_coord(coord_de)
            coord_a = self.get_coord(coord_a)
            if not coord_de or not coord_a:
                return
            
            coord_entre = self.coup_valide(coord_de, coord_a)
            if coord_entre:
                plateau.cases[coord_a] = plateau.cases[coord_de]
                plateau.cases[coord_de] = CaseVide()
                plateau.cases[coord_entre] = CaseVide()
                partie.afficher_tous()
            else:
                personnage << "|err|Ce coup est invalide.|ff|"
    
    def get_coord(self, coord):
        """Retourne la coordonnée."""
        coord = coord.upper()
        try:
            colonne, ligne = coord
        except ValueError:
            self.personnage << "|err|Syntaxe invalide pour une coordonnée : " \
                    "{}|ff|".format(coord)
            return
        
        if coord not in self.plateau.cases:
            self.personnage << "|err|La case {} n'existe pas.|ff|".format(
                    coord)
            return
        
        return coord
    
    def coup_valide(self, coord_de, coord_a):
        """Retourne True si le coup est valide.
        
        Au solitaire, un coup est valide si :
            coord_de et coord_a sont séparés par une case occupée
            coord_a est vide
            coord_de est occupée
        
        """
        c_de, c_a = coord_de[0], coord_a[0]
        l_de, l_a = int(coord_de[1]), int(coord_a[1])
        if c_de == c_a and l_de != l_a:
            if abs(l_de - l_a) != 2:
                return False
            entre = c_de + str(l_de - (l_de - l_a) // 2)
        elif l_de == l_a and c_de != c_a:
            if abs(ord(c_de) - ord(c_a)) != 2:
                return False
            entre = chr(ord(c_de) - (ord(c_de) - ord(c_a)) // 2) + str(l_de)
        else:
            return False
        if not self.plateau.cases[coord_de]: return False
        if not self.plateau.cases[entre]: return False
        if self.plateau.cases[coord_a]: return False
        return entre

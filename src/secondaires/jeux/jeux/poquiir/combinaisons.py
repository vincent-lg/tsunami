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


"""Fichier définissant les combinaisons possibles."""

from abstraits.obase import BaseObj
from corps.fonctions import lisser

class Combinaison(BaseObj):
    
    """Classe représentant une combinaison abstraite."""
    
    points = None
    nom = None
    
    def __init__(self, combinaison, exterieures):
        """Constructeur de la combinaison.
        
        Les cartes contenues dans la liste combinaison sont celles formant
        la combinaison. Les autres sont contenues dans exterieures.
        
        """
        BaseObj.__init__(self)
        self.combinaison = combinaison
        self.exterieures = exterieures
        self._construire()
    
    def __getnewargs__(self):
        return (None, None)
    
    @property
    def nom(self):
        """Retourne le nom de la combinaison."""
        return "rien"
    
    @property
    def points_complet(self):
        """Retourne les points de la combinaison spécifique."""
        return (self.points, self.combinaison[-1].points)
    
    @property
    def points_exterieurs(self):
        """Retourne la somme des points des cartes non utilisées."""
        return sum(piece.points for piece in self.exterieures)
    
    @classmethod
    def forme(cls, pieces):
        """Retourne une combinaison si les pièces forment une combinaison.
        
        Les pièces doivent être transmises sous la forme d'une liste de listes.
        Les pièces de même valeur doivent être regroupées dans une liste et
        les pièces de plus grande valeur doivent apparaître en premier.
        
        Exemple s'inspirant, au lieu de pièces, des cartes standards :
            On a : 7 de coeur, as de coeur, 3 de carreau, 3 de trèffle...
            On doit recevoir : [[as coeur], [7 coeur], [3 carreau, 3 trèffle]]
        
        """
        return None

class Paire(Combinaison):
    
    """Combinaison représentant la paire."""
    
    points = 1
    
    @property
    def nom(self):
        nom_piece = self.combinaison[0].nom
        return "une paire de {}s".format(nom_piece)
    
    @classmethod
    def forme(cls, pieces):
        for groupe in pieces:
            if len(groupe) == 2:
                autres = list(pieces)
                autres.remove(groupe)
                exterieures = []
                for o_groupe in autres:
                    exterieures.extend(o_groupe)
                
                paire = cls(groupe, exterieures)
                return paire
        
        return None

class DoublePaire(Combinaison):
    
    """Combinaison représentant la double paire."""
    
    points = 2
    
    @property
    def nom(self):
        nom_1 = self.combinaison[0].nom
        nom_2 = self.combinaison[2].nom
        return "une double-paire de {}s et {}s".format(nom_1, nom_2)
    
    @classmethod
    def forme(cls, pieces):
        groupes = []
        for groupe in pieces:
            if len(groupe) == 2:
                groupes.append(groupe)
                if len(groupes) != 2:
                    continue
                
                autres = list(pieces)
                for o_groupe in groupes:
                    autres.remove(o_groupe)
                
                exterieures = []
                for o_groupe in autres:
                    exterieures.extend(o_groupe)
                
                dpaire = cls(groupes[0] + groupes[1], exterieures)
                return dpaire
        
        return None

class Brelan(Combinaison):
    
    """Combinaison représentant le brelan."""
    
    points = 3
    
    @property
    def nom(self):
        nom_piece = self.combinaison[0].nom
        return "un brelan de {}s".format(nom_piece)
    
    @classmethod
    def forme(cls, pieces):
        for groupe in pieces:
            if len(groupe) == 3:
                autres = list(pieces)
                autres.remove(groupe)
                exterieures = []
                for o_groupe in autres:
                    exterieures.extend(o_groupe)
                
                brelan = cls(groupe, exterieures)
                return brelan
        
        return None

class Suite(Combinaison):
    
    """Combinaison représentant la suite."""
    
    points = 4
    
    @property
    def nom(self):
        nom_piece = self.combinaison[0].nom_complet_defini
        return lisser("une suite à {}".format(nom_piece))
    
    @classmethod
    def forme(cls, pieces):
        a_pieces = []
        for groupe in pieces:
            a_pieces.extend(groupe)
        
        a_pieces = sorted(a_pieces, key=lambda piece: piece.points,
                reverse=True)
        for i, piece in enumerate(a_pieces):
            t_pieces = [piece]
            nb = 1
            for a_piece in a_pieces[i + 1:]:
                if piece.points - a_piece.points == nb:
                    t_pieces.append(a_piece)
                    nb += 1
                    if len(t_pieces) == 5:
                        exterieures = list(a_pieces)
                        for t_piece in t_pieces:
                            if t_piece in exterieures:
                                exterieures.remove(t_piece)
                        
                        suite = cls(t_pieces, exterieures)
                        return suite
        
        return None

class Couleur(Combinaison):
    
    """Combinaison représentant la couleur."""
    
    points = 5
    
    @property
    def nom(self):
        nom_piece = self.combinaison[0].nom_complet_defini
        return lisser("une couleur à {}".format(nom_piece))
    
    @classmethod
    def forme(cls, pieces):
        a_pieces = []
        for groupe in pieces:
            a_pieces.extend(groupe)
        
        a_pieces = sorted(a_pieces, key=lambda piece: piece.points,
                reverse=True)
        couleurs = {}
        for piece in a_pieces:
            liste = couleurs.get(piece._couleur, [])
            liste.append(piece)
            couleurs[piece._couleur] = liste
        
        for groupe in couleurs.values():
            if len(groupe) >= 5:
                exterieures = list(a_pieces)
                for piece in groupe:
                    if piece in exterieures:
                        exterieures.remove(piece)
                
                couleur = cls(groupe, exterieures)
                return couleur
        
        return None

class Carre(Combinaison):
    
    """Combinaison représentant le carré."""
    
    points = 6
    
    @property
    def nom(self):
        nom_piece = self.combinaison[0].nom
        return "un carré de {}s".format(nom_piece)
    
    @classmethod
    def forme(cls, pieces):
        print("carré", pieces)
        for groupe in pieces:
            if len(groupe) == 4:
                autres = list(pieces)
                autres.remove(groupe)
                exterieures = []
                for o_groupe in autres:
                    exterieures.extend(o_groupe)
                
                carre = cls(groupe, exterieures)
                return carre
        
        return None

combinaisons = [Carre, Couleur, Suite, Brelan, DoublePaire, Paire]
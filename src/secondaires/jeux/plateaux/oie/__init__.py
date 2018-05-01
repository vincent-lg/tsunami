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


"""Plateau du jeu de l'oie."""

from .. import BasePlateau
from .case import *
from .pion import Pion

class Plateau(BasePlateau):
    
    """Plateau du jeu de l'oie.
    
    Il est utilisé pour jouer au jeu de l'oie.
    Il définit les cases du jeu, les messages des différentes cases et
    les différents pièges.
    
    """
    
    jeux = ["jeu de l'oie"]
    nom = "jeu de l'oie"
    def init(self):
        """Initialisation du plateau."""
        Case.numero = 1
        self.cases = [
            Case("la futaie", "f", "|vr|", "dans"),
            Case("la cascade", "_", "|bl|", "sous"),
            Case("la prairie", "p", "|vr|", "dans"),
            Case("la ferme", "m", "|mr|", "dans"),
            CaseOie(),
            CasePont(),
            Case("l'étable", "e", "|rgc|", "dans"),
            Case("le moulin", "m", "|jn|", "dans"),
            CaseOie(),
            Case("le port", "p", "|bl|"),
            Case("les ruines", "-", "|mg|"),
            Case("le désert", "d", "|jn|"),
            Case("le phare", "h", "|mr|"),
            CaseOie(),
            Case("l'ossuaire", "u", "|gr|"),
            Case("la colline", "l", "|mr|"),
            Case("la crique", "c", "|bl|"),
            CaseOie(),
            CaseHotellerie(),
            Case("l'arène", "a", "|jn|", "dans"),
            Case("le champ de maïs", "p", "|vr|", "dans"),
            Case("l'écurie", "r", "|gr|", "dans"),
            CaseOie(),
            Case("le marais", "s", "|mr|", "dans"),
            Case("le champ de bataille", "b", "|nr|"),
            Case("la forêt", "f", "|vrc|", "dans"),
            CaseOie(),
            Case("le tumulus", "t", "|mr|"),
            Case("la banquise", "q", "|bc|"),
            Case("la bergerie", "b", "|mr|", "dans"),
            CasePuits(),
            CaseOie(),
            Case("l'orangeraie", "o", "|jn|"),
            Case("la jetée", "j", "|bl|"),
            Case("la tour de guet", "t", "|gr|"),
            CaseOie(),
            Case("le rempart", "r", "|gr|"),
            Case("la plage", "g", "|jn|"),
            Case("la pinède", "p", "|mr|"),
            Case("la basse-cour", "a", "|rgc|"),
            CaseOie(),
            CaseLabyrinthe(),
            Case("le bûcher", "u", "|jn|"),
            Case("la grotte", "g", "|mr|", "dans"),
            CaseOie(),
            Case("le camp", "p", "|gr|", "dans"),
            Case("la plaine enneigée", "n", "|bc|"),
            Case("le temple", "t", "|vr|", "dans"),
            Case("le voilier", "v", "|bc|"),
            CaseOie(),
            Case("l'oasis", "s", "|jn|", "dans"),
            CasePrison(),            
            Case("la roseraie", "r", "|mr|", "dans"),
            CaseOie(),
            Case("le rocher", "h", "|gr|"),
            Case("le pigeonnier", "g", "|jn|"),
            Case("la citadelle", "l", "|gr|"),
            CaseMort(),
            CaseOie(),
            Case("la roue", "r", "|bl|"),
            Case("la montagne", "m", "|vr|"),
            Case("le fleuve", "v", "|bl|"),
            CaseJardin(),
        ]
        self.pions = {
            "1": Pion("jaune", 1),
            "2": Pion("rouge", 2),
            "3": Pion("bleu", 3),
            "4": Pion("vert", 4),
            "5": Pion("orange", 5),
            "6": Pion("violet", 6),
        }
        self.ordre = \
            "            |{00}|\n" \
            "  /---------| |\n" \
            "  |{06} {05} {04} {03} {02} {01}|\n" \
            "  | |---------|---\\\n" \
            "  |{07}|{32} {31} {30} {29} {28} {27} {26}|\n" \
            "  | | |---------| |\n" \
            "  |{08}|{33}|{50} {49} {48} {47} {46}|{25}|\n" \
            "  | | | |-----| | |\n" \
            "  |{09}|{34}|{51}|{60} {59} {58}|{45}|{24}|\n" \
            "  | | | | |-| | | |\n" \
            "  |{10}|{35}|{52}|{61} {62}|{57}|{44}|{23}|\n" \
            "  | | | |---| | | |\n" \
            "  |{11}|{36}|{53} {54} {55} {56}|{43}|{22}|\n" \
            "  | | |-------| | |\n" \
            "  |{12}|{37} {38} {39} {40} {41} {42}|{21}|\n" \
            "  | |-----------| |\n" \
            "  |{13} {14} {15} {16} {17} {18} {19} {20}|\n" \
            "  \\---------------/"
    
    def afficher(self, personnage, jeu, partie):
        """Affiche la partie en cours au personnage."""
        cases = list(self.cases)
        for joueur, pos in jeu.joueurs.items():
            case = cases[pos]
            pion = jeu.pions.get(joueur)
            if pion:
                cases[pos] = str(pion.numero)
        
        return self.ordre.format(*cases)

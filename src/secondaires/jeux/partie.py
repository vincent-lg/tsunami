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


"""Fichier contenant la classe Partie, détaillée plus bas."""

from abstraits.id import ObjetID
from bases.collections.liste_id import ListeID

class Partie(ObjetID):
    
    """Classe représentant une partie.
    
    Une partie est un état figé d'un jeu.
    
    """
    
    groupe = "partie"
    sous_rep = "jeux/parties"
    def __init__(self, jeu, plateau):
        """Constructeur de la partie."""
        ObjetID.__init__(self)
        self.jeu = jeu
        self.plateau = plateau
        self.__joueurs = ListeID(self)
    
    def __getnewargs__(self):
        return (None, None)
    
    @property
    def personnage(self):
        """Retourne le premier joueur."""
        return self.__joueurs[0]
    
    def ajouter_joueur(self, personnage):
        """Ajoute le personnage comme joueur."""
        if self.plateau.nb_joueurs_max > len(self.__joueurs):
            self.__joueurs.append(personnage)
            return True
        
        return False
    
    def afficher(self, personnage):
        return self.plateau.afficher(personnage)
    
    def afficher_tous(self):
        """Affiche la partie à tous les participants."""
        for p in self.__joueurs:
            p << self.afficher(p)

ObjetID.ajouter_groupe(Partie)

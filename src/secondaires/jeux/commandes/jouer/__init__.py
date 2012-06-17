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


"""Package contenant la commande 'jouer'."""

from primaires.interpreteur.commande.commande import Commande

from secondaires.jeux.contextes.plateau import Plateau as ContextePlateau
from secondaires.jeux.partie import Partie

class CmdJouer(Commande):
    
    """Commande 'jouer'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "jouer", "play")
        self.schema = "<nom_objet>"
        self.aide_courte = "permet de jouer à un jeu"
        self.aide_longue = \
            "Cette commande lance une partie sur un plateau de jeu. Bien " \
            "entendu, si quelqu'un est déjà en train de jouer, vous ne " \
            "pouvez commencer votre propre partie à moins qu'il ne vous " \
            "cède la place."
    
    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        nom_objet = self.noeud.get_masque("nom_objet")
        nom_objet.proprietes["type"] = "'plateau de jeu'"
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        objet = dic_masques["nom_objet"].objet
        personnage.agir("jouer")
        jeux = type(self).importeur.jeux.jeux
        plateaux = type(self).importeur.jeux.plateaux
        plateau = plateaux[objet.plateau]
        jeu = plateau.jeux[0]
        jeu = jeux[jeu]
        
        partie = objet.partie
        if partie is None:
            plateau = plateau()
            jeu = jeu()
            partie = Partie(objet, jeu, plateau)
            jeu.plateau = plateau
            jeu.partie = partie
            objet.partie = partie
        elif partie.en_cours:
            personnage << "|err|La partie est déjà commencée.|ff|"
            return
        elif len(partie.joueurs) >= partie.jeu.nb_joueurs_max:
            personnage << "|err|Il n'y a plus de place libre.|ff|"
            return
        
        personnage.cle_etat = "jeu"
        partie.ajouter_joueur(personnage)
        contexte = ContextePlateau(personnage.instance_connexion, objet,
                partie)
        personnage.contextes.ajouter(contexte)
        personnage << contexte.accueil()

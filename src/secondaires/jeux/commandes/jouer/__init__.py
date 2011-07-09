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

from secondaires.jeux.contextes.plateau import Plateau

class CmdJouer(Commande):
    
    """Commande 'jouer'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "jouer", "play")
        self.schema = "<objet_jeu>"
        self.nom_categorie = "bouger"
        self.aide_courte = "Permet de jouer à un jeu"
        self.aide_longue = \
            "Cette commande permet de jouer à un jeu "
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        objet = dic_masques["objet_jeu"].element
        
        jeux = type(self).importeur.jeux
        
        if jeux.get_jeu(objet.jeu) is None:
            raise(ValueError("Le jeu n'existe pas"))
        else:
            partie = jeux.get_partie(objet)
            contexte = Plateau(personnage.instance_connexion, objet)
            personnage.contexte_actuel.migrer_contexte(contexte)
            partie.arriverPif(personnage)
        

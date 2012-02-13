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


"""Ce package contient les backens de jeu.

Ce fichier contient la classe BaseJeu dont doit être hérité chaque jeu.
Cette classe est détaillée plus bas.

"""

from abstraits.obase import BaseObj

class BaseJeu(BaseObj):
    
    """Classe définissant un jeu.
    
    Ce jeu est indépendant du plateau. En effet, un plateau peut être
    utilisé pour différents jeux, par exemple on trouve beaucoup de jeux
    différents utilisant 52 cartes.
    
    Le jeu tel que défini dans cette classe est l'ensemble des règles
    du jeu indépendemment du plateau. Le plateau lui va contenir les
    cases, les différents pions et d'autres détails. Les informations
    ponctuelles sur le jeu (la position des joueurs, les tours de chacun)
    va être défini dans la partie.
    
    """
    
    nom = "" # nom du jeu
    def __init__(self):
        """Constructeur d'un jeu.
        
        Il ne doit pas être redéfini. Pour ajouter des attributs,
        redéfinir plutôt la méthode init qui est appelée par le constructeur.
        
        """
        BaseObj.__init__(self)
        self.partie = None
        self.plateau = None
        self.nb_joueurs_min = 1
        self.nb_joueurs_max = 1
        self.init()
        self._construire()
    
    def __getnewargs__(self):
        return ()
    
    def peut_commencer(self):
        """La partie peut-elle commencée ?"""
        return True
    
    def peut_jouer(self, personnage):
        """Le joueur peut-il jouer ?
        
        Cette méthode retourne True si le joueur peut jouer ou False sinon.
        En outre, si une explication doit être donnée sur le fait que
        ce joueur ne eput pas jouer, ce doit être ici.
        
        """
        return True
    
    def jouer(self, personnage, msg):
        """Joue au jeu.
        
        La variable msg contient le message entré par le joueur voulant jouer.
        
        Pour rappel, le contexte de jeu interprète les messages commençant
        par un slash (/) comme des options. Tous les autres sont des
        ordres adressés au jeu pour jouer et sont transmis à cette méthode.
        Chaque jeu peut avoir une différente syntaxe pour jouer
        (par exemple, le solitaire demandra qu'on entre deux coordonnées
        séparés par un espace, ce sera aussi le cas des échecs, mais ce
        ne sera pas le cas d'un jeu de carte où il faudra choisir le numéro
        de la carte que l'on souhaite jouer par exemple). Cela est à
        l'initiative de cette méthode de comprendre le message et de
        l'interpréter.
        
        Chaque jeu doit donc redéfinir cette méthode.
        
        """
        self.partie.en_cours = True
    
    # Options
    # Le nom des méthodes est opt_ suivi du raccourci. Ainsi, pour
    # quitter le jeu, il faut entrer /q ce qui redirigera vers
    # la méthode opt_q
    def opt_q(self, personnage, message):
        """Quitte le jeu."""
        personnage.contextes.retirer()
        personnage << "Vous quittez la partie."
        self.partie.retirer_joueur(personnage)
        if len(self.partie.joueurs) == 0:
            self.partie.detruire()
    
    def opt_v(self, personnage, message):
        """Affiche le plateau."""
        personnage << self.partie.afficher(personnage)

# -*-coding:Utf-8 -*

# Copyright (c) 2010 LE GOFF Vincent
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


"""Fichier contenant le module primaire joueur."""

from abstraits.module import *
from primaires.joueur.contextes import liste_contextes
from primaires.joueur import commandes
from primaires.joueur import masques
from primaires.joueur.config import cfg_joueur

class Module(BaseModule):
    """Classe utilisée pour gérer des joueurs, c'est-à-dire des personnages
    connecté par client, à distinguer des NPCs.
    
    Les mécanismes de jeu propres aux personnages, c'est-à-dire communs aux
    joueurs et NPCs, ne sont pas défini dans ce module mais dans le module
    primaire 'perso'.
    
    """
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "joueur", "primaire")
        self.commandes = []
    
    def config(self):
        """Méthode de configuration du module"""
        type(self.importeur).anaconf.get_config("joueur", \
            "joueur/joueur.cfg", "config joueur", cfg_joueur)
        
        BaseModule.config(self)
    
    def init(self):
        """Méthode d'initialisation du module"""
        # On ajoute les contextes chargés dans l'interpréteur
        for contexte in liste_contextes:
            self.importeur.interpreteur.contextes[contexte.nom] = contexte
        
        # Ajout des masques dans l'interpréteur
        self.importeur.interpreteur.ajouter_masque(masques.commande.Commande())
        
        # On ajoute les commandes du module
        self.commandes = [
            commandes.commande.CmdCommande(),
            commandes.module.CmdModule(),
            commandes.shutdown.CmdShutdown(),
            commandes.quitter.CmdQuitter(),
            commandes.qui.CmdQui(),
        ]
        
        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)
        
        BaseModule.init(self)

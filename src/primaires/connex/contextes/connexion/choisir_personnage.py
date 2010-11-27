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
# pereIBILITY OF SUCH DAMAGE.

import re

from primaires.interpreteur.contexte import Contexte

# Constantes
cmd_creer = "c"
cmd_supprimer = "s"
cmd_quitter = "q"

class ChoisirPersonnage(Contexte):
    """Contexte du choix de personnage
    
    """
    nom = "connex:connexion:choix_personnages"
    
    def __init__(self, pere):
        """Constructeur du contexte"""
        Contexte.__init__(self, pere)
    
    def get_prompt(self):
        """Message de prompt"""
        return "Votre choix : "
    
    def accueil(self):
        """Message d'accueil"""
        ret = \
            "\n|tit|------= Choix du personnage =-----|ff|\n" \
            "Entrez un des |ent|nombres|ff| ou |ent|lettres|ff| ci-dessous :\n"
        
        # On va calculer la marge gauche
        m_g = 1
        
        for i, joueur in enumerate(self.pere.compte.joueurs.values()):
            no = "|cmd|" + str(i + 1) + "|ff|"
            ret += "\n"
            ret += str(no).rjust(len(no) + m_g)
            ret += " pour se connecter avec le joueur |ent|{0}|ff|".format( \
                    joueur.nom)
        
        if len(self.pere.compte.joueurs) > 0:
            # on saute deux lignes
            ret += "\n\n"
        
        ret += "|cmd|{C}|ff| pour |ent|créer|ff| un nouveau " \
                "personnage\n".format(C = cmd_creer.upper())
        if len(self.pere.compte.joueurs) > 0:
            # on propose de supprimer un des joueurs créé
            ret += "|cmd|{S}|ff| pour |ent|supprimer|ff| un personnage de ce " \
                    "compte\n".format(S = cmd_supprimer.upper())
        
        ret += "|cmd|{Q}|ff| pour |ent|quitter|ff| le jeu".format( \
                Q = cmd_quitter.upper())
        return ret
    
    def interpreter(self, msg):
        """Méthode d'interprétation"""
        msg = msg.lower()
        if msg.isdecimal():
            # On le convertit
            choix = int(msg) - 1
            # On vérifie qu'il est bien dans la liste des comptes
            if choix < 0 or choix >= len(self.pere.compte.joueurs):
                self.pere.envoyer("|err|Aucun numéro ne correspond à ce " \
                        "joueur.|ff|")
            else:
                # on se connecte sur le joueur
                pass
        elif msg == cmd_creer:
            # on redirige vers la création de compte
            self.migrer_contexte("personnage:creation:nouveau_nom")
        elif msg == cmd_supprimer:
            # On redirige vers la suppression de comptes
            pass
        elif msg == cmd_quitter:
            # On déconnecte le joueur
            self.pere.envoyer("|rg|A bientôt !|ff|")
            self.pere.deconnecter("Déconnexion demandée par le client")
        else:
            self.pere.envoyer("|att|Commande invalide.|ff|")

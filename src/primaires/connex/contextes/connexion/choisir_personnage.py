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
    
    def entrer(self):
        """Si aucun personnage n'a été créé, on redirige vers la création d'un
        premier personnage.
        
        """
        if len(self.pere.compte.joueurs) == 0:
            self.migrer_contexte("personnage:creation:nouveau_nom")
    
    def get_prompt(self):
        """Message de prompt"""
        return "Votre choix : "
    
    def accueil(self):
        """Message d'accueil"""
        ret = \
            "\n|tit|------= Choix du personnage =------|ff|\n" \
            "Faites votre |ent|choix|ff| parmi la liste ci-dessous :\n"
        
        for i, joueur in enumerate(self.pere.compte.joueurs.values()):
            no = " |cmd|" + str(i + 1) + "|ff|"
            ret += "\n" + no + " pour jouer |ent|{0}|ff|".format( \
                joueur.nom.capitalize())
        
        if len(self.pere.compte.joueurs) > 0:
            # on saute deux lignes
            ret += "\n\n"
        
        ret += " |cmd|{C}|ff| pour |ent|créer|ff| un nouveau " \
                "personnage\n".format(C = cmd_creer.upper())
        if len(self.pere.compte.joueurs) > 0:
            # on propose de supprimer un des joueurs créé
            ret += " |cmd|{S}|ff| pour |ent|supprimer|ff| un personnage de " \
                "ce compte\n".format(S = cmd_supprimer.upper())
        
        ret += " |cmd|{Q}|ff| pour |ent|quitter|ff| le jeu".format( \
                Q = cmd_quitter.upper())
        return ret
    
    def interpreter(self, msg):
        """Méthode d'interprétation"""
        cfg_connex = type(self).importeur.anaconf.get_config("connex")
        nb_perso_max = cfg_connex.nb_perso_max
        
        msg = msg.lower()
        if msg.isdecimal():
            # On le convertit
            choix = int(msg) - 1
            # On vérifie qu'il est bien dans la liste des comptes
            if choix < 0 or choix >= len(self.pere.compte.joueurs):
                self.pere.envoyer("|err|Aucun personnage ne correspond à ce " \
                        "numéro.|ff|")
            else:
                # on se connecte sur le joueur
                IDs_joueurs = list(self.pere.compte.joueurs.keys())
                joueur = self.pere.compte.joueurs[IDs_joueurs[choix]]
                self.pere.joueur = joueur
                joueur.compte = self.pere.compte
                joueur.instance_connexion = self.pere
                self.migrer_contexte("personnage:connexion:mode_connecte")
        elif msg == cmd_creer:
            if len(self.pere.compte.joueurs) >= nb_perso_max and nb_perso_max != -1:
                self.pere.envoyer("|err|Vous ne pouvez avoir plus de {0} " \
                        "personnages.|ff|".format(nb_perso_max))
            else:
                # On redirige vers la création de compte
                self.migrer_contexte("personnage:creation:nouveau_nom")
        elif msg == cmd_supprimer:
            # On redirige vers la suppression de comptes
            pass
        elif msg == cmd_quitter:
            # On déconnecte le joueur
            self.pere.envoyer("\nA bientôt !")
            self.pere.deconnecter("Déconnexion demandée par le client")
        else:
            self.pere.envoyer("|err|Votre choix est invalide.|ff|")

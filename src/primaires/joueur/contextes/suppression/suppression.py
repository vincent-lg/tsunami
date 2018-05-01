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
# pereIBILITY OF SUCH DAMAGE.


"""Fichier contenant le contexte "personnage:suppression:suppression"""

from primaires.interpreteur.contexte import Contexte
from primaires.joueur.joueur import Joueur

class Suppression(Contexte):
    """Contexte permettant la suppression d'un personnage. Le client
    doit sélectionner l'un de ses personnages. Une confirmation lui
    est demandée (utilisation de la variable self.confirmation), 
    puis le personnage ciblé est supprimé.
    
    Dans tous les cas, après suppression ou annulation de la part du
    client, on revient au contexte de choix d'un personnage.
    
    """
    nom = "personnage:suppression:suppression"
    
    def __init__(self, pere):
        """Constructeur du contexte"""
        Contexte.__init__(self, pere)
        self.opts.rci_ctx_prec = "connex:connexion:choix_personnages"
        self.confirmation = -1
    
    def accueil(self):
        """Message d'accueil du contexte"""
        ret = \
            "\n|tit|--= Suppression d'un personnage =--|ff|\n" \
            "Choisissez le |ent|personnage|ff| à supprimer parmi la liste " \
            "ci-dessous :\n"
            
        for i, joueur in enumerate(self.pere.compte.joueurs):
            no = " |cmd|" + str(i + 1) + "|ff|"
            ret += "\n" + no + " pour supprimer |ent|{0}|ff|".format( \
                joueur.nom.capitalize())
                
        return ret
    
    def get_prompt(self):
        """Message de prompt"""
        if self.confirmation < 0:
            return "Votre choix : "
        else:
            return "Nom du personnage : "
    
    def interpreter(self, msg):
        """méthode d'interprétation"""
        if self.confirmation < 0:
            if not msg.isdecimal():
                self.pere.envoyer("|err|Votre choix est invalide.|ff|")
            else:
                choix = int(msg) - 1
                if choix < 0 or choix >= len(self.pere.compte.joueurs):
                    self.pere.envoyer("|err|Aucun personnage ne " \
                            "correspond à ce numéro.|ff|")
                else:
                    #On enclenche la procédure de confirmation
                    self.confirmation = choix
                    self.pere.envoyer("Veuillez confirmer la suppression " \
                        "de ce personnage en entrant son |ent|nom|ff|.")
        else:
            msg = msg.lower()
            nom = self.pere.compte.joueurs[self.confirmation].nom.lower()
            if nom != msg:
                self.pere.envoyer("|err|Le nom entré est incorrect|ff|")
                self.migrer_contexte(self.nom)
            else:
                joueur = self.pere.compte.joueurs[self.confirmation]
                del self.pere.compte.joueurs[self.confirmation]
                joueur.detruire()
                self.pere.envoyer("|att|Personnage supprimé !|ff|")
                self.migrer_contexte(self.opts.rci_ctx_prec)

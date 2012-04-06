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
# pereIBILITY OF SUCH DAMAGE.

from primaires.interpreteur.contexte import Contexte

import re

## Constantes
# Regex
RE_PASS_VALIDE = re.compile(r"^[a-zA-Z0-9{}/\[\]()+=$_*@^\"'`£#-]+$", re.I)
# Taille mini du mot de passe
MIN = 6

class ChoisirPass(Contexte):
    """Contexte du choix de mot de passe.
    Le client doit choisir un mot de passe sécurisant l'accès au compte
    nouvellement créée.
    
    """
    
    def __init__(self, pere):
        """Constructeur du contexte"""
        Contexte.__init__(self, pere)
        self.opts.rci_ctx_prec = None
        self.suivant = None
    
    def get_prompt(self):
        """Message de prompt"""
        return "Votre mot de passe : "
    
    def entrer(self):
        """En arrivant dans le contexte"""
        self.pere.client.masquer = True
        self.pere.envoyer_options("masquer")
        
    def sortir(self):
        """En sortant du contexte"""
        self.pere.client.masquer = False
        self.pere.envoyer_options("afficher")
        
    def accueil(self):
        """Message d'accueil"""
        ret = \
            "\n|tit|------= Choix du mot de passe =-----|ff|\n" \
            "Entrez un |ent|mot de passe|ff| ; il correspond à votre " \
            "compte uniquement,\n" \
            "veillez à vous en souvenir et à ne le divulguer " \
            "sous aucun prétexte."
        if self.opts.rci_ctx_prec:
            ret += "\nSi vous voulez revenir au choix de l'encodage, " \
                    "entrez |cmd|/|ff|."
        return ret
    
    def interpreter(self, msg):
        """Méthode appelée quand un message est réceptionné"""
        cfg_connex = type(self).importeur.anaconf.get_config("connex")
        type_chiffrement = cfg_connex.type_chiffrement
        clef_salage = cfg_connex.clef_salage
        min = cfg_connex.pass_min
        
        if len(msg) < min:
            self.pere.envoyer("|err|Pour des raisons de sécurité, le mot de " \
                            "passe doit faire au minimum\n" \
                            "{0} caractères.|ff|".format(min))
        elif RE_PASS_VALIDE.search(msg) is None:
            self.pere.envoyer("|err|Le mot de passe entré contient des " \
                            "caractères non autorisés ; les caractères\n" \
                            "admis sont les lettres (majuscules et " \
                            "minuscules, sans accents), les\n" \
                            "chiffres et certains caractères spéciaux : " \
                            "|ff||cmd|{}/\[\]()+=$_*@^\"'`£#-|ff||err|.|ff|")
        else:
            # Hash du mot de passe
            self.pere.compte.mot_de_passe = \
                self.pere.compte.hash_mot_de_pass(clef_salage, \
                type_chiffrement, msg)
            self.migrer_contexte(self.suivant)

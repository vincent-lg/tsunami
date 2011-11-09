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

class ConfirmerPass(Contexte):
    """Contexte de confirmation de mot de passe.
    Le client doit entrer une nouvelle fois le mot de passe qu'il a choisi au
    contexte précédent.
    
    """
    
    def __init__(self, pere):
        """Constructeur du contexte"""
        Contexte.__init__(self, pere)
        self.opts.rci_ctx_prec = None
        self.suivant = None
    
    def get_prompt(self):
        """Message de prompt"""
        return "Confirmez le mot de passe : "
    
    def entrer(self):
        """En arrivant dans le contexte"""
        self.pere.client.masquer = True
        
    def sortir(self):
        """En sortant du contexte"""
        self.pere.client.masquer = False
        
    def accueil(self):
        """Message d'accueil"""
        return \
            "\n|tit|----------= Confirmation =----------|ff|\n" \
            "Entrez une nouvelle fois votre |ent|mot de passe|ff| pour " \
            "le confirmer."
    
    def interpreter(self, msg):
        """Méthode appelée quand un message est réceptionné"""
        cfg_connex = type(self).importeur.anaconf.get_config("connex")
        type_chiffrement = cfg_connex.type_chiffrement
        clef_salage = cfg_connex.clef_salage
        
        if self.pere.compte.mot_de_passe == \
            self.pere.compte.hash_mot_de_pass(clef_salage, \
                type_chiffrement, msg):
            if self.suivant is None:
                self.pere.joueur.contextes.retirer()
                self.pere.envoyer("|att|Votre mot de passe a bien été " \
                        "modifié.|ff|")
            else:
                self.migrer_contexte(self.suivant)
        else:
            self.pere.envoyer("|err|Le mot de passe de confirmation ne " \
                    "correspond pas à celui entré à l'étape\n" \
                    "précédente. Si cette erreur persiste, vous vous " \
                    "êtes peut-être trompé\n" \
                    "en indiquant votre mot de passe la première fois.\n" \
                    "Dans ce cas, entrez |ff||cmd|/|ff||err| pour " \
                    "retourner à l'étape précédente.|ff|")

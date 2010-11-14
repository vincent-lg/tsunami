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


from primaires.interpreteur.contexte import Contexte

import re

## Constantes
# Regex
RE_MAIL_VALIDE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b", re.I)

class EntrerEmail(Contexte):
    """Contexte du choix de l'adresse mail.
    On récupère l'adresse email et on envoit un mail avec le code de
    validation qui sera récupéré par le contexte suivant
    
    """
    def __init__(self):
        """Constructeur du contexte"""
        Contexte.__init__(self, "connex:creation:entrer_email")
    
    def get_prompt(self, emt):
        """Message de prompt"""
        return "Votre email : "
    
    def accueil(self, emt):
        """Message d'accueil"""
        return \
            "\n------= Entrez adresse email =------\n" \
            "Entrez votre |grf|adresse email|ff| pour votre nouveau compte.\n" \
            "Avant de pouvoir utiliser votre compte, un e-mail contenant\n" \
            "un code de validation vous sera envoyé à cette adresse.\n" \
            "Veillez donc à ce qu'elle soit valide."
    
    def deconnecter(self, emt):
        """En cas de déconexion du joueur, on supprime son compte"""
        type(self).importeur.connex.supprimer_compte(emt.emetteur)
    
    def interpreter(self, emt, msg):
        """Méthode appelée quand un message est réceptionné"""
        # On passe le message en minuscules
        msg = msg.lower()
        if msg in type(self).importeur.connex.email_comptes:
            self.envoyer(emt, "Cette adresse e-mail a déjà été utilisée.")
        elif RE_MAIL_VALIDE.search(msg) is None:
            self.envoyer(emt, "|rg|Ceci n'est pas une adresse mail valide.|ff|")
        else:
            emt.emetteur.adresse_email = msg
            config = type(self).importeur.anaconf.get_config("email")
            if config.serveur_mail:
                self.migrer_contexte(emt, "connex:creation:validation")
            else:
                emt.emetteur.valide = True
                self.migrer_contexte(emt, "connex:connexion:entrer_nom")
    

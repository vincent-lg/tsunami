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

class Validation(Contexte):
    
    def __init__(self):
        """Constructeur du contexte"""
        Contexte.__init__(self, "connex:creation:validation")
        self.opts.rci_ctx_prec = "connex:creation:entrer_email"
    
    def get_prompt(self, emt):
        """Message de prompt"""
        # Comme l'option ncod est activée, le préfixe est affiché en dur
        return "Code de validation : "
    
    def accueil(self, emt):
        """Message d'accueil"""
        return \
            "\n-----= Validation de l'email =------\n" \
            "Blabla validation"
    
    def deconnecter(self, emt):
        """En cas de déconexion du joueur, on supprime son compte"""
        type(self).importeur.connex.supprimer_compte(emt.emetteur)
    
    def interpreter(self, emt, msg):
        self.migrer_contexte(emt, "connex:connexion:entrer_nom")

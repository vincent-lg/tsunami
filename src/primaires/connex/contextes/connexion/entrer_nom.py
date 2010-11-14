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


import re

from primaires.interpreteur.contexte import Contexte
from primaires.connex.motd import MOTD

## Constantes
# Regex
RE_NOUVEAU = None # on ne connaît pas la chaîne

class EntrerNom(Contexte):
    """Contexte demandant au client d'entrer le nom de son compte.
    Ce contexte est censément le premier appelé à la connexion d'un client.
    Plusieurs sorties possibles :
    *   Le client entre une demande de nouveau compte (voir RE_NOUVEAU) :
        Dans ce cas, on redirige sur le contexte 'connex:creation:entrer_nom'
    *   Le client entre un nom de compte existant (c'est-à-dire
        créé, au moins partiellement)
    *   Sinon, on affiche une erreur (le compte n'existe pas)
    
    """
    def __init__(self):
        """Constructeur du contexte"""
        global RE_NOUVEAU
        Contexte.__init__(self, "connex:connexion:entrer_nom")
        self.opts.emt_ncod = False
        self.opts.sup_accents = True
        cnx_cfg = type(self).importeur.anaconf.get_config("connex")
        RE_NOUVEAU = re.compile("^{0}$".format(cnx_cfg.chaine_nouveau), re.I)
    
    def get_prompt(self, emt):
        """Message de prompt"""
        return "Votre compte : "
    
    def accueil(self, emt):
        """Message d'accueil"""
        cnx_cfg = type(self).importeur.anaconf.get_config("connex")
        return \
            "\nEntrez votre |grf|nom de compte|ff| ou |grf|{0}|ff| pour " \
            "en créer un.\n" \
            "|rg|Un seul compte par personne est autorisé.|ff|".format( \
            cnx_cfg.chaine_nouveau)
    
    def interpreter(self, emt, msg):
        """Méthode appelée quand un message est réceptionné"""
        if RE_NOUVEAU.search(msg): # le client demande un nouveau compte
            self.migrer_contexte(emt, "connex:creation:entrer_nom")
        elif type(self).importeur.connex.compte_est_cree(msg):
            print (type(self).importeur.connex.get_compte(msg))
            emt.emetteur = type(self).importeur.connex.get_compte(msg)
            self.migrer_contexte(emt, "connex:connexion:entrer_pass")
        else:
            self.envoyer(emt, "Ce compte n'existe pas. Entrez |grf|nouveau|ff| " \
                            "si vous souhaitez le créer.")

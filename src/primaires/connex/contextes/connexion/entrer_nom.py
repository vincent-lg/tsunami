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


import re

from primaires.interpreteur.contexte import Contexte
from primaires.connex.motd import MOTD

## Constantes
# Regex
RE_NOUVEAU = None # on ne connaît pas la chaîne

# Messages
FERMETURE_ERREUR = \
    "|rg|L'univers de Vancia est temporairement fermé aux joueurs.|ff|\n" \
    "Vous ne pouvez vous connecter à l'univers avec ce compte.\n" \
    "Si vous souhaitez malgré tout vous connectez, envoyez un e-mail à " \
    "l'adresse\n" \
    "|ent|vanciamud@gmail.com|ff| pour obtenir ce droit."

class EntrerNom(Contexte):
    """Contexte demandant au client d'entrer le nom de son compte.
    
    Ce contexte est censément le premier appelé à la connexion d'un client.
    Plusieurs sorties pereibles :
    *   Le client entre une demande de nouveau compte (voir RE_NOUVEAU) :
        Dans ce cas, on redirige sur le contexte 'connex:creation:entrer_nom'
        La création de compte doit être autorisée.
    *   Le client entre un nom de compte existant (c'est-à-dire
        créé, au moins partiellement)
    *   Sinon, on affiche une erreur (le compte n'existe pas)
    
    """
    nom = "connex:connexion:entrer_nom"
    
    def __init__(self, pere):
        """Constructeur du contexte"""
        global RE_NOUVEAU
        Contexte.__init__(self, pere)
        self.opts.sup_accents = True
        cfg_connex = type(self).importeur.anaconf.get_config("connex")
        RE_NOUVEAU = re.compile("^{0}$".format(cfg_connex.chaine_nouveau), re.I)
    
    def get_prompt(self):
        """Message de prompt"""
        return "Votre compte : "
    
    def accueil(self):
        """Message d'accueil"""
        cfg_connex = type(self).importeur.anaconf.get_config("connex")
        return \
            "\nEntrez votre |cmd|nom de compte|ff| ou |cmd|{0}|ff| pour " \
            "en créer un.\n" \
            "|att|Un seul compte par personne est autorisé.|ff|".format( \
            cfg_connex.chaine_nouveau)
    
    def interpreter(self, msg):
        """Méthode appelée quand un message est réceptionné"""
        cfg_connex = type(self).importeur.anaconf.get_config("connex")
        msg = msg.lower()
        if RE_NOUVEAU.search(msg): # le client demande un nouveau compte
            if cfg_connex.creation_autorisee or \
                    not cfg_connex.fermeture_filtree or \
                    self.pere.connexion_locale():
                self.migrer_contexte("connex:creation:entrer_nom")
            else:
                self.pere << "|err|La création de compte sur ce MUD " \
                        "est interdite.|ff|"
        elif type(self).importeur.connex.compte_est_cree(msg):
            compte = importeur.connex.get_compte(msg)
            if compte.nom != cfg_connex.compte_admin and \
                    cfg_connex.fermeture_filtree and not compte.autorise:
                self.pere.envoyer(FERMETURE_ERREUR)
            else:
                self.pere.compte = compte
                self.migrer_contexte("connex:connexion:entrer_pass")
        else:
            self.pere.envoyer("|err|Ce compte n'existe pas.|ff|\n" \
                    "Entrez |grf|{0}|ff| si vous souhaitez le créer.".format( \
                    cfg_connex.chaine_nouveau))

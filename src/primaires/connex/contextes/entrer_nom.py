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
RE_NOUVEAU = re.compile(r"^nouveau$", re.I)
RE_NOM_VALIDE = re.compile(r"^[A-Za-z0-9]{3,15}$", re.I)

class EntrerNom(Contexte):
    """Contexte demandant au client d'entrer le nom de son compte.
    Plusieurs sorties possibles :
    *   Le client entre une demande de nouveau compte (voir RE_NOUVEAU) :
        Dans ce cas, on redirige sur le contexte 'creer_compte_nom'
    *   Le client entre un nom valide (voir RE_NOM_VALIDE) :
        *   Le nom de compte existe
            Dans ce cas, on le redirige sur le contexte 'entrer_mdp'
        *   Le nom de compte n'existe pas
            On affiche l'erreur correspondante et on boucle
    *   Le nom de compte est invalide :
        Dans ce cas, on affiche une erreur correspondante et on boucle
    
    """
    def __init__(self):
        """Constructeur du contexte"""
        Contexte.__init__(self, "entrer_nom")
        self.opts.emt_ncod = False
    
    def get_prompt(self, emt):
        """Message de prompt"""
        return "Votre compte :"
    
    def accueil(self, emt):
        """Message d'accueil"""
        return "Entrez votre nom de compte ou 'nouveau' pour en creer un.\n" \
                "Un seul compte par personne est autorise."
    
    def interpreter(self, emt, msg):
        """Méthode appelée quand un message est réceptionné"""
        if RE_NOUVEAU.search(msg): # le client demande un nouveau compte
            self.envoyer(emt, "Nouveau joueur")
        elif RE_NOM_VALIDE.search(msg):
            self.envoyer(emt, "Nom valide")
        else:
            self.envoyer(emt, "Nom invalide")

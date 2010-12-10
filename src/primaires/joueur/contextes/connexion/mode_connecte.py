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


"""Fichier contenant le contexte 'personnage:connexion:mode_connecte"""

from primaires.interpreteur.contexte import Contexte
from primaires.interpreteur.masque.fonctions import *


class ModeConnecte(Contexte):
    """Le contexte de mode connecté.
    C'est une petite instution à lui tout seul.
    A partir du moment où un joueur se connecte, il est connecté à ce contexte.
    Les commandes se trouvent définies dans ce contexte. En revanche, d'autres
    contextes peuvent venir se greffer par-dessus celui-ci. Mais il reste
    toujours un contexte présent dans la pile des contextes du joueur dès
    lors qu'il est connecté.
    
    """
    nom = "personnage:connexion:mode_connecte"
    
    def __init__(self, pere):
        """Constructeur du contexte"""
        Contexte.__init__(self, pere)
        self.opts.prompt_clr = ""
        self.opts.prompt_prf = ""
    
    def accueil(self):
        """Message d'accueil du contexte"""
        return "Vous êtes connecté"""
    
    def get_prompt(self):
        """Méthode du prompt du contexte"""
        return "[0000000]"
    
    def interpreter(self, msg):
        """Méthode d'interprétation"""
        commandes = type(self).importeur.interpreteur.commandes
        dic_masques = {}
        valide = commandes.valider(self.pere.joueur, dic_masques, \
                chaine_vers_liste(msg))
        if not valide:
            self.pere.envoyer("|err|Commande invalide : {0}.|ff|".format(msg))

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


"""Fichier contenant le contexte "personnage:creation:langue_cmd"""

import re

from primaires.interpreteur.contexte import Contexte
from primaires.format.fonctions import supprimer_accents

# Constantes
LANGUES_DISPONIBLES = ['francais', 'anglais']

class LangueCMD(Contexte):
    """Contexte demandant au client de choisir la langue de ses commandes.
    Les commandes qu'il entrera par la suite seront fonction de cette
    option.
    
    """
    nom = "personnage:creation:langue_cmd"
    
    def __init__(self, pere):
        """Constructeur du contexte"""
        Contexte.__init__(self, pere)
    
    def accueil(self):
        """Message d'accueil du contexte"""
        return \
            "\n|tit|-------= Choix de la langue =-------|ff|\n" \
            "Entrez l'un des |ent|choix|ff| proposés ci-après.\nLa langue " \
            "choisie sera celle des commandes en jeu ; si vous n'êtes pas\n" \
            "familiarisé avec les MUDs, nous vous conseillons le français. " \
            "Une fois\nen jeu, vous pourrez toujours changer grâce à la " \
            "commande |cmd|options|ff|.\n\n" \
            "Langues disponibles : |cmd|français|ff|, |cmd|anglais|ff|"
    
    def get_prompt(self):
        """Message de prompt"""
        return "Entrez le nom de la langue : "
    
    def interpreter(self, msg):
        """Méthode d'interprétation"""
        msg = supprimer_accents(msg).lower()
        if msg not in LANGUES_DISPONIBLES:
            self.pere << "|err|Cette langue n'est pas disponible.|ff|"
        else:
            self.pere.joueur.langue_cmd = msg
            races = type(self).importeur.perso.races
            if races:
                self.migrer_contexte("personnage:creation:choix_race")
            else:
                self.pere.compte.ajouter_joueur(self.pere.joueur)
                
                self.pere.joueur.pre_connecter()

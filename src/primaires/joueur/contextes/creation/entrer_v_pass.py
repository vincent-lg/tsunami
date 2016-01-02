# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 LE GOFF Vincent
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

import hashlib

from primaires.interpreteur.contexte import Contexte

class EntrerVPassJoueur(Contexte):
    nom = "joueur:creation:entrer_v_pass"
    def accueil(self):
        """Message d'accueil du contexte"""
        return \
            "\n|tit|----= Mot de passe du joueur de Vancia =----|ff|\n" \
            "Entrez à présent le mot de passe que vous entriez " \
            "sur Vancia\npour vous connecter avec ce joueur."
    
    def get_prompt(self):
        """Message de prompt"""
        return "Mot de passe : "
    
    def interpreter(self, msg):
        """Méthode d'interprétation"""
        mdp = hashlib.new("md5", msg.encode())
        mdp = mdp.digest()
        if mdp == self.pere.joueur.v_mot_de_passe:
            joueur = self.pere.joueur
            del joueur.v_mot_de_passe
            joueur.instance_connexion = self.pere
            self.migrer_contexte("personnage:creation:langue_cmd")
        else:
            self.pere << "|err|Mot de passe inconnu.|ff|"

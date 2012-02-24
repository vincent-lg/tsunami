# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Fichier contenant le contexte "personnage:creation:recup_vancia"""

from primaires.interpreteur.contexte import Contexte

class RecupVancia(Contexte):
    """Contexte demandant au client d'entrer le nom de son personnage sous Vancia.
    
    Le joueur entré doit :
    -   Exister, bien sûr
    -   Ne pas avoir de compte
    -   Avoir un attribut v_mot_de_passe
    
    Si ces conditions sont remplies, on redirige vers entrer_v_pass.
    
    """
    
    nom = "personnage:creation:recup_vancia"
    def __init__(self, pere):
        """Constructeur du contexte"""
        Contexte.__init__(self, pere)
        self.opts.rci_ctx_prec = "connex:connexion:choix_personnages"
    
    def accueil(self):
        """Message d'accueil du contexte"""
        return \
            "\n|tit|----= Importer un joueur depuis Vancia =----|ff|\n" \
            "Vous pouvez ici récupérer vos joueurs créés sur Vancia " \
            "avant la migration.\nLe joueur sera ensuite ajouté à " \
            "votre compte. Vous pouvez récupérer plusieurs\n" \
            "joueurs de Vancia et les regrouper dans le même compte.\n" \
            "Vous devez d'ailleurs le faire si vous avez " \
            "des clones, car|rg|\nun compte par personne seulement doit " \
            "être créé.|ff|\n\n" \
            "Entrez |ent|le nom|ff| du joueur que vous souhaitez importer."
    
    def get_prompt(self):
        """Message de prompt"""
        return "Nom du joueur : "
    
    def interpreter(self, msg):
        """Méthode d'interprétation"""
        msg = msg.capitalize()
        try:
            joueur = importeur.joueur.joueurs[msg]
        except KeyError:
            self.pere << "|err|Ce joueur n'existe pas.|ff|"
        else:
            if joueur.compte is self.pere.compte:
                self.pere << "|err|Ce joueur est déjà lié à ce compte.|ff|"
                return
            elif joueur.compte is not None:
                self.pere << "|err|Ce joueur est déjà lié à un autre compte.|ff|"
                return
            if not hasattr(joueur, "v_mot_de_passe"):
                self.pere << "|err|Ce joueur a apparemment été déjà " \
                        "importé ailleurs.|ff|"
                return
            
            self.pere.joueur = joueur
            self.migrer_contexte("joueur:creation:entrer_v_pass")

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


"""Package contenant la commande 'éjecter'"""

from primaires.interpreteur.commande.commande import Commande

class CmdEjecter(Commande):
    
    """Commande 'éjecter'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "éjecter", "eject")
        self.nom_categorie = "moderation"
        self.groupe = "administrateur"
        self.schema = "<nom_joueur>"
        self.aide_courte = "éjecte un joueur"
        self.aide_longue = \
                "Cette commande permet d'éjecter un joueur, c'est-" \
                "à-dire provoquer sa déconnexion. C'est généralement un " \
                "avertissement de modération (le joueur est déconnecté " \
                "mais peut se reconnecter facilement)."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        joueur = dic_masques["nom_joueur"].joueur
        if not joueur.est_connecte():
            personnage << "|err|Ce joueur n'est pas connecté.|ff|"
            return
        
        if joueur.est_immortel():
            personnage << "|err|Vous ne pouvez éjecter un administrateur.|ff|"
            return
        
        joueur.envoyer("|rg|VOUS ÊTES ÉJECTÉ DU SERVEUR.|ff|")
        joueur.instance_connexion.deconnecter("Éjection")
        personnage << "|att|Le joueur {} a été éjecté.|ff|".format(
                joueur.nom)

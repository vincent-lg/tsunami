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


"""Fichier contenant le paramètre 'joueur' de la commande 'bannir'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmJoueur(Parametre):
    
    """Commande 'bannir joueur'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "joueur", "player")
        self.schema = "<nom_joueur>"
        self.aide_courte = "banni définitivement un joueur"
        self.aide_longue = \
            "Cette commande permet de bannir définitivement un joueur. " \
            "Toutefois, si le joueur est déjà banni, utiliser cette " \
            "commande une nouvelle fois permet de lever le bannissement."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        joueur = dic_masques["nom_joueur"].joueur
        if joueur.est_immortel():
            personnage << "|err|Vous ne pouvez bannir un administrateur.|ff|"
            return
        
        if joueur in importeur.connex.joueurs_bannis:
            importeur.connex.joueurs_bannis.remove(joueur)
            personnage << "Le joueur {} a été débanni.".format(joueur.nom)
        else:
            if joueur in importeur.connex.bannissements_temporaires:
                del importeur.connex.bannissements_temporaires[joueur]
            
            if joueur.est_connecte():
                joueur.envoyer("|rg|VOUS ÊTES BANNI DU SERVEUR.|ff|")
                joueur.instance_connexion.deconnecter("Bannissement temporaire")
            importeur.connex.joueurs_bannis.append(joueur)
            personnage << "|att|Vous bannissez {}|ff|.".format(
                    joueur.nom)

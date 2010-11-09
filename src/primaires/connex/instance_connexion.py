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


"""Ce fichier définit la classe InstanceConnexion, détaillée plus bas."""

from primaires.connex.motd import MOTD

class InstanceConnexion:
    """Classe représentant une instance de connexion.
    Elle est là pour faire la jonction entre un client connecté et un
    personnage.
    
    """
    importeur = None
    
    def __init__(self, client):
        """Constructeur d'une instance de connexion.
        On peut y trouver trois informations :
        *   le client connecté
        *   l'emetteur
        *   le contexte
        
        """
        self.client = client
        self.emetteur = None
        self.contexte = None
        self.envoyer(MOTD.encode())
        self.contexte = type(self).importeur.interpreteur.contextes[ \
                'entrer_nom']
        self.contexte.migrer_contexte(self, 'entrer_nom')
    
    def _get_contexte_actuel(self):
        return self.contexte
    
    contexte_actuel = property(_get_contexte_actuel)
    
    def envoyer(self, message):
        """Envoie au client le message.
        Le message passé doit être un type bytes.
        On l'envoie donc telle quelle.
        
        """
        self.client.envoyer(message)
    
    def receptionner(self, message):
        """Cette méthode est appelée quand l'instance de connexion
        réceptionne un message. Deux cas sont psosibles :
        *   contexte n'est pas None
            Dans ce cas, on demande au contexte de traiter le message.
            On lui passe en paramètre l'instance (self)
        *   contexte est à None
            Dans ce cas, on envoie le message à l'émetteur qui se charge
            de l'interpréter.
        
        Note: cela fait que les contextes peuvent accepter soit une instance
        de connexion, soit un émetteur. Les contextes à attendre
        une instance ne seront pas nombreux : ce seront ceux appelés
        à la connexion / création de compte. Tous les autres auront un
        personnage défini.
             
        """
        if self.contexte: # le personnage ne semble pas encore connecté
            self.contexte.receptionner(self, message)
        else:
            self.emetteur.receptionner(message)
    
    def migrer_contexte(self, nouveau_contexte):
        """Méthode de migration d'un contexte à un autre.
        On peut passer le contexte sous la forme d'une chaîne.
        Dans ce cas, on le cherche dans l'interpréteur.
        
        """
        if type(nouveau_contexte) is str:
            nouveau_contexte = type(self).importeur.interpreteur.contextes[ \
                    nouveau_contexte]
            self.envoyer(nouveau_contexte.accueil(self).encode())
        self.contexte = nouveau_contexte

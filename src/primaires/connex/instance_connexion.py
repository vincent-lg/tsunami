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
from primaires.format.fonctions import *

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
        *   la file d'attente des messages à envoyer [1]
        
        [1] Quand on envoie un message grâce à la fonction 'envoyer',
            on ne l'envoie pas directement au client.
            On stocke le message dans la file d'attente. A chaque tour de
            boucle synchro, ou en cas de déconnexion du client, on lui envoie
            toute la file d'attente d'un coup.
        
        """
        self.client = client
        self.emetteur = None
        self.file_attente = [] # file d'attente des messages à envoyer
        self.contexte = type(self).importeur.interpreteur. \
            contextes["connex:connexion:afficher_MOTD"](self)
        self.contexte.actualiser()
        self.contexte.migrer_contexte("connex:connexion:entrer_nom")
        self.nbr_essaie = 0
    
    def _get_contexte_actuel(self):
        return self.contexte
    
    contexte_actuel = property(_get_contexte_actuel)
    
    def _get_encodage(self):
        """Retourne l'encodage de l'émetteur ou 'Utf-8'."""
        encodage = "Utf-8"
        if self.emetteur and self.emetteur.encodage:
            encodage = self.emetteur.encodage
        
        return encodage
    
    encodage = property(_get_encodage)
    
    def deconnecter(self, msg):
        """Méthode pour déconnecter le client"""
        self.envoyer_file_attente(ajt_prompt = False)
        if self.client:
            self.client.deconnecter(msg)
            self.client = None
    
    # Fonctions de préparation avant l'envoi
    def formater_message(self, msg):
        """Retourne le message formaté en fonction des diverses options
        du contexte et aussi du type d'entrée.
        msg peut être une chaîne non encodée ('str') ou encodée ('bytes').
        
        Dans tous les cas, on retourne une chaîne encodée ('bytes').
        
        """
        # On récupère les informations de formattage (charte graphique)
        cfg_charte = type(self.importeur).anaconf.get_config("charte_graph")
        
        # On convertit tout en bytes, c'est plus simple ainsi
        # On doit déduire l'encodage qui sera éventuellement utilisé
        encodage = self.encodage
        msg = get_bytes(msg, encodage)
        
        # Ajout de la couleur
        msg = ajouter_couleurs(msg, cfg_charte)
        # On remplace les caractères spéciaux
        msg = remplacer_sp_cars(msg)
        # Suppression des accents si l'option du contexte est activée
        if self.contexte.opts.sup_accents:
            msg = supprimer_accents(msg)
        # On remplace les sauts de ligne
        msg = convertir_nl(msg)
        
        return msg
    
    def envoyer(self, msg):
        """Envoie au client le message.
        On est capable d'envoyer deux types de message :
        *   un type str : dans ce cas, on l'encode et on peut y appliquer
            pas mal d'options du contexte
        *   un type bytes : on l'envoie tel quel ou presque
        
        Note importante : le message n'est pas envoyé directement au client.
        Il est stocké, sous la forme d'une chaîne bytes, dans la file
        d'attente et envoyé dans deux circonstances :
        *   si on demande à l'instance connexion de se déconnecter
            Dans ce cas, aucun prompt n'est envoyé.
        *   à chaque tour de la boucle synchro
        
        """
        msg = self.formater_message(msg)
        self.file_attente.append(msg)
    
    def get_prompt(self):
        """Méthode retournant le prompt déduit du contexte.
        Le prompt retourné est encodé.
        
        """
        prompt = self.formater_message(self.contexte.get_prompt())
        
        # Préfixe et suffixe du prompt
        if prompt:
            pfx_prompt = self.contexte.opts.prompt_prf
            sfx_prompt = ""
            # Coloration du prompt
            if self.contexte.opts.prompt_clr:
                pfx_prompt = self.contexte.opts.prompt_clr + pfx_prompt
                sfx_prompt += "|ff|"
            pfx_prompt = self.formater_message(pfx_prompt)
            sfx_prompt = self.formater_message(sfx_prompt)
            # On ajoute les préfixes et suffixes au prompt
            prompt = pfx_prompt + prompt + sfx_prompt
        
        return prompt
    
    def get_file_attente(self):
        """Récupère la file d'attente.
        Retourne les messages sous la forme d'un type bytes (chaîne encodée).
        
        """
        msg = NL.join(self.file_attente)
        
        return msg
    
    def envoyer_file_attente(self, ajt_prompt = True):
        """On récupère puis on envoie la file d'attente des messages à envoyer.
        On ajoute le prompt à la fine d'attente si ajt_prompt est à True.
        
        """
        if self.file_attente:
            msg = self.get_file_attente()
            self.file_attente = []
            if ajt_prompt:
                msg += 2 * NL + self.get_prompt()
            else:
                msg += NL
        
            if self.client:
                self.client.envoyer(msg)
    
    def receptionner(self, message):
        """Cette méthode est appelée quand l'instance de connexion
        réceptionne un message. Deux cas sont possibles :
        *   contexte n'est pas None
            Dans ce cas, on demande au contexte de traiter le message.
            On lui passe en paramètre l'instance (self).
        *   contexte est à None
            Dans ce cas, on envoie le message à l'émetteur qui se charge
            de l'interpréter.
        
        Note : cela fait que les contextes peuvent accepter soit une instance
        de connexion, soit un émetteur. Les contextes à attendre
        une instance ne seront pas nombreux : ce seront ceux appelés
        à la connexion / création de compte. Tous les autres auront un
        personnage défini.
        
        """
        if self.contexte: # Le personnage ne semble pas encore connecté
            self.contexte.receptionner(message)
        else:
            self.emetteur.receptionner(message)
    
    def migrer_contexte(self, nouveau_contexte):
        """Méthode de migration d'un contexte à un autre.
        On peut passer le contexte sous la forme d'une chaîne.
        Dans ce cas, on le cherche dans l'interpréteur.
        
        """
        if type(nouveau_contexte) is str:
            nouveau_contexte = type(self).importeur.interpreteur. \
                contextes[nouveau_contexte]
            self.envoyer(nouveau_contexte.accueil())
        self.contexte = nouveau_contexte

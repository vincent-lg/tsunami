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

from abstraits.obase import BaseObj
from primaires.format.fonctions import *
from .motd import MOTD

import telnetlib as tlib

OPTIONS = {
    "masquer": tlib.IAC + tlib.WILL + tlib.ECHO,
    "afficher": tlib.IAC + tlib.WONT + tlib.ECHO,
}

class InstanceConnexion(BaseObj):
    """Classe représentant une instance de connexion.
    
    Elle est là pour faire la jonction entre un client connecté et un
    personnage.
    
    """
    
    def __init__(self, client, creer_contexte=True):
        """Constructeur d'une instance de connexion.
        
        On peut y trouver trois informations :
        *   le client connecté
        *   le compte émetteur (une fois qu'il est déclaré)
        *   le personnage connecté (une fois qu'il l'est)
        *   le contexte
        *   la file d'attente des messages à envoyer [1]
        
        [1] Quand on envoie un message grâce à la fonction 'envoyer',
            on ne l'envoie pas directement au client.
            On stocke le message dans la file d'attente. A chaque tour de
            boucle synchro, ou en cas de déconnexion du client, on lui envoie
            toute la file d'attente d'un coup.
        
        """
        BaseObj.__init__(self)
        self.client = client
        self.compte = None
        self.joueur = None
        self.file_attente = [] # file d'attente des messages à envoyer
        self.contexte = None
        self.nb_essais = 0
        self.nb_msg = 0 # nombre de messages envoyés
        self.avec_prompt = True
        
        if creer_contexte:
            self.contexte = type(self).importeur.interpreteur. \
                contextes["connex:connexion:afficher_MOTD"](self)
            self.contexte.actualiser()
            self.contexte.migrer_contexte("connex:connexion:entrer_nom")
    
    def __getnewargs__(self):
        """Méthode retournant les valeurs par défaut du constructeur"""
        return (None, False)
    
    def __lshift__(self, msg):
        """Redirige vers 'envoyer'"""
        self.envoyer(msg)
        return self
    
    def _get_contexte_actuel(self):
        """Retourne le contexte actuel de l'instance.
        -   si le joueur est défini et connecté, alors on retourne
            le contexte actuel du joueur.
        -   sinon, on retourne le contexte de l'isntance
        
        """
        if self.joueur and self.joueur.est_connecte():
            contexte = self.joueur.contexte_actuel
        else:
            contexte = self.contexte
        
        return contexte
    
    def _set_contexte_actuel(self, nouveau_contexte):
        """On change le nouveau contexte. Le contexte peut être de
        différentes provenances (voir _get_contexte_actuel) et on s'assure
        que le contexte modifié soit bien celui actuellement appelé (soit
        celui de l'instance de connexion, soit celui du joueur).
        
        """
        if self.joueur and self.joueur.est_connecte():
            self.joueur.contexte_actuel = nouveau_contexte
        else:
            self.contexte = nouveau_contexte
    
    contexte_actuel = property(_get_contexte_actuel, _set_contexte_actuel)
    
    @property
    def adresse_ip(self):
        """Retourne l'adresse IP de l'instance ou 'inconnue'"""
        if self.client:
            adresse = self.client.adresse_ip
        else:
            adresse = "inconnue"
        
        return adresse
    
    def est_connecte(self):
        client = self.client
        if not client:
            return False
        if not client.socket:
            return False
        if client.socket.fileno() < 0:
            return False
        return True
    
    def connexion_locale(self):
        """Retourne True si l'adresse IP est locale, False sinon."""
        return self.adresse_ip == "127.0.0.1"
    
    def creer_depuis(self, autre):
        """Cette méthode se charge de construire self sur le modèle de autre
        (une autre instance de connexion).
        
        """
        if autre.compte:
            self.compte = autre.compte
        if autre.joueur:
            self.joueur = autre.joueur
            self.joueur.instance_connexion = self
        if autre.contexte:
            self.contexte = \
                type(self).importeur.interpreteur.contextes[ \
                autre.contexte.nom](self)
        if self.joueur:
            for i, contexte in enumerate(self.joueur.contextes):
                contexte.pere = self
    
    def _get_encodage(self):
        """Retourne l'encodage du compte ou 'Utf-8'."""
        encodage = "Utf-8"
        if self.compte:
            encodage = self.compte.encodage
        
        return encodage
    
    encodage = property(_get_encodage)
    
    def deconnecter(self, msg):
        """Méthode pour déconnecter le client.
        Si un joueur est lié à l'instance, on demande la pré-déconnexion
        du joueur.
        
        """
        self.envoyer_file_attente(ajt_prompt = False)
        if self.client and self.client.est_connecte():
            self.client.deconnecter(msg)
            self.client = None
        
        if self.joueur:
            self.joueur.pre_deconnecter()
    
    # Fonctions de préparation avant l'envoi
    def formater_message(self, msg):
        """Retourne le message formaté en fonction des diverses options
        du contexte et aussi du type d'entrée.
        msg peut être une chaîne non encodée ('str') ou encodée ('bytes').
        
        Dans tous les cas, on retourne une chaîne encodée ('bytes').
        
        """
        # On récupère les informations de formattage (charte graphique)
        cfg_charte = type(self.importeur).anaconf.get_config("charte_graph")
        
        # Si le compte le spécifie, on supprime les codes couleurs
        if self.compte and not self.compte.couleur:
            msg = supprimer_couleurs(msg)
        
        # On convertit tout en bytes, c'est plus simple ainsi
        # On doit déduire l'encodage qui sera éventuellement utilisé
        encodage = self.encodage
        msg = get_bytes(msg, encodage)
        
        # Ajout de la couleur
        msg = ajouter_couleurs(msg, cfg_charte)
        
        if not self.contexte_actuel.opts.aff_sp_cars:
            # On remplace les caractères spéciaux
            msg = remplacer_sp_cars(msg)
        
        # Suppression des accents si l'option du contexte est activée
        if self.contexte_actuel.opts.sup_accents:
            msg = supprimer_accents(msg)
        # On remplace les sauts de ligne
        msg = convertir_nl(msg)
        
        return msg
    
    def envoyer(self, msg):
        """Envoie au client le message.
        
        On est capable d'envoyer deux types de message :
        *   un type str : dans ce cas, on l'encode
        *   un type bytes : on n'a pas besoin de l'encoder
        
        Note importante : le message n'est pas envoyé directement au client.
        Il est stocké, sous la forme d'une chaîne bytes, dans la file
        d'attente et envoyé dans deux circonstances :
        *   si on demande à l'instance connexion de se déconnecter
            Dans ce cas, aucun prompt n'est envoyé.
        *   à chaque tour de la boucle synchro
        
        """
        self.nb_msg += 1
        msg = self.formater_message(msg)
        self.file_attente.append(msg)
    
    def get_prompt(self):
        """Méthode retournant le prompt déduit du contexte.
        Le prompt retourné est encodé.
        
        """
        prompt = self.formater_message(self.contexte_actuel.get_prompt())
        
        # Préfixe et suffixe du prompt
        if prompt:
            pfx_prompt = self.contexte_actuel.opts.prompt_prf
            sfx_prompt = ""
            # Coloration du prompt
            if self.contexte_actuel.opts.prompt_clr:
                pfx_prompt = self.contexte_actuel.opts.prompt_clr + \
                        pfx_prompt
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
        
        On ajoute le prompt à la fine d'attente si ajt_prompt est à True et
        si self.avec_prompt.
        
        """
        if self.file_attente:
            msg = self.get_file_attente()
            self.file_attente = []
            if ajt_prompt and self.avec_prompt:
                msg = msg.rstrip(b"\r\n")
                if self.contexte_actuel.opts.nl:
                    msg += NL
                
                msg += NL + self.get_prompt()
            else:
                msg += NL
            self.avec_prompt = True
            
            if self.client:
                self.client.envoyer(msg)
    
    def envoyer_options(self, nom):
        """Envoie des options au client."""
        option = OPTIONS[nom]
        if self.client:
            self.client.envoyer(option)
    
    def sans_prompt(self):
        """Désactive le prompt pour le prochain message envoyé."""
        self.avec_prompt = False
    
    def receptionner(self, message):
        """Cette méthode est appelée quand l'instance de connexion
        réceptionne un message.
        On déduit le contexte actuel grâce à la propriété 'contexte_actuel'.
        
        Note : cela fait que les contextes peuvent accepter soit une instance
        de connexion, soit un joueur. Les contextes à attendre
        une instance ne seront pas nombreux : ce seront ceux appelés
        à la connexion / création de compte. Tous les autres auront un
        personnage défini.
        
        """
        self.contexte_actuel.receptionner(message)
    
    def migrer_contexte(self, nouveau_contexte):
        """Méthode de migration d'un contexte à un autre.
        On peut passer le contexte sous la forme d'une chaîne.
        Dans ce cas, on le cherche dans l'interpréteur.
        
        """
        if type(nouveau_contexte) is str:
            nouveau_contexte = type(self).importeur.interpreteur. \
                contextes[nouveau_contexte]
            self.envoyer(nouveau_contexte.accueil())
        self.contexte_actuel = nouveau_contexte
    
    def write(self, message):
        """Surcharge de la méthode write.
        Cela permet d'utiliser l'instance de connexion comme un descripteur
        de fichier en écriture.
        
        """
        self.envoyer(message)

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


"""Fichier contenant le module primaire communication."""

from abstraits.module import *
from primaires.communication import masques
from primaires.communication import commandes
from primaires.communication.config import cfg_com
from primaires.format.fonctions import *
from .conversations import Conversations
from .canal import Canal
from .canaux import Canaux

class Module(BaseModule):
    
    """Cette classe représente le module qui gère toutes les communications
    entre clients (donc entre joueurs la plupart du temps)
    Elle gère également les canaux de communication.
    
    """
    
    def __init__(self, importeur):
        BaseModule.__init__(self, importeur, "communication", "primaire")
        self.logger = type(self.importeur).man_logs.creer_logger( \
                "communication", "communication")
        self.masques = []
        self.commandes = []
        self.conversations = Conversations()
        self.dernier_canaux = {}
        self._canaux = None
    
    def init(self):
        """Initialisation du module"""
        # On récupère les canaux
        canaux = None
        sous_rep = "canaux"
        fichier = "canaux.sav"
        if self.importeur.supenr.fichier_existe(sous_rep, fichier):
            canaux = self.importeur.supenr.charger(sous_rep, fichier)
        if canaux is None:
            canaux = Canaux()
            self.logger.info("Aucun canal de communication récupéré")
        else:
            if len(canaux) > 1:
                self.logger.info("{} canaux de communication récupérés".format(
                        len(canaux)))
            else:
                self.logger.info("1 canal de communication récupéré")
        
        self._canaux = canaux
        
        BaseModule.init(self)
    
    def config(self):
        """Configuration du module.
        On crée le fichier de configuration afin de l'utiliser plus tard
        pour la mise en forme.
        
        """
        
        type(self.importeur).anaconf.get_config("config_com", \
            "communication/config.cfg", "config communication", cfg_com)
        
        BaseModule.config(self)
    
    def ajouter_masques(self):
        """Ajout des masques"""
        self.importeur.interpreteur.ajouter_masque(masques.message.Message)
        self.importeur.interpreteur.ajouter_masque(
                masques.id_conversation.IdConversation)
        self.importeur.interpreteur.ajouter_masque(masques.canal.Canal)
    
    def ajouter_commandes(self):
        """Ajout des commandes"""
        self.commandes = [
            commandes.dire.CmdDire(),
            commandes.crier.CmdCrier(),
            commandes.emote.CmdEmote(),
            commandes.parler.CmdParler(),
            commandes.repondre.CmdRepondre(),
            commandes.canaux.CmdCanaux(),
        ]
        
        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)
    
    @property
    def canaux(self):
        """Retourne les canaux existants"""
        return self._canaux
    
    def ajouter_canal(self, nom, auteur):
        """Ajoute un canal à la lsite des canaux existants
        Retourne le canal créé.
        
        """
        
        self._canaux[nom] = Canal(nom, auteur)
        return self._canaux[nom]
    
    def supprimer_canal(self, nom):
        """Supprime le canal de la liste des canaux"""
        del self._canaux[nom]
    
    def rejoindre_ou_creer(self, personnage, arguments):
        """Connecte le joueur au canal passé en argument, ou le crée s'il
        n'existe pas.
        
        """
        
        if not arguments or arguments.isspace():
            personnage << "|err|Vous devez préciser un canal.|ff|"
            return
        nom_canal = arguments.split(" ")[0]
        if nom_canal in self.canaux:
            if personnage in self.canaux[nom_canal].connectes:
                personnage << "|err|Vous êtes déjà connecté à ce canal.|ff|"
                return
            self.canaux[nom_canal].rejoindre_ou_quitter(personnage)
            personnage << "|att|Vous êtes à présent connecté au canal " \
                    "{}.|ff|".format(nom_canal)
        else:
            canal = self.ajouter_canal(nom_canal, personnage)
            canal.rejoindre_ou_quitter(personnage)
            personnage << "|att|Le canal {} a été créé. Vous y êtes à " \
                    "présent connecté.|ff|".format(nom_canal)
    
    def quitter_ou_detruire(self, personnage, arguments):
        """Déconnecte le joueur et détruit le canal s'il est vide"""
        if not arguments or arguments.isspace():
            personnage << "|err|Vous devez préciser un canal.|ff|"
            return
        nom_canal = arguments.split(" ")[0]
        if nom_canal not in self.canaux:
            personnage << "|err|Vous n'êtes pas connecté à ce canal.|ff|"
            return
        canal = self.canaux[nom_canal]
        if personnage not in canal.connectes:
            personnage << "|err|Vous n'êtes pas connecté à ce canal.|ff|"
            return
        self.canaux[nom_canal].rejoindre_ou_quitter(personnage)
        res = "Vous avez bien quitté le canal {}.".format(nom_canal)
        if not self.canaux[nom_canal].connectes:
            del self.canaux[nom_canal]
            res += " Vide, il a été détruit."
        personnage << "|att|" + res + "|ff|"
    
    def immerger(self, personnage, arguments):
        """Immerge le personnage dans le canal choisi"""        
        if not arguments or arguments.isspace():
            personnage << "|err|Vous devez préciser un canal.|ff|"
            return
        nom_canal = arguments.split(" ")[0]
        if nom_canal not in self.canaux:
            personnage << "|err|Le canal {} n'existe pas.|ff|".format(nom_canal)
            return
        canal = self.canaux[nom_canal]
        if personnage not in canal.connectes:
            personnage << "|err|Vous n'êtes pas connecté à ce canal.|ff|"
            return
        canal.immerger_ou_sortir(personnage)
    
    def dire_dernier_canal(self, personnage, arguments):
        """Envoie un message au dernier canal utilisé par personnage"""
        if not arguments or arguments.isspace():
            personnage << "Que voulez-vous dire ?"
            return
        if not personnage.nom in self.dernier_canaux:
            personnage << "|err|Vous n'avez utilisé aucun canal.|ff|"
            return
        dernier_canal = self.dernier_canaux[personnage.nom]
        if dernier_canal not in self.canaux:
            personnage << "|err|Le canal {} n'existe pas.|ff|".format(
                    dernier_canal)
            del self.dernier_canaux[personnage.nom]
            return
        canal = self.canaux[dernier_canal]
        if not personnage in canal.connectes:
            personnage << "|err|Vous n'êtes pas connecté au canal " \
                    "{}.|ff|".format(dernier_canal)
            return
        canal.envoyer(personnage, arguments)
    
    def dire_canal(self, personnage, arguments):
        """Envoie un message à un canal, de la part de personnage"""
        nom_canal = arguments.split(" ")[0]
        message = " ".join(arguments.split(" ")[1:])
        canal = self.canaux[nom_canal]
        if personnage not in canal.connectes:
            personnage << "|err|Vous n'êtes pas connecté à ce canal.|ff|"
            return
        if not message or message.isspace():
            personnage << "Que voulez-vous dire ?"
            return
        canal.envoyer(personnage, message)
    
    def traiter_commande(self, personnage, commande):
        """Traite les commandes au premier niveau"""
        res = False
        canaux_connectes = self.canaux.canaux_connectes(personnage)
        noms_canaux_connectes = [canal.nom for canal in canaux_connectes]
        if commande.startswith("+"):
            res = True
            self.rejoindre_ou_creer(personnage, commande[1:])
        elif commande.startswith("-"):
            res = True
            self.quitter_ou_detruire(personnage, commande[1:])
        elif commande.startswith(":"):
            res = True
            self.immerger(personnage, commande[1:])
        elif commande.startswith(". "):
            res = True
            self.dire_dernier_canal(personnage, commande[2:])
        elif commande.split(" ")[0] in noms_canaux_connectes:
            res = True
            self.dire_canal(personnage, commande)
        
        return res

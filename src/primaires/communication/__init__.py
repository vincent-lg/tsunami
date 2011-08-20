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
from primaires.format.fonctions import *
from primaires.communication.config import cfg_com
from primaires.communication import masques
from primaires.communication import commandes

from .editeurs.chedit import EdtChedit
from .editeurs.socedit import EdtSocedit
from .editeurs.medit import EdtMedit
from .editeurs.messagerie import EdtMessagerie

from .conversations import Conversations
from .attitudes import Attitudes
from .attitude import INACHEVEE
from .canaux import Canaux
from .canal import *
from .boite_mail import BoiteMail
from .mudmail import *

class Module(BaseModule):
    
    """Classe représentant le module primaire 'communication'.
    
    Ce module gère toutes les communications entre clients (entre joueurs
    la plupart du temps). Il s'occupe également des canaux de communication,
    du mudmail et d'autres systèmes anodins.
    
    """
    
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "communication", "primaire")
        self.logger = type(self.importeur).man_logs.creer_logger( \
                "communication", "communication")
        self.masques = []
        self.commandes = []
        self.conversations = None
        self.attitudes = None
        self._canaux = None
        self.derniers_canaux = {}
        self.mails = None
    
    def config(self):
        """Configuration du module"""
        self.cfg_com = type(self.importeur).anaconf.get_config("config_com", \
            "communication/config.cfg", "config communication", cfg_com)
        self.cfg_com._set_globales({
            "PRIVE": PRIVE,
            "MUET": MUET,
            "INVISIBLE": INVISIBLE,
            "IMM_AUTOCONNECT": IMM_AUTOCONNECT,
            "PERSO_AUTOCONNECT": PERSO_AUTOCONNECT,
        })
        
        BaseModule.config(self)
    
    def init(self):
        """Initialisation du module"""
        self.conversations = Conversations()
        
        # On récupère les attitudes
        attitudes = None
        sous_rep = "communication"
        fichier = "attitudes.sav"
        if self.importeur.supenr.fichier_existe(sous_rep, fichier):
            attitudes = self.importeur.supenr.charger(sous_rep, fichier)
        else:
            attitudes = Attitudes()
        self.attitudes = attitudes
        
        # On récupère les canaux
        canaux = None
        sous_rep = "communication"
        fichier = "canaux.sav"
        if self.importeur.supenr.fichier_existe(sous_rep, fichier):
            canaux = self.importeur.supenr.charger(sous_rep, fichier)
        if canaux is None:
            canaux = Canaux()
        else:
            if len(canaux) > 1:
                self.logger.info("{} canaux de communication récupérés".format(
                        len(canaux)))
            elif len(canaux) == 1:
                self.logger.info("1 canal de communication récupéré")
            else:
                self.logger.info("Aucun canal de communication récupéré")
        self._canaux = canaux
        
        # On crée les canaux par défaut
        cfg_com = self.cfg_com
        for ligne in cfg_com.liste_canaux:
            nom_c = ligne[0]
            if not nom_c in self.canaux:
                self.ajouter_canal(nom_c, None)
                self.logger.info("Création du canal '{}'".format(nom_c))
                self.canaux[nom_c].clr = ligne[1]
                self.canaux[nom_c].flags = ligne[2]
        # Ajout du canal 'info'
        if not "info" in self.canaux:
            chan_info = self.ajouter_canal("info", None)
            self.logger.info("Création du canal 'info'")
            chan_info.clr = cfg_com.couleur_info
            chan_info.flags = MUET | PERSO_AUTOCONNECT
            chan_info.resume = cfg_com.resume_info
        
        # On récupère les mails
        mails = None
        sous_rep = "communication"
        fichier = "mails.sav"
        if self.importeur.supenr.fichier_existe(sous_rep, fichier):
            mails = self.importeur.supenr.charger(sous_rep, fichier)
        if mails is None:
            mails = BoiteMail()
        else:
            if len(mails) > 1:
                self.logger.info("{} mudmails récupérés".format(
                        len(mails)))
            elif len(mails) == 1:
                self.logger.info("1 mudmail récupéré")
            else:
                self.logger.info("Aucun mudmail récupéré")
        self.mails = mails
        
        # On lie la méthode joueur_connecte avec l'hook joueur_connecte
        # La méthode joueur_connecte sera ainsi appelée quand un joueur
        # se connecte
        self.importeur.hook["joueur:connecte"].ajouter_evenement(
                self.joueur_connecte)
        
        BaseModule.init(self)
    
    def ajouter_commandes(self):
        """Ajout des commandes"""
        self.commandes = [
            commandes.dire.CmdDire(),
            commandes.crier.CmdCrier(),
            commandes.emote.CmdEmote(),
            commandes.parler.CmdParler(),
            commandes.repondre.CmdRepondre(),
            commandes.canaux.CmdCanaux(),
            commandes.socedit.CmdSocedit(),
            commandes.attitudes.CmdAttitudes(),
            commandes.messages.CmdMessages(),
        ]
        
        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)
        
        # Ajout des éditeurs
        self.importeur.interpreteur.ajouter_editeur(EdtChedit)
        self.importeur.interpreteur.ajouter_editeur(EdtSocedit)
        self.importeur.interpreteur.ajouter_editeur(EdtMedit)
        self.importeur.interpreteur.ajouter_editeur(EdtMessagerie)
    
    def preparer(self):
        """Préparation du module.
        On nettoie tous les canaux.
        
        """
        for canal in self._canaux.iter().values():
            canal.nettoyer()
    
    @property
    def canaux(self):
        """Retourne les canaux existants"""
        return self._canaux
    
    @property
    def attitudes_jouables(self):
        """Retourne une liste les attitudes jouables"""
        try:
            ret = [att for att in self.attitudes.values() \
                    if att.statut != INACHEVEE]
        except KeyError:
            ret = []
        return ret
    
    def ajouter_canal(self, nom, auteur):
        """Ajoute un canal à la liste des canaux existants
        Retourne le canal créé.
        
        """
        self._canaux[nom] = Canal(nom, auteur, self._canaux)
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
        else:
            canal = self.ajouter_canal(nom_canal, personnage)
            personnage << "|att|Le canal {} a été créé.|ff|".format(nom_canal)
            canal.rejoindre_ou_quitter(personnage)
    
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
        if not personnage.nom in self.derniers_canaux:
            personnage << "|err|Vous n'avez utilisé aucun canal.|ff|"
            return
        dernier_canal = self.derniers_canaux[personnage.nom]
        if dernier_canal not in self.canaux:
            personnage << "|err|Le canal {} n'existe pas.|ff|".format(
                    dernier_canal)
            del self.derniers_canaux[personnage.nom]
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
        
        for att in self.attitudes_jouables:
            if contient(att.cle, commande.split(" ")[0]):
                res = True
                self.attitudes[att.cle].jouer(personnage, commande)
        
        return res
    
    def joueur_connecte(self, joueur):
        """On avertit le joueur s'il a des messages non lus."""
        mails = self.mails.get_mails_pour(joueur, RECU)
        mails = [mail for mail in mails if not mail.lu]
        if len(mails) == 1:
            joueur << "\n|jn|Vous avez un message non lu.|ff|"
        elif len(mails) > 1:
            joueur << "\n|jn|Vous avez {} messages non lus.|ff|".format(
                    len(mails))

# -*-coding:Utf-8 -*

# Copyright (c) 2010 DAVY Guillaume
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

import re
import random

from primaires.interpreteur.contexte import Contexte

## Constantes

# Chaîne de caractère où sont choisis les caractères pour les mots de passe
char_mdp = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

# E-mail envoyé au bout de X tentatives
obj_alerte = "{X} tentatives de connexions au compte {nom} sur {MUD}"
msg_alerte_user = \
    "{X} fois de suite un mot de passe erroné a été entré pour essayé " \
    "de se connecté à votre compte : {nom} sur {MUD}\n" \
    "Si vous ne vous rappelez plus de votre mot de passe vous pouvez\n" \
    "Entrez {oubli} à la place de votre mot de passe et un nouveau " \
    "vous sera envoyé\n"
msg_alerte_admin = \
    "{X} fois de suite un mot de passe erroné a été entré pour essayé " \
    "de se connecté au compte : {nom} sur {MUD}\n" \
    "L'adresse IP de la dernière connexion est : {ip}\n"

# Email pour envoyé le nouveau mot de passe
obj_nouveau_mdp = "Nouveau mot de passe pour {nom} sur {MUD}"
msg_nouveau_mdp = \
    "Un nouveau mot de passe pour le compte {nom} " \
    "sur {MUD} vous a été crée ceux-ci suite à votre demande" \
    "ou à {Y} tentatives erronées\n\n" \
    "Nouveau mot de passe : {password}"

destinateur = "info"

class EntrerPass(Contexte):
    """Contexte demandant au client son mot de passe.
    On peut aboutir à la validation du compte si elle n'est pas fait
    ou alors au choix du personage si tous se passe bien.
    Le nombre de tentative de connexion est limité : un message d'alerte sera
    envoyé après un certain nombre d'essaie et un nouveau mot de passe sera
    envoyé après un autre nombre d'essaie. De plus l'utilisateur se fait
    déconnecté après un certain nombre d'essai. Tout ceci est configurable
    dans le fichier de configuration de connex.
    On peut aussi se faire envoyer un nouveau mot de passe si on a oublié le
    sien.
    """
    
    nom = "connex:connexion:entrer_pass"
    
    def __init__(self, poss):
        """Constructeur du contexte"""
        Contexte.__init__(self, poss)
        self.attente = False
        self.logger = type(self.importeur).man_logs.creer_logger(
            "entrer_pass", "entrer_pass", "entrer_pass.log")
    
    def get_prompt(self):
        """Message de prompt"""
        return "Mot de passe : "
    
    def accueil(self):
        """Message d'accueil"""
        cnx_cfg = type(self.importeur).anaconf.get_config("connex")
        return \
            "\nEntrez votre |cmd|mot de passe|ff| ou |cmd|{0}|ff| si vous " \
            "l'avez oublié.\n".format(cnx_cfg.chaine_oubli)
    
    def envoie_nouveau_MDP(self):
        """Envoie un nouveau mot de passe à l'utilisateur."""
        cnx_cfg = type(self.importeur).anaconf.get_config("connex")
        mdp = "".join(random.sample(char_mdp ,10))
        emt = self.poss.emetteur
        mail = emt.adresse_email
        nom_MUD = type(self.importeur).anaconf.get_config("globale").nom
        emt.mot_de_passe = emt.hash_mot_de_pass(
            cnx_cfg.clef_salage, cnx_cfg.type_chiffrement, mdp)
        objet = obj_nouveau_mdp.format(nom=emt.nom, MUD=nom_MUD)
        message = msg_nouveau_mdp.format(nom=emt.nom, MUD=nom_MUD, \
                                         password=mdp, \
                                         Y=cnx_cfg.nbr_avant_nouveau)
        
        type(self).importeur.email.envoyer(destinateur, mail, objet, message)
        emt.nb_essais = 0
    
    def alerte(self):
        """Méthode appelé quand il y a eu trop de tentative. Elle envoie un
        message à l'admin et à l'utilisateur."""
        oubli = type(self.importeur).anaconf.get_config("connex").chaine_oubli
        X = type(self.importeur).anaconf.get_config("connex").nbr_avant_alerte
        mail = self.poss.emetteur.adresse_email
        nom = self.poss.emetteur.nom
        ip = self.poss.client.adresse_ip
        nom_MUD = type(self.importeur).anaconf.get_config("globale").nom
        admin = type(self.importeur).anaconf.get_config("email").adminMail
        objet = obj_alerte.format(nom=nom, MUD=nom_MUD, X=X)
        message_admin = msg_alerte_user.format(nom=nom, MUD=nom_MUD, X=X,
                                               ip=ip, oubli=oubli)
        message_user = msg_alerte_admin.format(nom=nom, MUD=nom_MUD, X=X, ip=ip)
        
        self.logger.warning("Mot de passe erroné pour {nom}, {X} essaie " \
            "depuis la dernière connexion réussi, ip : {ip}.".format(nom=nom, \
            X=X,ip=ip))
        type(self).importeur.email.envoyer(destinateur, mail, objet, \
                                           message_admin)
        type(self).importeur.email.envoyer(destinateur, admin, objet, \
                                           message_user)
    
    def action(self):
        """Méthode appelé quand il y a eu beaucoup trop de tentative.
        Elle envoie un message à l'admin et envoie un nouveau mot de
        passe à l'utilisateur."""
        nom = self.poss.emetteur.nom
        ip=self.poss.client.adresse_ip
        nom_MUD = type(self.importeur).anaconf.get_config("globale").nom
        admin = type(self.importeur).anaconf.get_config("email").adminMail
        X = type(self.importeur).anaconf.get_config("connex").nbr_avant_nouveau
        objet = obj_alerte.format(nom=nom, MUD=nom_MUD, X=X)
        message = msg_alerte_admin.format(nom=nom, MUD=nom_MUD, X=X, ip=ip)
        
        self.logger.warning("Mot de passe erroné pour {nom}, {X} essaie " \
            "depuis la dernière connexion réussi, ip : {ip}.".format(nom=nom, \
            X=X,ip=ip))
        self.envoie_nouveau_MDP()
        type(self).importeur.email.envoyer(destinateur, admin, objet, \
                                           message)
    
    def arreter_attente(self):
        self.attente = False
        self.poss.envoyer("Mot de passe incorrect")
    
    def interpreter(self, msg):
        """Méthode appelée quand un message est réceptionné"""
        if not self.attente:
            emt = self.poss.emetteur
            cnx_cfg = type(self.importeur).anaconf.get_config("connex")
            mot_de_passe = emt.hash_mot_de_pass(cnx_cfg.clef_salage, \
                                                cnx_cfg.type_chiffrement, msg)
            
            self.poss.nb_essais += 1
            emt.nb_essais += 1
            
            if msg == cnx_cfg.chaine_oubli:
                self.envoie_nouveau_MDP()
                self.poss.envoyer( \
                    "Un nouveau mot de passe vous a été envoyé par mail")
            elif emt.mot_de_passe == mot_de_passe:
                emt.nb_essais = 0
                if emt.valide:
                    self.migrer_contexte("connex:connexion:choix_personnages")
                else:
                    self.migrer_contexte("connex:creation:validation")
            else:
                self.logger.debug("Mot de passe erroné pour {nom}, {X} " \
                    "essaie depuis la dernière connexion réussi. Et {Y} " \
                    "depuis la connexion de {ip}.".format(nom=emt.nom, \
                    X=emt.nb_essais, Y=self.poss.nb_essais, \
                    ip=self.poss.client.adresse_ip))
                if emt.nb_essais == cnx_cfg.nbr_avant_alerte:
                    self.alerte()
                elif emt.nb_essais == cnx_cfg.nbr_avant_nouveau:
                    self.action()
                if self.poss.nb_essais != 0 and self.poss.nb_essais % \
                   cnx_cfg.nbr_avant_logout == 0:
                    self.poss.envoyer("Mot de passe incorrect")
                    self.poss.envoyer("Déconnexion trop d'essaie.")
                    self.poss.deconnecter("Déconnexion trop d'essaie.")
                else:
                    self.attente = True
                    type(self).importeur.diffact.ajouter_action( \
                        "mot de passe erroné", cnx_cfg.seconde_à_attendre, \
                        self.arreter_attente)

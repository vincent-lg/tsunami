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

# TODO: primaire/interpreteur/contexte/__init__.py

# TODO: et si il y a pas de serveur mail configuré ?
# TODO: Mutualisé le code de hash
# TODO: Adresse mail admin, pour le from des messages et a qui envoyé ceux pour administrateur
# TODO: Oublie mieux dans le nom du compte plutôt que le mot de passe pour les oublies de pseudo

# TODO: Message compte bien crée
# TODO: Logger les erreurs

import re
import random
import string

from primaires.interpreteur.contexte import Contexte

## Constantes

# Email envoyé au bout de X tentatives
msg_user_tentatives = \
    "{X} fois de suite un mot de passe erroné a été entré pour essayé " \
    "de se connecté à votre compte : {compte} sur {MUD}\n" \
    "Si vous ne vous rappelez plus de votre mot de passe vous pouvez\n" \
    "Entrez {oubli} à la place de votre mot de passe et un nouveau " \
    "vous sera envoyé\n"

# Email envoyé au bout de X tentatives
msg_admin_tentatives = \
    "{X} fois de suite un mot de passe erroné a été entré pour essayé " \
    "de se connecté au compte : {compte} sur {MUD}\n" \
    "L'adresse IP de la dernière connexion est : {ip}\n"

# Email pour envoyé le nouveau mot de passe
msg_newmdp = \
    "Un nouveau mot de passe pour le compte {compte} " \
    "sur {MUD} vous a été crée ceux-ci suite à votre demande" \
    "ou à {Y} tentatives erronées\n\n" \
    "Nouveau mot de passe : {password}"

destinateur = "admin"
admin_mail = "root@localhost"

class EntrerPass(Contexte):
    """Contexte demandant au client son mot de passe
    Ce contexte est censément le premier appelé à la connexion d'un client.
    A la fin soit on aboutit
    
    """
    def __init__(self):
        """Constructeur du contexte"""
        Contexte.__init__(self, "connex:connexion:entrer_pass")
    
    def get_prompt(self, emt):
        """Message de prompt"""
        return "Mot de passe : "
    
    def accueil(self, emt):
        """Message d'accueil"""
        cnx_cfg = type(self.importeur).anaconf.get_config("connex")
        return \
        "\nEntrez votre mot de passe, si vous l'avez oublié entrez {0}" \
        " et un nouveau vous sera envoyé.".format(cnx_cfg.chaine_oubli)
    
    def sendNewMdp(self, emt):
        
        mdp = "".join(random.sample("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", 10))
        
        cnx_cfg = type(self.importeur).anaconf.get_config("connex")
        
        emt.emetteur.mot_de_passe = emt.emetteur.hash_mot_de_pass( cnx_cfg.clef_salage,cnx_cfg.type_chiffrement,mdp)
        
        #TODO
        type(self).importeur.email.envoyer( \
            admin_mail, \
            emt.emetteur.adresse_email, \
            "Nouveau mot de passe pour {nom} sur {MUD}".format(nom=emt.emetteur.nom,MUD="TODO"), \
            msg_newmdp.format(compte = emt.emetteur.nom,MUD="TODO",Y=cnx_cfg.nombre_avant_nouveau, password=mdp) \
        )
        
        emt.emetteur.tentatives_intrusion = 0
    
    def interpreter(self, emt, msg):
        """Méthode appelée quand un message est réceptionné"""
        
        cnx_cfg = type(self.importeur).anaconf.get_config("connex")
        
        if msg==cnx_cfg.chaine_oubli:
            self.sendNewMdp(emt)
            self.envoyer(emt,"Un mail avec un nouveau mot de passe vous a été envoyé")
            return
        
        cnx_cfg = type(self.importeur).anaconf.get_config("connex")
        
        mot_de_passe = emt.emetteur.hash_mot_de_pass(cnx_cfg.clef_salage,cnx_cfg.type_chiffrement,msg)
        
        if emt.emetteur.mot_de_passe == mot_de_passe:
            emt.emetteur.tentatives_intrusion = 0
            if emt.emetteur.valide == True:
                self.migrer_contexte(emt, "connex:connexion:choisir_personnage")
            else:
                self.migrer_contexte(emt, "connex:creation:validation")
        else:
            emt.emetteur.tentatives_intrusion += 1
            if emt.emetteur.tentatives_intrusion==cnx_cfg.nombre_avant_avertissement:
                #TODO
                objet = "{X} tentatives de connexions au compte {compte} sur {MUD}".format( \
                    X = cnx_cfg.nombre_avant_avertissement, \
                    compte = emt.emetteur.nom, \
                    MUD = "TODO" \
                )
                #TODO
                message = msg_admin_tentatives.format( \
                    X = cnx_cfg.nombre_avant_avertissement, \
                    MUD = "TODO", \
                    compte = emt.emetteur.nom, \
                    ip = emt.client.adresse_ip \
                )
                type(self).importeur.email.envoyer(destinateur,emt.emetteur.adresse_email,objet,message)
                type(self).importeur.email.envoyer(destinateur,admin_mail,objet,message)
            elif emt.emetteur.tentatives_intrusion>=cnx_cfg.nombre_avant_nouveau:
                self.sendNewMdp(emt)
                #TODO
                objet = "{X} tentatives de connexions au compte {compte} sur {MUD}".format( \
                    X = cnx_cfg.nombre_avant_nouveau, \
                    compte = emt.emetteur.nom, \
                    MUD = "TODO"
                )
                #TODO
                message = msg_admin_tentatives.format( \
                    X = cnx_cfg.nombre_avant_nouveau, \
                    MUD = "TODO", \
                    compte = emt.emetteur.nom, \
                    ip = emt.client.adresse_ip \
                )
                type(self).importeur.email.envoyer(destinateur,admin_mail,objet,message)
            
            
            if emt.tentatives_intrusion % 3 == 2:
                emt.client.deconnecter("Trop de tentative de connexion")
            #TODO prévenir qu'on le jarte
            emt.tentatives_intrusion += 1
            self.envoyer(emt, "Password incorrect. " \
                        "Veuillez l'entrer à nouveau.")
            

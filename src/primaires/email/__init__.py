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


"""Ce fichier contient le module primaire email."""

import smtplib

from email.mime.text import MIMEText
from socket import error as SocketError

from abstraits.module import *
from abstraits.id import ObjetID, est_objet_id
from primaires.email.config import cfg_email
from primaires.format.fonctions import supprimer_accents
from .email import Email

class Module(BaseModule):
    
    """Classe représentant le module 'email'.
    
    Ce module permet, comme son nom l'indique, d'envoyer des e-mails aux
    clients.
    
    NOTE IMPORTANTE: il est préférable de faire tourner, sur le serveur
    hébergeant le projet, un serveur mail afin de pouvoir envoyer ces e-mails.
    Ils peuvent être de diférentes natures, pour avertir le détenteur du
    compte, tout autant que pour garder le contact avec les joueurs.
    Toutefois, une donnée de configuration du module spécifiera si
    le serveur hébergeur possède un serveur mail. Si ce n'est pas le cas,
    aucun mail ne sera envoyé grâce à ce module.
    Restez cependant conscient qu'un serveur mail configuré est un plus
    pour le projet. Contacter un détenteur de compte par mail peut parfois
    être indispensable.
    
    """
    
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "email", "primaire")
        self.logger = type(self.importeur).man_logs.creer_logger("email", \
                "emails", "envoyes.log")
        self.serveur_mail = False # un serveur mail est configuré
        self.nom_hote = "" # aucun nom d'hôte configuré par défaut
        
        self.emails = []
        
        # Le nom d'hôte se configure dans le fichier de configuration. Mais on
        # peut lister plusieurs adresses dans le dictionnaire ci-dessous.
        # Si par exemple vous définissez une clé "info":"webmaster",
        # vous pourrez faire email.envoyer("info", ...) ce qui redirigera vers
        # webmaster@nom_hote_configure.
        self.aliases = {}
    
    def config(self):
        """Méthode de configuration.
        On récupère le fichier de configuration correspondant au module.
        
        """
        conf_mail = type(self.importeur).anaconf.get_config("email", \
                "email/serveur.cfg", "modele email", cfg_email)
        
        # On copie les données de configuration
        self.serveur_mail = conf_mail.serveur_mail
        self.nom_hote = conf_mail.nom_hote
        
        BaseModule.config(self)
    
    def envoyer(self, destinateur, destinataires, sujet, corps):
        """Méthode appelée pour envoyer un message.
        Si le serveur mail n'est pas actif ou que le nom d'hôte n'est pas
        précisé, on n'envoie rien du tout.
        
        Le destinateur doit être soit un alias, soit un nom, mais pas une adresse.
        L'adresse est en effet composée comme suit : {de}@{nom_hote}
        
        Le destinataire peut être une adresse unique sous la forme d'une
        chaîne ou bien une liste d'adresses.
        
        Enfin, le sujet et le message doivent être des chaînes non encodées.
        
        """
        if self.serveur_mail:
            if not self.nom_hote: # le nom d'hôte n'est pas précisé
                self.logger.warning("Impossible d'envoyer le mail à {0} " \
                        "(sujet : {1}) car le nom d'hôte n'est pas précisé " \
                        "dans les données de configuration".format(
                        destinataires, sujet))
            else:
                if destinateur in self.aliases:
                    destinateur = self.aliases[destinateur]
                
                email = Email("{0}@{1}".format(destinateur, self.nom_hote),
                        destinataires, supprimer_accents(sujet), corps)
                
                self.emails.append(email)
                
                email.envoyer()
    
    def boucle(self):
        """Méthode appelée à chaque tour de boucle synchro. Vérifie que
        les mails ont bien été envoyés.
        
        """
        for email in self.emails:
            if not email.isAlive() and email.erreur:
                    self.logger.warning("Impossible d'envoyer le mail à {0} " \
                            "(sujet : {1}) : {2}".format(email.destinataires, \
                            email.sujet, email.erreur))
        
        self.emails = [ email for email in self.emails if email.isAlive() ]

# -*-coding:Utf-8 -*

# Copyright (c) 2011 DAVY Guillaume
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


"""Ce fichier contient la classe Email, détaillée plus bas."""

try:
    import smtplib
    from email.mime.text import MIMEText
    from socket import error as SocketError
except ImportError:
    smtplib = None
import threading

from abstraits.module import *
from abstraits.id import ObjetID, est_objet_id
from primaires.email.config import cfg_email
from primaires.format.fonctions import supprimer_accents

class Email(threading.Thread):
    
    """Classe Email.
    
    Elle permet l'envoi d'un mail de manière asynchrone via l'utilisation
    des threads. Lors de l'envoi d'un mail un thread est créé pour s'occuper
    de cette tâche et se terminera quand le mail sera fini d'être envoyé.
    
    """
    
    def __init__(self, destinateur, destinataires, sujet, corps):
        threading.Thread.__init__(self)
        
        self.destinateur = destinateur
        self.sujet = sujet
        
        # Si le destinataire est une chaîne, on la met en liste
        if type(destinataires) is not list:
            self.destinataires = [destinataires]
        else:
            self.destinataires = destinataires
        
        self.mail = MIMEText(corps.encode("Utf-8"), "plain", "Utf-8")
        self.mail["From"] = destinateur
        self.mail["Subject"] = sujet
        self.mail["To"] = destinataires
        
        self.erreur = None
    
    def envoyer(self):
        self.start()
    
    def run(self):
        # On essaye de se connecter au serveur mail
        try:
            smtp = smtplib.SMTP()
            smtp.connect()
            smtp.sendmail(self.destinateur, self.destinataires,
                    self.mail.as_string())
            smtp.close()
        except SocketError as err:
            self.erreur = err

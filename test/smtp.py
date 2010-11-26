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

import smtpd
import asyncore
import email
import time

class Smtp(smtpd.SMTPServer):
    """Classe représentant un serveur SMTP. C'est un
    serveur ultra-basique qui se contente de reçevoir
    les mails et de les mettres dans une listes
    
    """
    
    #Listes des messages reçu
    msgs = []
    
    def __init__(self):
        """Lance le serveur"""
        smtpd.SMTPServer.__init__(self,('',25), None)
    
    def __del__(self):
        """Stop le serveur"""
        self.close()
    
    def process_message(self, peer, mailfrom, rcpttos, data):
        """Callback appelé quand un message est reçu"""
        self.msgs.append(data.encode() + \
            email.message_from_string(data).get_payload(decode=True))
    
    def attendre_message_de(self,timeout,mail):
        """Attend un message provenant d'un email donné"""
        self.msgs = []
        debut = time.clock()
        while debut + timeout > time.clock():
            asyncore.loop(timeout=0.5,count=1)
            while len(self.msgs)>0:
                message = self.msgs.pop()
                if message.find(mail.encode()) != -1:
                    return message
        return None


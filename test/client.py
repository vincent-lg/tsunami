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

import socket
import time

HOTE = 'localhost'
PORT = 14000

class client():
    
    def __init__(self,smtp):
        self.smtp = smtp
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(0.1)
    
    def __deinit__(self,sm):
        self.socket.close()
    
    def connect(self):
        self.socket.connect((HOTE, PORT))
        return self.attendre_reponse()
    
    def attendre_reponse(self):
        donnee = b""
        try:
            while 1:
                rec = self.socket.recv(100)
                donnee += rec
        except socket.timeout:
            return donnee
    
    def envoyer(self,message):
        self.socket.send(message + b'\n')
        return self.attendre_reponse()
    
    def extraire_code(self,message):
        avant = b"Code de validation : "
        apres = b"Note : si vous avez"
        return int(message[message.index(avant) + \
            len(avant):message.index(apres)])
    
    def creer_compte(self,nom,mdp,mail):
        self.envoyer(b'nouveau')
        self.envoyer(nom.encode())
        self.envoyer(b'1')
        self.envoyer(mdp.encode())
        self.envoyer(mdp.encode())
        self.envoyer(mail.encode())
        time.sleep(0.3)
        self.smtp.loop()
        code=""
        for message in self.smtp.msgs:
            if message.find(mail.encode()) != -1:
                code = self.extraire_code(message)
                self.smtp.msgs.remove(message)
        message = self.envoyer(str(code).encode())
        message.index(b"Choix du personnage")
    
    def connexion(self,nom,mdp):
        self.envoyer(nom.encode())
        message = self.envoyer(mdp.encode())
        message.index(b"Choix du personnage")
    
    

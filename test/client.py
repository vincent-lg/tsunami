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

from tests import EchecTest

#Hote sur lequel se trouvé kassie
HOTE = 'localhost'
#Port sur lequel écoute kassie
PORT = 14000

class Client():
    """Classe représentant un client à Kassie.
    Elle permet de se connecté à kassie mais
    aussi de faire quelque combinaison de commande
    souvent utilisé comme celle pour créé un compte
    ou se connecté
    
    """
    
    def __init__(self,smtp):
        """Construction de la socket"""
        self.smtp = smtp
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(0.1)
    
    def __del__(self):
        """Destructeur du module"""
        self.socket.close()
    
    def connecter(self):
        """Connecter le client"""
        self.socket.connect((HOTE, PORT))
        return self.attendre_reponse()
    
    def attendre_reponse(self):
        """Récupère ce qui attend sur la socket"""
        donnee = b""
        try:
            while 1:
                rec = self.socket.recv(100)
                donnee += rec
        except socket.timeout:
            return donnee
    
    def envoyer(self,message):
        """Envoie un message"""
        self.socket.send(message + b'\n')
        return self.attendre_reponse()
    
    def extraire_code(self,msg):
        """Extrait le code de validation d'un email"""
        avant = b"Code de validation : "
        apres = b"Note : si vous avez"
        return int(msg[(msg.index(avant) + len(avant)):msg.index(apres)])
    
    def creer_compte(self,nom,mdp,mail):
        """Creer un compte sur Kassie"""
        
        try:
            self.envoyer(b'nouveau')
            self.envoyer(nom.encode())
            self.envoyer(b'1')
            self.envoyer(mdp.encode())
            self.envoyer(mdp.encode())
            self.envoyer(mail.encode())
        except socket.error as detail:
            raise EchecTest("Erreur de connexion avec Kassie")
        
        try:
            message = self.smtp.attendre_message_de(1,mail);
        except socket.error as detail:
            raise EchecTest("Erreur de connexion avec le smtp")
            
        if message == None:
            raise EchecTest("Mail de validation non reçue")
        
        try:
            code = self.extraire_code(message)
        except ValueError as detail:
            raise EchecTest("Code introuvable dans le mail")
        
        try:
            message = self.envoyer(str(code).encode())
            message.index(b"Choix du personnage")
        except socket.error as detail:
            raise EchecTest("Erreur de connexion avec Kassie")
        except ValueError as detail:
            raise EchecTest("Réponse attendu de la part de Kassie " \
                "invalide, compte non crée")
    
    def connexion(self,nom,mdp):
        """Se connecter sur Kassie"""
        try:
            self.envoyer(nom.encode())
            message = self.envoyer(mdp.encode())
            message.index(b"Choix du personnage")
        except socket.error as detail:
            raise EchecTest("Erreur de connexion avec Kassie")
        except ValueError as detail:
            raise EchecTest("Réponse attendu de la part de Kassie " \
                    "invalide, connection impossible")

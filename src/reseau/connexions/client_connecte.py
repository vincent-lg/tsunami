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


"""Ce fichier définit la classe ClientConnecte, détaillée plus bas."""

import socket

class ClientConnecte:
    """Cette classe est une classe envelope d'un socket.
    Elle reprend les méthodes utiles à la manipulation des sockets et possède
    quelques attributs et méthodes implémentées pour faciliter son insertion dans
    un serveur TCP.
    
    Cette classe est appelée pour héberger un client connecté, c'est-à-dire
    dont la demande de connexion a été validée par le serveur.
    
    On définit pour chaque connexion instanciée un numéro d'identification
    nommé 'id'. L'id courant sera contenu comme variable statique de cette classe.

    """
    id_courant = 0

    def __init__(self, socket_connecte, infos):
        """Constructeur standard.
        
        On donne à la connexion créée une ID qui lui sera propre.
        Les paramètres à entrer sont :
        - le socket retourné par la méthode accept()
        - les infos de connexion, un tuple contenant :
            - l'adresse IP du client
            - le port sortant du client

        """
        self.id = ClientConnecte.id_courant
        ClientConnecte.id_courant += 1

        # Notre socket connecté
        self.socket = socket_connecte

        # Informations de connexion
        self.adresse_ip = infos[0]
        self.port = infos[1] # le port sortant du client pour se connecter
        
        # Statut de connexion
        self.connecte = True
        
        # Message en cours (il contient la chaîne que le client
        # est en train d'écrire, dans le cas d'un client qui envoie
        # au fur et à mesure les caractères entrés)
        self.message = b""

        # retour : il contient le message retourné en cas de déconnexion
        self.retour = ""
    
    def __str__(self):
        """On affiche l'ID du client, son ip et son port entrant"""
        return "{0} ({1}:{2}, {3})".format( \
            self.id, self.adresse_ip, self.port, self.socket.fileno())

    def nettoyer(self, message):
        """Cette méthode se charge de nettoyer le message passé en paramètre.
        Elle retourne le message nettoyé.

        Les nettoyages effectués sont :
        -   compatibilité telnet Windows : on retire les caractères
            d'effacement et les caractères derrière ce signe
        -   compatibilité tintin++ : on supprime les caractères préfixant
            un accent, sans accent derrière

        """
        # Compatibilité telnet
        car_eff = b"\x08"
        while message.count(car_eff) > 0:
            pos = message.find(car_eff)
            if pos > 0:
                message = message[:pos-1] + message[pos+1:]
            else:
                message = message[pos+1:]

        # Compatibilité Tintin++
        car_eff = 195
        n_message = b""
        for i, car in enumerate(message):
            if not (car == car_eff and i+1<len(message) and \
                    bytes([message[i+1]]).isalpha()):
                n_message += bytes([car])


        message = n_message
        return message

    def decoder(self, message, decodage=0):
        """Test de décodage.
        Fonction récursive : tant qu'on peut décoder, on essaye.

        Si le décodage échoue, une exception sera levée.
        """
        encodages = ['Utf-8', 'Latin-1']
        try:
            actuel = encodages[decodage]
        except IndexError:
            raise UnicodeError("aucun encodage n'a pu etre utilise " \
                    "sur cette chaine")
        try:
            n_message = message.decode(actuel)
            return n_message
        except UnicodeError:
            return self.decoder(message, decodage+1)

    def envoyer(self, message):
        """Envoie d'un message au socket.
        Le message est déjà encodé. Ce n'set plus un type str.
        """
        self.socket.send(message)

    def recevoir(self):
        """Cette méthode se charge de réceptionner le message en attente.

        On appelle la méthode recv du socket.
    En cas d'exception socket.error, on déconnecte le client.

        """
        try:
            message = self.socket.recv(1024)
        except socket.error:
            self.deconnecter("perte de la connexion")
        if message == b"":
            self.deconnecter("perte de la connexion")
        else:
            self.message += message

    def message_est_complet(self):
        """Retourne True si le message se termine par un caractère de fin de
        ligne, False sinon.

        """
        fin_lignes = [b"\r", b"\n"]
        est_complet = False
        for code in fin_lignes:
            if not est_complet:
                est_complet = self.message.endswith(code)
        return est_complet

    def get_message(self):
        """Cette méthode retourne le message complet.
        Elle met à jour self.message en supprimant le message retourné.
        Si plusieurs messages complets sont contenus, on ne retourne que le
        premier.

        """
        message = self.message
        message = message.replace(b"\r", b"\n")
        while message.count(b"\n\n")>0:
            message = message.replace(b"\n\n", b"\n")
        messages = message.split(b"\n")
        self.message = b"\n".join(messages[1:])
        message = messages[0] # on retourne le premier message
        message = self.nettoyer(message)
        return message

    def get_message_decode(self):
        """Cette méthode travaille avec get_message et retourne le message
        décodé, si possible.

        """
        return self.decoder(self.get_message())

    def deconnecter(self, message):
        """Méthode appelée pour déconnecter un client.
        - on ferme la connexion du socket
        - on met à jour le booléen self.connecte
        - on stock le message retourné dans self.retour

        """
        self.socket.close()
        self.connecte = False
        self.retour = message

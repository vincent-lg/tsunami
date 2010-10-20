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


"""Cet exemple met en place un système de chat minimaliste gérant :
- les connexions multiples
- les déconnexions fortuites
- la réception ou l'envoie de messages aux clients

On utilise les fonctions de callback pour paramétrer comment doit
réagir le serveur lors d'une connexion, d'une déconnexion ou d'une
réception d'un message. Consultez le code pour plus d'informations.

"""

import os
import sys

sys.path.append(os.getcwd() + "/../src")

from reseau.connexions.serveur import *

fin_ligne = "\r\n"

# Fonctions de callback

def connexion(serveur, client):
    """Que se passe-t-il quand client se connecte ?"""
    print("Connexion du client {0}".format(client))
    for c in serveur.clients.values():
        if c is not client:
            c.envoyer("$$ {0} se connecte au serveur{1}".format( \
                    client, fin_ligne).encode())

def deconnexion(serveur, client):
    """Que se passe-t-il quand client se déconnecte ?"""
    print("Déconnexion du client {0} : {1}".format(client, client.retour))
    for c in serveur.clients.values():
        if c is not client:
            c.envoyer("** {0} se déconnecte du serveur{1}".format( \
                    client, fin_ligne).encode())

def reception(serveur, client):
    """Que se passe-t-il quand client envoie un message au serveur ?"""
    msg = client.get_message() # msg contient un type bytes, aps str
    print("J'ai réceptionné en bytes {0}".format(msg))
    for c in serveur.clients.values():
        c.envoyer("<{0}> {1}{2}".format(client.id, msg, fin_ligne).encode())


# Création et paramétrage du serveur

serveur = ConnexionServeur(4000) # test sur le port 4000

# Paramétrage des callbacks
# callback lors de la connexion
serveur.callbacks["connexion"].fonction = connexion
serveur.callbacks["connexion"].parametres = (serveur,)

# callback lors de la déconnexion
serveur.callbacks["deconnexion"].fonction = deconnexion
serveur.callbacks["deconnexion"].parametres = (serveur,)

# callback lors de la réception de message
serveur.callbacks["reception"].fonction = reception
serveur.callbacks["reception"].parametres = (serveur,)

# Fin du paramétrage du serveur

serveur.init() # initialisation, indispensable
while True: # le serveur ne s'arrête pas naturellement
    serveur.verifier_connexions()
    serveur.verifier_receptions()

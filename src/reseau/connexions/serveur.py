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


"""Ce fichier définit la classe ConnexionServeur détaillée plus bas.

Pour créer un serveur opérationnel, quelques instructions suffisent :

>>> serveur = ConnexionServeur(4000) # test sur le port 4000
>>> serveur.init() # initialisation, indispensable
>>> while True: # le serveur ne s'arrête pas naturellement
...     serveur.verifier_connexions()
...     serveur.verifier_receptions()

Note importante: une fonction de Callback est utilisée pour définir
des instructions à effectuer dans les cas suivants :
- un client se connecte
- un client se déconnecte
- un client envoie un message réceptionné par le serveur

Ces fonctions, ainsi que leurs paramètres, sont à préciser avant
l'initialisation et le lancement du serveur.

Par défaut, ces fonctions de callback vallent None.

"""

import sys
import socket
import select

from reseau.connexions.client_connecte import ClientConnecte
from bases.fonction import *

class ConnexionServeur:
    """Cette classe représente le socket en écoute sur le port choisit
    dont le rôle est d'ajouter de nouveaux clients et de gérer leurs messages.
    
    Sur une architecture réseau simple, elle n'a besoin d'être instanciée
    qu'une unique fois.
    
    Après son instanciation, on doit appeler dans une boucle les méthodes
    chargées de vérifier les connexions en attente, d'accepter les clients
    éventuels puis d'interroger chaque client pour savoir si des messages
    sont à récupérer.
    
    """
    
    def __init__(self, port, nb_clients_attente=5, nb_max_connectes=-1, \
            attente_connexion=0.05, attente_reception=0.05):
        """Créée un socket en écoute sur le port spécifié.
        - port : le port surlequel on écoute (>1024)
        - nb_clients_attente : le nombre maximum de clients en attente de
          connexion. Ce nombre est passé à la méthode listen du socket
        - nb_max_connectes : le nombre maximum de clients connectés
          Ce peut être utile pour éviter la surcharge du serveur.
          Si ce nombre est dépassé, on accepte puis déconnecte immédiatement
          le client ajouté. On précise
          -1 si on ne veut aucune limite au nombre de clients
        - attente_connexion : temps pendant lequel on attend de nouvelles
          connexions. C'est en fait le Time Out passé à select.select
          quand il s'agit de surveiller les clients qui souhaitent se
          connecter. Ce temps est précisé en seconde (0.05 s = 50 ms)
          Si on souhaite un Time Out infini mettre cette variable à None.
        - attente_reception : temps indiquant pendant combien de temps
          on attend un message à réceptionner sur les clients déjà connectés.
          Ce nombre est passé comme Time Out de select.select quand il s'agit
          de surveiller les sockets connectés. Ce temps est précisé en seconde
          (0.05 s = 50 ms)
          Si on souhaite un Time Out infini mettre cette variable à None.
        
        Petite précision sur l'utilité de select.select :
            On utilise cette fonction pour surveiller un certain nombre
            de sockets. La fonction s'interrompt à la fin du Time Out spécifié
            ou dès qu'un changement est survenu sur les sockets observés.
        
            Ainsi, si on surveille les clients connectés en attendant
            des messages à réceptionner, dès qu'un client aura envoyé un
            nouveau message, la fonction s'interrompera et nous laissera le
            soin de récupérer les messages des clients retournés.
            Si à l'issue du temps d'attente aucun message n'a été réceptionné,
            la fonction s'interrompt et on peut reprendre la main.
        
        """
        self.port = port # port sur lequel on va écouter
        self.nb_clients_attente = nb_clients_attente
        self.nb_max_connectes = nb_max_connectes
        self.attente_connexion = attente_connexion
        self.attente_reception = attente_reception

        self.clients = {} # un dictionnaire {id_client:client}

        # Dictionnaire permettant, depuis un socket, de retrouver l'ID client
        self.filenos = {} # correspondance {fileno_du_socket,id_client}

        # Socket serveur
        self.socket  = None

        # Fonctions de callback
        self.callbacks = {
            # declencheur : (fonction, parametres)
            "connexion":Fonction(None),
            "deconnexion":Fonction(None),
            "reception":Fonction(None),
        }

    def init(self):
        """Cette méthode doit être appelée après l'appel au constructeur.
        Elle se charge d'initialiser le socket serveur et, en somme,
        de le mettre en écoute sur le port spécifié.
        """
        # Initialisation du socket serveur
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # On paramètre le socket
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # On essaye de se mettre en écoute sur le port précisé
        # Si ça ne marche pas, on affiche l'erreur et on quitte immédiatement
        try:
            self.socket.bind(('', self.port))
        except socket.error as erreur:
            print("Le socket serveur n'a pu être connecté: {0}".format(erreur))
            sys.exit(1)

        # On met en écoute le socket serveur
        self.socket.listen(self.nb_clients_attente)

    def get_client_depuis_socket(self, socket):
        """Cette méthode retourne le client connecté, en fonction du
        socket passé en paramètre. On se base sur le fileno() du socket
        pour retrouver l'ID du client et sur le dictionnaaire filenos
        faisant la correspondance.

        On retourne le client trouvé.

        """
        try:
            return self.clients[self.filenos[socket.fileno()]]
        except KeyError:
            raise KeyError("le socket n. {0} n'est pas un socket client" \
                    .format(socket.fileno()))

    def get_clients_sockets(self):
        """Retourne la liste des sockets des différents clients connectés."""
        sockets = []
        for client in self.clients.values():
            sockets.append(client.socket)
        return sockets

    def ajouter_client(self, socket, infos):
        """Cette méthode se charge d'ajouter un client connecté au
        dictionnaire des clients. On en profite pour remplir le dictionnaire
        faisant la correspondance entre ID client et fileno() de socket.

        Cette méthode fait appel à la fonction de callback connexion.

        On retourne le client créé et ajouté.

        """
        client = ClientConnecte(socket, infos)
        # On ajoute le client au dictionnaire des clients (id-client)
        self.clients[client.id] = client

        # On renseigne le dictionnaire {socket.fileno():id_client}
        self.filenos[socket.fileno()] = client.id

        # On appelle la fonction de callback "connexion"
        self.callbacks["connexion"].executer(client)

        return client

    def retirer_client(self, client):
        """Cette méthode se charge de retirer un client des clients
        connectés.

        On doit mettre à jour self.clients mais aussi self.filenos.

        Avant tout cependant, on appelle la fonction de callback "deconnexion".

        """
        # On appelle la fonction de callback "deconnexion"
        self.callbacks["deconnexion"].executer(client)

        # On supprime le client des clients connectés
        if client.id in self.clients.keys():
            del self.clients[client.id]

        # On supprime le socket des filenos enregistrés
        if client.socket.fileno() in self.filenos.keys():
            del self.filenos[client.socket.fileno()]

    def verifier_deconnexions(self):
        """Cette méthode doit être appelée régulièrement pour retirer
        les clients déconnectés.

        """
        for client in list(self.clients.values()):
            if not client.connecte:
                client.socket.close() # au cas où
                self.retirer_client(client)

    def verifier_connexions(self):
        """Cette méthode vérifie si des clients ne sont pas en attente
        de connexion. Elle a un comportement bloquant pendant le temps
        attente_connexion spécifié dans le constructeur de l'objet.

        Elle se charge d'ajouter les clients connectés à la liste
        des clients si le nombre maximum de connecté n'est pas excédé.

        Dans le cas contraire, on envoie au client un message par défaut
        et on le déconnecte du serveur.

        """
        self.verifier_deconnexions()
        # On attend avec select.select qu'une connexion se présente
        # Si aucune connexion ne se présente, au bout du temps indiqué
        # dans self.attente_connexion, select.select s'arrête
        # en levant une exception select.error
        try:
            connexions, none, none = select.select(
                [self.socket], [], [], self.attente_connexion)
        except select.error:
            pass

        # On parcourt la boucle des connexions en attente
        # En toute logique, elle ne possède qu'un client puisque select.select
        # s'interrompt dès qu'elle reçoit une demande de connexion
        for connexion in connexions:
            # On tente d'accepter la connexion
            try:
                socket, infos = connexion.accept()
            except socket.error:
                pass
            else:
                # On vérifie qu'on peut ajouter un nouveau client
                if self.nb_max_connectes >= 0 \
                        and len(self.clients) >= self.nb_max_connectes:
                    # On refuse la connexion
                    socket.send("Ce serveur ne peut accueillir de connexions " \
                        "supplementaires.".encode())
                    socket.close()
                else:
                    # On créée notre client
                    client = self.ajouter_client(socket, infos)

    def verifier_receptions(self):
        """Cette méthode vérifie si des clients ont envoyé des messages
        à réceptionner. Elle se base sur select.select pour cela.

        """
        self.verifier_deconnexions()
        # On attend avec select.select qu'un message soit réceptionné
        # Si aucun message n'est à réceptionner au bout du temps indiqué
        # dans self.attente_reception, select.select s'arrête
        # en levant une exception select.error
        receptions = []
        try:
            receptions, none, none = select.select(
                self.get_clients_sockets(), [], [], self.attente_reception)
        except select.error:
            pass

        # On parcourt la boucle des clients possédant un message à réceptionner
        for socket in receptions:
            # On récupère le client correspondant
            client = self.get_client_depuis_socket(socket)
            client.recevoir()
            # On part du principe que le message est récupéré au fur et à
            # mesure dans les fonctions de callback. Sans quoi, cette
            # instruction provoque une boucle infinie
            while client.message_est_complet():
                # On appelle la fonction de callback "reception"
                self.callbacks["reception"].executer(client)

        # On vérifie une dernière fois que tous les clients sont bien
        # connectés
        self.verifier_deconnexions()

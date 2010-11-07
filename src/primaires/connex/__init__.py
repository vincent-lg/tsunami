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


"""Fichier contenant la classe Connex définissant le module primaire
du même nom.

"""

from abstraits.module import *
from primaires.connex.instance_connexion import InstanceConnexion
from reseau.connexions.client_connecte import ClientConnecte

# Nom du groupe fictif
NOM_GROUPE = "connexions"

class Connex(Module):
    """Module gérant les connexions et faisant donc le lien entre les clients
    connectés et les joueurs, ou leur instance de connexion.
    
    """
    def __init__(self, importeur):
        """Constructeur du module"""
        self.instances = {}
        Module.__init__(self, importeur, "connex", "primaire")
    
    def init(self):
        """Initialisation du module.
        On récupère les instances de connexion et on les stocke dans
        'self.instances' si elles sont encore connectées.
        En cas de crash, les anciennes connexions n'ont pas pu être effacées.
        Cette méthode se charge de faire le ménage également.
        
        """
        
        if NOM_GROUPE in type(self.importeur).parid:
            objets = type(self.importeur).parid[NOM_GROUPE].values()
            print("On récupère de parid")
        else:
            objets = []
            print("On récupère rien")
        
        for inst in objets:
            if inst.client.n_id in type(self.importeur).serveur.clients.keys():
                inst.client = type(self.importeur).serveur.clients[ \
                        inst.client.n_id]
                self.instances[inst.client.n_id] = inst
                print("On récupère", inst)
        
        # On ajoute le dictionnaire 'instances' comme groupe fictif de 'parid'
        type(self.importeur).parid[NOM_GROUPE] = self.instances
        
        Module.init(self)
    
    def __getitem__(self, item):
        """Méthode appelée quand on fait connex[item].
        L'item peut être de plusieurs types :
        -   entier : c'est l'ID du client
        -   client : on récupère son ID
        
        """
        if isinstance(item, ClientConnecte):
            item = item.n_id
        if item not in self.instances.keys():
            raise KeyError("L'ID {0} ne se trouve pas dans les instances " \
                    "connectées".format(repr(item)))
        return self.instances[item]
    
    def ajouter_instance(self, client):
        """Cette méthode permet d'ajouter une instance de connexion.
        Elle est appelée quand la connexion est établie avec le serveur.
        Ainsi, l'instance de connexion est créée avec des paramètres par
        défaut.
        
        """
        instance_connexion = InstanceConnexion(client)
        self.instances[client.n_id] = instance_connexion
    
    def retirer_instance(self, client):
        """L'instance à supprimer peut être de plusieurs types :
        -   entier : c'est l'ID du client
        -   ClientConnecte : on extrait son ID
        
        """
        if isinstance(client, ClientConnecte):
            client = client.n_id
        if client not in self.instances:
            raise KeyError("l'ID {0} ne se trouve pas dans les instances " \
                    "connectées".format(repr(client)))
        instance = self.instances[client]
        del self.instances[client]

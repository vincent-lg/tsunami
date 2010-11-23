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


"""Fichier contenant le module primaire connex."""

from abstraits.module import *
from primaires.connex.instance_connexion import InstanceConnexion
from reseau.connexions.client_connecte import ClientConnecte
from primaires.connex.compte import Compte
from primaires.connex.contextes import liste_contextes
from primaires.connex.config import cfg_connex

# Nom du groupe fictif
NOM_GROUPE = "connexions"

class Module(BaseModule):
    """Module gérant les connexions et faisant donc le lien entre les clients
    connectés et les joueurs, ou leur instance de connexion.
    
    """
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "connex", "primaire")
        InstanceConnexion.importeur = self.importeur
        self.instances = {}
        self.cnx_logger = type(self.importeur).man_logs.creer_logger( \
                "connex", "connexions")
        # Comptes
        self.comptes = {}
        self.cpt_logger = type(self.importeur).man_logs.creer_logger( \
                "connex", "comptes")
    
    def config(self):
        """Configuration du module.
        On crée le fichier de configuration afin de l'utiliser plus tard
        dans les contextes.
        
        """
        type(self.importeur).anaconf.get_config("connex", \
            "connex/connex.cfg", "modele connexion", cfg_connex)
        
        BaseModule.config(self)
    
    def init(self):
        """Initialisation du module.
        On récupère les instances de connexion et on les stocke dans
        'self.instances' si elles sont encore connectées.
        
        """
        if NOM_GROUPE in type(self.importeur).parid:
            objets = type(self.importeur).parid[NOM_GROUPE].values()
        else:
            objets = []
        
        for inst in objets:
            if inst.client.n_id in type(self.importeur).serveur.clients.keys():
                inst.client = type(self.importeur).serveur.clients[ \
                        inst.client.n_id]
                self.instances[inst.client.n_id] = inst
        
        # On ajoute le dictionnaire 'instances' comme groupe fictif de 'parid'
        type(self.importeur).parid[NOM_GROUPE] = self.instances
        
        # On récupère les comptes
        comptes = self.importeur.supenr.charger_groupe(Compte)
        for compte in comptes:
            self.comptes[compte.id.id] = compte
            if not compte.valide:
                self.supprimer_compte(compte)
        
        # On affiche proprement le nombre de comptes (un peu verbeux mais-)
        nombre_comptes = len(self.comptes)
        if nombre_comptes == 0:
            self.cpt_logger.info("Aucun compte récupéré")
        elif nombre_comptes == 1:
            self.cpt_logger.info("1 compte récupéré")
        else:
            self.cpt_logger.info("{0} comptes récupérés".format(len(self.comptes)))
        
        # On ajoute les contextes chargés dans l'interpréteur
        for contexte in liste_contextes:
            self.importeur.interpreteur.contextes[contexte.nom] = contexte
        
        BaseModule.init(self)
    
    def boucle(self):
        """A chaque tour de boucle synchro, on envoie la file d'attente des
        instances de connexion.
        
        """
        for inst in self.instances.values():
            inst.envoyer_file_attente()
    
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
            raise KeyError("L'ID {0} ne se trouve pas dans les instances " \
                    "connectées".format(repr(client)))
        instance = self.instances[client]
        if instance.contexte_actuel:
            instance.contexte_actuel.deconnecter()
        
        del self.instances[client]
    
    def ajouter_compte(self, nom_compte):
        """Méthode appelée pour ajouter un compte identifié par son nom"""
        nouv_compte = Compte(nom_compte)
        self.cpt_logger.info("Création du compte {0}: {1}".format( \
                nom_compte, nouv_compte))
        self.comptes[nouv_compte.id.id] = nouv_compte
        return nouv_compte
    
    def supprimer_compte(self, compte):
        """Supprime le compte 'compte'"""
        if compte.id.id in self.comptes.keys():
            self.cpt_logger.info("Suppression du compte {0}: {1}".format( \
                    compte.nom, compte))
            del self.comptes[compte.id.id]
            compte.detruire()
        else:
            raise KeyError("Le compte {0} n'est pas dans la liste " \
                    "des comptes existants".format(compte))
    
    def get_compte(self, nom):
        """Récupère le compte 'compte'"""
        for compte in self.comptes.values():
            if compte.nom==nom:
                return compte
        return None
    
    def _get_email_comptes(self):
        """Retourne sous la forme d'un tuple la liste des emails de comptes
        créés ou en cours de création.
        
        """
        emails = []
        for compte in self.comptes.values():
            emails.append(compte.adresse_email)
        
        return tuple(emails)
    
    email_comptes = property(_get_email_comptes)
    
    def _get_nom_comptes(self):
        """Retourne sous la forme d'un tuple la liste des noms de comptes
        créés ou en cours de création.
        
        """
        noms = []
        for compte in self.comptes.values():
            noms.append(compte.nom)
        
        return tuple(noms)
    
    nom_comptes = property(_get_nom_comptes)
    
    def _get_nom_joueurs(self):
        """Retourne sous la forme d'un tuple la liste des noms de joueurs
        créés ou en cours de création.
        
        """
        noms = []
        for compte in self.comptes.values():
            for joueur in compte.joueurs.values():
                noms.append(joueur.nom)
        
        return tuple(noms)
    
    nom_joueurs = property(_get_nom_joueurs)

    def compte_est_cree(self, nom_compte):
        """Return True si le compte est créé, False sinon.
        
        """
        return nom_compte in self.nom_comptes

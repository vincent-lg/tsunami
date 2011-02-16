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


"""Fichier contenant le module secondaire stat."""

import time

from abstraits.module import *
from bases.fonction import *
from .stats import Stats
import secondaires.stat.commandes

class Module(BaseModule):
    
    """Module de statistique, appelé pour faire des stats sur le MUD,
    surveiller le Watch Dog, le temps d'interprétation des commandes et
    alerter en cas de problème.
    
    Pour ce faire, il redéfinit certaines fonctions de callback. Il garde de
    côté les anciennes et au moment de son déchargement, il les replace dans
    le serveur.
    
    """
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "stat", "secondaire")
        self.callbacks = {}
        self.stats = None
    
    def init(self):
        """Initialisation du module"""
        # on récupère les fonctions de callback du serveur
        serveur = self.importeur.serveur
        
        # On les sauvegarde dans le module
        self.callbacks = dict(serveur.callbacks)
        
        # à présent, on remplace certaines callbacks par de nouvelles
        reception = serveur.callbacks["reception"]
        serveur.callbacks["reception"] = Fonction(
                self.cb_reception, *reception.args, **reception.kwargs)
        
        # On récupère les informations statistiques
        sous_rep = "stats"
        fichier = "stats.sav"
        if self.importeur.supenr.fichier_existe(sous_rep, fichier):
            self.stats = self.importeur.supenr.charger(sous_rep, fichier)
        if self.stats is None or self.stats.uptime != \
                type(self.importeur).serveur.uptime:
            self.stats = Stats(type(self.importeur).serveur.uptime)
        
        # On ajoute les commandes du module
        # On ajoute les commandes du module
        self.commandes = [
            commandes.stat.CmdStat(),
        ]
        
        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)
    
    def detruire(self):
        """Destruction du module"""
        type(self.importeur).serveur.callbacks = self.callbacks
    
    def cb_reception(self, serveur, importeur, logger, client, msg):
        """Callback appelée quand on réceptionne un message"""
        en_hotboot = type(self.importeur).en_hotboot
        masquer = client.masquer
        avant = time.time()
        self.callbacks["reception"].executer(client, msg)
        apres = time.time()
        diff = apres - avant
        if en_hotboot == type(self.importeur).en_hotboot:
            if self.stats.nb_commandes == 0:
                self.stats.tps_moy_commandes = diff
            else:
                self.stats.tps_moy_commandes = \
                (self.stats.tps_moy_commandes * self.stats.nb_commandes + \
                diff) / (self.stats.nb_commandes + 1)
            self.stats.nb_commandes += 1
        
        if not masquer:
            print("Exécution de", msg, "en", diff, "sec")

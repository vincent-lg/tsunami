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


"""Ce fichier contient le code principal du projet.

Vous pouvez le renommer en fonction du nom choisi de votre projet.

"""

import signal
import sys

from reseau.connexions.serveur import *
from reseau.fonctions.callbacks import *
from bases.importeur import Importeur
from bases.parser_cmd import ParserCMD
from bases.anaconf import anaconf
from bases.logs import man_logs
from bases.parid import parid
from corps.config import pere

# Définition de la fonction appelée quand on arrête le MUD avec CTRL + C
# Le lancement du MUD se trouve sous la fonction
def arreter_mud(signal, frame):
    """Fonction appelée pour arrêter le MUD proprement"""
    global importeur, log
    importeur.tout_detruire()
    importeur.tout_arreter()
    log.info("Fin de la session\n\n\n")
    sys.exit(0)

# On relie cette fonction avec la levée de signal SIGINT et SIGTERM
signal.signal(signal.SIGINT, arreter_mud)
signal.signal(signal.SIGTERM, arreter_mud)

## Configuration du projet et lancement du MUD
# On crée un analyseur de la ligne de commande
parser_cmd = ParserCMD()
parser_cmd.interpreter()

# On configure anaconf
anaconf.config(parser_cmd)

# On charge la configuration globale du projet
config_globale = anaconf.get_config("globale", "kassie.cfg", \
        "modèle global", pere)

# On configure man_logs
man_logs.config(anaconf, parser_cmd)

# On se crée un logger
log = man_logs.creer_logger("", "sup", "kassie.log")

# On prend comme base le port présent dans le fichier de configuration
port = config_globale.port

# Si le port est spécifié dans la ligne de commande, on le change
# Utiliser un port différent précisé dans la ligne de commande a surtout
# été mis en place pour créer de multiples sessions de test du MUD
if "port" in parser_cmd.keys():
    port = parser_cmd["port"]

# Vous pouvez changer les paramètres du serveur, tels que spécifiés dans
# le constructeur de ServeurConnexion (voir reseau/connexions/serveur.py)
# La plupart des informations se trouve dans la configuration globale
serveur = ConnexionServeur(port, config_globale.nb_clients_attente, \
        config_globale.nb_max_connectes)

# On crée l'importeur, gérant les différents modules (primaires et secondaires)
importeur = Importeur(parser_cmd, anaconf, man_logs, parid, serveur)

# On lance le processus d'instanciation des modules
importeur.tout_charger()
importeur.tout_instancier()

# On configure et initialise les modules
importeur.tout_configurer()
importeur.tout_initialiser()

# Initialisation du serveur
serveur.init() # le socket serveur se met en écoute
log.info("Le serveur est à présent en écoute sur le port {0}".format(port))

# Configuration des fonctions de callback
# Note: si vous souhaitez modifier le comportement en cas de connexion
# au serveur, déconnexion ou réception d'un message client,
# modifiez directement les fonctions de callback dans :
# reseau/fonctions/callbacks.py

# Fonction de callback appelée lors de la connexion d'un client
serveur.callbacks["connexion"].fonction = cb_connexion
serveur.callbacks["connexion"].args = (serveur, importeur, log)

# Fonction de callback appelée lors de la déconnexion d'un client
serveur.callbacks["deconnexion"].fonction = cb_deconnexion
serveur.callbacks["deconnexion"].args = (serveur, importeur, log)

# Fonction de callback appelée lors de la réception d'un message d'un client
serveur.callbacks["reception"].fonction = cb_reception
serveur.callbacks["reception"].args = (serveur, importeur, log)

# Lancement de la boucle synchro
# Note: tout se déroule ici, dans une boucle temps réelle qui se répète
# jusqu'à l'arrêt du MUD. De cette manière, on garde le contrôle total
# sur le flux d'instructions.

while True:
    importeur.boucle()
    serveur.verifier_connexions()
    serveur.verifier_receptions()

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


"""Ce fichier contient la classe Log, détaillée plus bas.

Il permet d'instancier un objet de cette classe, appelée man_logs
(gestionnaire des loggers). Cet objet sera importé par le corps et les modules
qui ont beson de logger certaines choses. Depuis cette classe, on peut créer
un logger avec certains paramètres. Ce logger peut ensuite être utilisé pour
enregistrer des messages propres à une fonciton, un module, une action du
corps...

Mode d'emplois :
*   Commencez par importer man_logs (objet pour manipuler les loggers)
    >>> from bases.log import man_logs
*   Si c'est la première fois que man_logs est appelé, il doit être configuré
    (c'est logiquement le fichier principal, à la racine du projet, qui se charge
    de cette tâche)
    >>> man_logs.config(anaconf, parser_cmd)
    Note: anaconf est l'objet gérant a configuration du projet. parser_cmd
    est le parser de la ligne de commande (certaines options utiles aux logs
    peuvent y être spécifiées)
*   Vous pouvez ensuite créer un logger grâce à la méthode creer_logger
    >>> logger = man_logs.creer_logger(
    ...         sous_rep, nom_logger, nom_fichier)
    Note:
    -   sous_rep est le sous-répertoire menant au logger. On parle de sous-
        répertoire car il se construit à la suite de REP_LOGS, le chemin
        à donner ici est donc l'arborescence interne des fichiers de logs
        Par exemple : 'diffact/erreurs'
        Le répertoire 'erreurs' sera construit dans le dossier 'diffact',
        lui-même construit dans le dossier REP_LOGS .
    -   le nom du logger : il identifie de façon unique un logger. SI le nom
        du fichier n'est pas précisé, il sert comme base
        Evitez de donner un nom peu explicite tel que 'erreurs', cela
        pourrait entraîner des conflits.
        Si ce logger est chargé des erreurs du module 'diffact', donner un nom
        comme 'diffact:erreurs' par exemple
    -   le nom de fichier (facultatif quoique préférable)
        Lui donner de préférence l'extension .log

NOTE IMPORTANTE: on peut créer des loggers avant que man_logs ne soit
configuré. Toutefois, étant donné que man_logs ne sait pas encore où
enregistrer les fichiers de log, il les stock en mémoire en attendant
d'être configuré. Les messages sont affiché en console sans délai mais ils ne
seront écrit en fichier qu'après la configuration de man_logs.

"""

import os
import time

from bases.logs.logger import *

# Dossier d'enregistrement des fichiers de log
# Vous pouvez changer  directement cette variable, ou bien la modifier
# dans les fichiers de configuration, ou encore la passer en argument
# de la ligne de commande
REP_LOGS = os.path.expanduser("~") + os.sep + "kassie" + os.sep + "logs"

class ManLogs:
    """Cette classe permet d'enregistrer et gérer les fichiers de log.
    
    Chaque module primaire ou secondaire ayant besoin de logger des
    informations (c'est-à-dire la majorité sinon la totalité)
    devra passer par cette classe.
    
    On conserve une trace des loggers créés.

    """
    def __init__(self):
        """Constructeur du manager"""
        self.loggers = {} # {nom_logger:logger}
    
    def config(self, anaconf, parser_cmd):
        """Configuration du manager"""
        global REP_LOGS
        config_globale = anaconf.get_config("globale")
        # Si le chemin est précisé dans la configuration globale
        if config_globale.chemin_logs:
            REP_LOGS = config_globale.chemin_logs
        
        # Si le chemin est précisé en argument de la ligne de commande
        if "chemin-logs" in parser_cmd.keys():
            REP_LOGS = self.parser_cmd["chemin-logs"]
        
        # On construit le répertoire si il n'existe pas
        if not os.path.exists(REP_LOGS):
            os.makedirs(REP_LOGS)
        
        # Tous les loggers créés avant la configuration du manager
        # doivent être configurés également. On leur donne le répertoire
        # d'enregistrement des logs et on leur demande de s'enregistrer
        # dans des fichiers
        for logger in self.loggers.values():
            Logger.en_fil = False
            logger.rep_base = REP_LOGS
            logger.verif_rep()
            logger.enregistrer_fil_attente()
    
    def creer_logger(self, sous_rep, nom_logger, nom_fichier=""):
        """Retourne un nouveau logger.
        Si le nom de fichier n'est pas spécifié, on s'appuie sur le nom
        du logger .log.
        On se base dans tous les cas sur rep_base lié au sous_rep pour
        créer l'architecture d'enregistrement des logs.

        """
        global REP_LOGS
        if nom_fichier == "":
            nom_fichier = "{0}.log".format(nom_logger)

        logger = Logger(REP_LOGS, sous_rep, nom_fichier, nom_logger)
        self.loggers[nom_logger] = logger
        return logger

# On crée le 'man_logs' (gestionnaire des loggers)
# Cet objet sera celui directement manipulé par le corps ou les modules
# souhaitant logger des informations (c'est-à-dire une majorité)
# Aucun autre objet de la classe ManLogs n'a besoin d'être créé
man_logs = ManLogs()

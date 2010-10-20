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


"""Ce fichier contient la classe Log, définissant le module primaire
du même nom.

"""

import os
import time

from abstraits.module import *
from primaires.log.logger import *

# Dossier d'enregistrement des fichiers de log
# Vous pouvez changer cette variable, ou bien spécifier l'option en
# ligne de commande
REP_LOGS = os.path.expanduser("~") + os.sep + "kassie" + os.sep + "logs"

class Log(Module):
    """Classe du module 'log'.
    
    Ce module permet d'enregistrer et gérer les fichiers de log.
    
    Chaque module primaire ou secondaire ayant besoin de logger des
    informations (c'est-à-dire la majorité sinon la totalité)
    devra passer par ce module.
    
    On conserve une trace des loggers créés.

    NOTE IMPORTANTE: ce module ne pourra pas travailler avant d'être
    initialisé. Si des messages de log doivent être envoyés avant
    l'initialisation, ils seront mis dans une fil d'attente et enregistrés
    lors de l'initialisation.
    
    Voir primaires/log/logger.py
    
    """
    def __init__(self, importeur, parser_cmd):
        """Constructeur du module"""
        Module.__init__(self, importeur, parser_cmd, "log", "primaire")
        self.loggers = {} # {nom_logger:logger}

    def config(self):
        """Méthode de configuration. On se base sur
        parser_cmd pour savoir si un dossier d'enregistrement
        des fichiers de log a été défini.
        
        """
        global REP_LOGS
        if "chemin-logs" in self.parser_cmd.keys():
            REP_LOGS = self.parser_cmd["chemin-logs"]
        
        # On construit le répertoire si il n'existe pas
        if not os.path.exists(REP_LOGS):
            os.makedirs(REP_LOGS)
        
        # On met à jour le rep_base de chaque logger
        for logger in self.loggers.values():
            logger.rep_base = REP_LOGS
            logger.verif_rep()

        Module.config(self)

    def init(self):
        """Redéfinition de l'initialisation.
        On va passer le statut de tous les loggers pour qu'ils puissent
        écrire en temps réel leur message. On va aussi leur demander
        d'enregistrer toute leur fil d'attente.
        
        """
        for logger in self.loggers.values():
            logger.en_fil = False
            logger.verif_rep()
            logger.enregistrer_fil_attente()
        
        Module.init(self)

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
        if self.statut == INITIALISE:
            logger.en_fil = False
            logger.verif_rep()
        self.loggers[nom_logger] = logger
        return logger

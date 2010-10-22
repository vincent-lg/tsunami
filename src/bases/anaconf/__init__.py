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


"""Ce fichier contient la classe Anaconf, un analyseur de fichier
de configurations.

"""

import os

from bases.anaconf.analyseur import Analyseur

# Dossier d'enregistrement des fichiers de configuration
# Vous pouvez changer cette variable, ou bien spécifier l'option en
# ligne de commande
REP_CONFIG = os.path.expanduser("~") + os.sep + "kassie" + os.sep + "config"

class Anaconf:
    """Cette classe gère la lecture, l'écriture et l'interprétation de fichiers
    de configuration.
    
    Chaque module primaire ou secondaire ayant besoin d'enregistrer des
    informations de configuration devra passer par anaconf.
    C'est également vrai pour les informations du corps
    (configuration générale).
    
    """
    def __init__(self, importeur, parser_cmd):
        """Constructeur du module"""
        global REP_CONFIG
        self.parser_cmd = parser_cmd
        self.importeur = importeur
        self.configs = {}
        
        if "chemin-configuration" in self.parser_cmd.keys():
            REP_CONFIG = self.parser_cmd["chemin-configuration"]
        
        # On construit le répertoire si il n'existe pas
        if not os.path.exists(REP_CONFIG):
            os.makedirs(REP_CONFIG)
        
    def get_config(self, nom_id, chemin="", nom_defaut="", defaut=""):
        """Cette méthode permet de charger une configuration contenue dans
        le fichier passé en paramètre.
        Si le fichier a déjà été chargé, on retourne l'analyseur correspondant.
        Le paramètre 'nom_id' sert d'identifiant pour les configurations déjà
        chargées.
        Le paramètre 'defauts' est une chaîne écrite comme un fichier
        de configuration, analysé comme tel et contenant les données par
        défaut.
        Si certaines données ne sont pas trouvées, on les met à jour grâce
        à ce paramètre et on met à jour le fichier de configuration.
        
        """
        global REP_CONFIG
        chemin = REP_CONFIG + os.sep + chemin
        if not nom_id in self.configs.keys():
            # On construit l'analyseur
            # Cela revient à charger le fichier de configuration
            # ATTENTION : si le chemin est laissé vide, on lève une exception
            if chemin == "":
                raise RuntimeError("le chargement de l'analyseur {0} " \
                        "a échoué. Aucun chemin passé en paramètre".format( \
                        nom_id))
            logger = self.importeur.log.creer_logger("anaconf", nom_id)
           # On construit le répertoire si il n'existe pas
            rep = os.path.split(chemin)[0]
            if not os.path.exists(rep):
                os.makedirs(rep)
            # On l'ajoute aux configurations chargées
            self.configs[nom_id] = Analyseur(chemin, \
                    nom_defaut, defaut, logger)
        
        # On retourne l'analyseur
        return self.configs[nom_id]


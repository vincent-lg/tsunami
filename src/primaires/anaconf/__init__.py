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


"""Ce fichier contient la classe Anaconf, définissant le module primaire
du même nom.

"""

import os

from abstraits.module import *
from primaires.anaconf.analyseur import Analyseur

# Dossier d'enregistrement des fichiers de configuration
# Vous pouvez changer cette variable, ou bien spécifier l'option en
# ligne de commande
REP_CONFIG = os.path.expanduser("~") + os.sep + "kassie" + os.sep + "config"

class Anaconf(Module):
    """Classe du module 'anaconf'.
    
    Ce module gère la lecture, l'écriture et l'interprétation de fichiers de
    configuration.
    
    Chaque module primaire ou secondaire ayant besoin d'enregistrer des
    informations de configuration devra passer par anaconf.
    
    """
    def __init__(self, importeur, parser_cmd):
        """Constructeur du module"""
        Module.__init__(self, importeur, parser_cmd, "anaconf", "primaire")

    def config(self):
        """Méthode de configuration. On se base sur
        parser_cmd pour savoir si un dossier d'enregistrement
        des fichiers de configuration a été défini.
        
        """
        global REP_CONFIG
        if "chemin-configuration" in self.parser_cmd.keys():
            REP_CONFIG = self.parser_cmd["chemin-configuration"]
        
        # On construit le répertoire si il n'existe pas
        if not os.path.exists(REP_CONFIG):
            os.makedirs(REP_CONFIG)
        
        Module.config(self)

    def charger_config(self, chemin, defauts):
        """Cette méthode permet de charger une configuration contenue dans
        le fichier passé en paramètre. Le paramètre defauts est un
        dictionnaire contenant les données par défaut.
        Si certaines données ne sont pas trouvées, on les met à jour grâce
        à ce dictionnaire.
        
        """
        global REP_CONFIG
        chemin = REP_CONFIG + os.sep + chemin
        # On construit le répertoire si il n'existe pas
        rep = os.path.split(chemin)[0]
        if not os.path.exists(rep):
            os.makedirs(rep)
        return Analyseur(chemin, defauts)


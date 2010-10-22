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


"""Ce fichier contient la classe Supenr, définissant le module primaire
du même nom.

"""

import os

from abstraits.module import *

# Dossier d'enregistrement des fichiers-données
# Vous pouvez changer cette variable, ou bien spécifier l'option en
# ligne de commande
REP_ENRS = os.path.expanduser("~") + os.sep + "kassie" + os.sep + "enregistrements"

class Supenr(Module):
    """Classe du module 'supenr'.
    
    Ce module gère l'enregistrement des données et leur récupération.
    
    """
    def __init__(self, importeur, parser_cmd):
        """Constructeur du module"""
        Module.__init__(self, importeur, parser_cmd, "supenr", "primaire")
    
    def config(self):
        """Méthode de configuration. On se base sur
        parser_cmd pour savoir si un dossier d'enregistrement
        des fichiers-données a été défini.
        
        """
        global REP_ENRS
        config_globale = self.anaconf.get_config("globale")
        if config_globale.chemin_enregistrement:
            REP_ENRS = config_globale.chemin_enregistrement
        
        if "chemin-enregistrement" in self.parser_cmd.keys():
            REP_ENRS = self.parser_cmd["chemin-enregistrement"]
        
        # On construit le répertoire si il n'existe pas
        if not os.path.exists(REP_ENRS):
            os.makedirs(REP_ENRS)
        
        Module.config(self)

    def init(self):
        """Redéfinition de l'initialisation.
        
        """
        Module.init(self)


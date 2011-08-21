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


"""Fichier contenant le module primaire meteo."""

from abstraits.module import *
from .config import cfg_meteo
from .perturbations.base import BasePertu

class Module(BaseModule):
    
    """Cette classe représente le module primaire meteo.
    
    Comme son nom l'indique, ce module gère la météorologie dans l'univers.
    La météo est régie par un ensemble de perturbations se déplaçant
    de façon semi-aléatoire dans l'univers. Ces perturbations sont décrites
    dans le dossier correspondant ; une partie de leur comportement
    est configurable.
    
    """
    
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "meteo", "primaire")
        self._perturbations = {}
    
    def config(self):
        """Configuration du module"""
        type(self.importeur).anaconf.get_config("config_meteo",
            "meteo/config.cfg", "config meteo", cfg_meteo)
        
        BaseModule.config(self)
    
    def init(self):
        """Initialisation du module"""
        self.importeur.hook["salle:meteo"].ajouter_evenement(
                self.donner_meteo)
        
        BaseModule.init(self)
    
    def donner_meteo(self, salle, liste_messages):
        """Affichage de la météo d'une salle"""
        pass

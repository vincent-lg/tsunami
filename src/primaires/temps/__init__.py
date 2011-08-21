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


"""Fichier contenant le module primaire temps."""

from abstraits.module import *
from .config import cfg_temps
from .temps import Temps
from . import commandes

class Module(BaseModule):
    
    """Cette classe contient les informations du module primaire temps.
    Ce module gère le temps, son écoulement et sa mesure. Une configuration
    complète de ce module permet de savoir :
    -   quelles sont les unités de temps (années, saisons, mois...)
    -   à quelle vitesse s'écoule le temps
    
    """
    
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "temps", "primaire")
        self.cfg = None
    
    def config(self):
        """Méthode de configuration du module"""
        self.cfg = type(self.importeur).anaconf.get_config("temps",
            "temps/temps.cfg", "config temps", cfg_temps)
        
        BaseModule.config(self)
    
    def init(self):
        """Initialisation du module"""
        # On récupère ou crée le temps
        temps = None
        sous_rep = "temps"
        fichier = "temps.sav"
        if self.importeur.supenr.fichier_existe(sous_rep, fichier):
            temps = self.importeur.supenr.charger(sous_rep, fichier)
        if temps is None:
            temps = Temps(self.cfg)
        self.importeur.hook["salle:meteo"].ajouter_evenement(
                self.voir_ciel)
        
        self.temps = temps
        BaseModule.init(self)
    
    def ajouter_commandes(self):
        """Ajout des commandes dans l'interpréteur"""
        self.commandes = [
            commandes.temps.CmdTemps(),
        ]
        
        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)
    
    def preparer(self):
        """Préparation du module."""
        self.inc()
    
    def inc(self):
        """Incrémentation du temps."""
        self.importeur.diffact.ajouter_action("inc_temps",
                1, self.inc)
        self.temps.inc()
    
    def voir_ciel(self, salle, liste_messages):
        liste_messages.append(self.temps.ciel_actuel)

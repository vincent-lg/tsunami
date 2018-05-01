# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 AYDIN Ali-Kémal
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
# ARE DISCLAIMED. IN NO evenement SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""Fichier contenant le module secondaire 'calendrier'."""

import datetime

from abstraits.module import *
from primaires.format.fonctions import format_nb
from . import commandes
from . import masques
from . import editeurs
from .evenement import Evenement

class Module(BaseModule):

    """Module secondaire définissant le calendrier.
    
    Ce module définit les évenements.
    
    """
    
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "calendrier", "secondaire")
        self.commandes = []
        self.evenements = {}
        self.logger = type(self.importeur).man_logs.creer_logger( \
                "calendrier", "calendrier")
                
    def init(self):
        """Initialisation du module"""
        evenements = self.importeur.supenr.charger_groupe(Evenement)
        
        if self.evenements:
            Evenement.id_actuel = max(self.evenements.keys()) + 1
        
        for evenement in evenements:
            self.evenements[evenement.id] = evenement
        
        self.logger.info(format_nb(len(self.evenements),
               "{nb} évènement{s} récupéré{s}", fem = False))
                
        BaseModule.init(self)
        
    def ajouter_commandes(self):
        """Ajouts des commandes dans l'interpréteur"""
        self.commandes = [commandes.calendrier.CmdCalendrier()]
        
        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)
        
        importeur.interpreteur.ajouter_editeur(editeurs.evedit.EdtEvedit)
       
    def creer_evenement(self, createur):
        """Crée un évènement"""
        evenement = Evenement(createur)
        self.ajouter_evenement(evenement)
        return evenement
    
    def ajouter_evenement(self, evenement):
        """Ajoute un évènement au dictionnaire."""
        self.evenements[evenement.id] = evenement
    
    def supprimer_evenement(self, id):
        """Supprime un évènement"""
        self.evenements[id].detruire()
        del self.evenements[id]

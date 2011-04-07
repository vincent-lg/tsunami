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


"""Fichier contenant le module primaire communication."""

from abstraits.module import *
from primaires.communication import commandes
from primaires.communication.config import cfg_com
from .canal import Canal
from .canaux import Canaux

class Module(BaseModule):
    
    """Cette classe représente le module qui gère toutes les communications
    entre clients (donc entre joueurs la plupart du temps)
    Elle gère également les canaux de communication.
    
    """
    
    def __init__(self, importeur):
        BaseModule.__init__(self, importeur, "communication", "primaire")
        self.commandes = []
        self.correspondants = []
        self._canaux = canaux
    
    def config(self):
        """Configuration du module.
        On crée le fichier de configuration afin de l'utiliser plus tard
        pour la mise en forme.
        
        """
        type(self.importeur).anaconf.get_config("config_com", \
            "communication/config.cfg", "config communication", cfg_com)
        
        BaseModule.config(self)
    
    def ajouter_masques(self):
        """Ajout des masques"""
        # self.importeur.interpreteur.ajouter_masque(
        #        masques.direction.Direction)
    
    def ajouter_commandes(self):
        """Ajout des commandes"""
        self.commandes = [
            commandes.dire.CmdDire(),
            commandes.hrp.CmdHrp(),
            commandes.emote.CmdEmote(),
            commandes.parler.CmdParler(),
        ]
        
        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)
    
    @property
    def canaux(self):
        """Retourne les canaux existants"""
        return dict(self._canaux)
    
    def ajouter_canal(self, nom):
        """Ajoute un canal à la lsite des canaux existants
        Retourne le canal créé.
        
        """
        canal = Canal(nom)
        self._canaux[nom] = canal
        return canal
    
    def supprimer_canal(self, nom):
        """Supprime le canal de la liste des canaux"""
        del self._canaux[nom]

# -*-coding:Utf-8 -*

# Copyright (c) 2010 DAVY Guillaume
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


"""Fichier contenant le module secondaire jeux."""

from abstraits.module import *
from . import commandes
from . import masques
from . import types
from .config import cfg_jeux

class Module(BaseModule):
    
    """
    Module gérant les jeux dans le jeu
    
    """
    
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "jeux", "secondaire")
        
        self.logger = type(self.importeur).man_logs.creer_logger( \
                "jeux", "jeux")
        
        self.jeux = []
        
        self.parties = {}
    
    def config(self):
        """Configuration du module.
        On crée le fichier de configuration afin de l'utiliser plus tard
        dans les contextes.
        
        """
        type(self.importeur).anaconf.get_config("jeux", \
            "jeux/jeux.cfg", "modele jeux", cfg_jeux)
        
        BaseModule.config(self)
    
    def init(self):
        
        BaseModule.init(self)
        
        jeux_cfg = type(self.importeur).anaconf.get_config("jeux")
        
        for nom_jeu in jeux_cfg.jeux:
            package = __import__("secondaires.jeux.backend." + nom_jeu)
            jeu = getattr(getattr(getattr(getattr(package, "jeux"),"backend"),nom_jeu),nom_jeu)
            self.jeux.append(jeu)
    
    def get_jeu(self, nom):
        for jeu in self.jeux:
            if jeu.nom == nom:
                return jeu
        return None
    
    def get_partie(self, objet):
        if not objet.id.id in self.parties:
            self.parties[objet.id.id] = self.get_jeu(objet.jeu)()
        return self.parties[objet.id.id]
    
    def ajouter_masques(self):
        self.importeur.interpreteur.ajouter_masque(
                masques.objet.ObjetJeu)
                
    def ajouter_commandes(self):
        self.commandes = [
            commandes.jouer.CmdJouer()
        ]
        
        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)
    

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


"""Fichier contenant le module primaire perso."""

from abstraits.module import *
from secondaires.bugtracker import commandes
from secondaires.bugtracker.editeurs.rapporteur import EdtRapporteur
from . import masques
from .conteneur_bugs import ConteneurBugs

class Module(BaseModule):
    
    """
    Module gérant les bugs, leur ajouts, leur modification ...
    
    """
    
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "bugtracker", "secondaire")
        
        self.logger = type(self.importeur).man_logs.creer_logger( \
                "bugs", "bugs")
        
        self.bugs = None
    
    def init(self):
        
        sous_rep = "bugs"
        fichier = "bugs.sav"
        
        bugs = None
        
        if self.importeur.supenr.fichier_existe(sous_rep, fichier):
            bugs = self.importeur.supenr.charger(sous_rep, fichier)
        if bugs is None:
            bugs = ConteneurBugs()
            self.logger.info("Aucun bug récupéré")
        else:
            s = ""
            if len(bugs) > 1:
                s = "s"
            self.logger.info("{} groupe{s} d'utilisateurs récupéré{s}".format(
                        len(bugs), s = s))
        
        self.bugs = bugs
        
        self.importeur.interpreteur.ajouter_masque(
                masques.ident.Ident)
                
        self.commandes = [
            commandes.rapport.CmdRapport(),
        ]
        
        self.importeur.interpreteur.ajouter_editeur(EdtRapporteur)
        
        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)
    

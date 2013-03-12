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


"""Fichier contenant le module secondaire 'magie'."""

from abstraits.module import *
from primaires.format.fonctions import *
from secondaires.magie import commandes
from secondaires.magie import masques
from secondaires.magie import types
from .editeurs.spedit import EdtSpedit
from .sorts import Sorts

class Module(BaseModule):
    
    """Ce module gère la magie en jeu, et tout ce qui s'y rattache.
    
    """
    
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "magie", "secondaire")
        self.logger = type(self.importeur).man_logs.creer_logger( \
                "magie", "magie")
        self.sorts = None
        self.commandes = []
    
    def init(self):
        """Initialisation du module"""
        # On récupère les sorts
        sorts = self.importeur.supenr.charger_unique(Sorts)
        if sorts is None:
            sorts = Sorts()
        else:
            self.logger.info(format_nb(len(sorts), "{nb} sort{s} récupéré{s}"))
        self.sorts = sorts
        
        # Ajout des commandes
        self.commandes = [
            commandes.lancer.CmdLancer(),
            #commandes.oublier.CmdOublier(),
            commandes.sorts.CmdSorts(),
        ]
        
        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)
        
        # Ajout de l'éditeur de sorts
        self.importeur.interpreteur.ajouter_editeur(EdtSpedit)
        
        # Ajout du niveau magie
        self.importeur.perso.ajouter_niveau("magie", "mysticisme")
        
        # Ajout des talents magiques
        ajouter_talent = self.importeur.perso.ajouter_talent
        ajouter_talent("destruction", "destruction", "magie", 0.20)
        ajouter_talent("alteration", "altération", "magie", 0.25)
        ajouter_talent("invocation", "invocation", "magie", 0.20)
        ajouter_talent("illusion", "illusion", "magie", 0.30)
        
        # Ajout de l'état
        etat = self.importeur.perso.ajouter_etat("magie")
        etat.msg_refus = "Vous êtes en train de lancer un sort."
        etat.msg_visible = "se concentre ici"
        
        BaseModule.init(self)
    
    def supprimer_sort(self, cle):
        """Supprime le sort spécifié"""
        sort = self.sorts[cle]
        del self.sorts[cle]

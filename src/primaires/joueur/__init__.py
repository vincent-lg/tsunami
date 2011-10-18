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


"""Fichier contenant le module primaire joueur."""

from abstraits.module import *
from primaires.joueur import commandes
from primaires.joueur import masques
from primaires.joueur.config import cfg_joueur
from .joueur import Joueur
from . import contextes

class Module(BaseModule):
    """Classe utilisée pour gérer des joueurs, c'est-à-dire des personnages
    connecté par client, à distinguer des PNJ.
    
    Les mécanismes de jeu propres aux personnages, c'est-à-dire communs aux
    joueurs et PNJ, ne sont pas défini dans ce module mais dans le module
    primaire 'perso'.
    
    """
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "joueur", "primaire")
        self.commandes = []
        self.groupe_par_defaut = "joueur"
        self.joueurs = {}
        self.compte_systeme = ""
        self.joueur_systeme = ""
    
    def config(self):
        """Méthode de configuration du module"""
        config = type(self.importeur).anaconf.get_config("joueur",
            "joueur/joueur.cfg", "config joueur", cfg_joueur)
        self.groupe_par_defaut = config.groupe_par_defaut
        self.compte_systeme = config.compte_systeme
        self.joueur_systeme = config.joueur_systeme
        # On crée les hooks du module
        self.importeur.hook.ajouter_hook("joueur:connecte",
                "Hook appelé après qu'un joueur se soit connecté.")
        
        BaseModule.config(self)
    
    def init(self):
        """Méthode d'initialisation du module"""
        joueurs = self.importeur.supenr.charger_groupe(Joueur)
        for joueur in joueurs:
            self.joueurs[joueur.nom] = joueur
        
        BaseModule.init(self)
    
    def ajouter_commandes(self):
        """Ajout des commandes dans l'interpréteur"""
        self.commandes = [
            commandes.afk.CmdAfk(),
            commandes.chgroupe.CmdChgroupe(),
            commandes.groupe.CmdGroupe(),
            commandes.distinction.CmdDistinction(),
            commandes.module.CmdModule(),
            commandes.options.CmdOptions(),
            commandes.pset.CmdPset(),
            commandes.quitter.CmdQuitter(),
            commandes.quitter.CmdQuitter(),
            commandes.restaurer.CmdRestaurer(),
            commandes.retenir_nom.CmdRetenir_nom(),
            commandes.shutdown.CmdShutdown(),
            commandes.where.CmdWhere(),
        ]
        
        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)
    
    def preparer(self):
        """Préparation du module.
        On s'assure que :
        -   les joueurs dits connectés le soient toujours
        
        """
        for joueur in self.importeur.connex.joueurs:
            i_c = joueur.instance_connexion
            if joueur.est_connecte() and (i_c is None or not i_c.est_connecte()):
                joueur.pre_deconnecter()
        
        # On vérifie que le groupe par défaut existe dans les groupes existants
        gen_logger = type(self.importeur).man_logs.get_logger("sup")
        groupe_par_defaut = "joueur"
        if self.groupe_par_defaut not in \
                self.importeur.interpreteur.groupes:
            gen_logger.warning("le groupe par défaut {} n'existe pas. " \
                    "Le groupe {} le remplace".format(self.groupe_par_defaut,
                    groupe_par_defaut))
            self.groupe_par_defaut = groupe_par_defaut
        
        # On charge ou crée le compte et joueur système
        if not self.importeur.connex.get_compte(self.compte_systeme):
            systeme = self.importeur.connex.ajouter_compte(self.compte_systeme)
            systeme.valide = True
        
        self.compte_systeme = self.importeur.connex.get_compte(
                self.compte_systeme)
        if self.joueur_systeme not in self.joueurs.keys():
            self.compte_systeme.creer_joueur(self.joueur_systeme)
        
        self.joueur_systeme = self.joueurs[self.joueur_systeme]

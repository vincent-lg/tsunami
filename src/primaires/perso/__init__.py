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


"""Fichier contenant le module primaire perso."""

from abstraits.module import *

from . import commandes
from . import masques
from .editeurs.skedit import EdtSkedit
from .editeurs.raedit import EdtRaedit
from .cfg_stats import cfg_stats
from .race import Race
from .stats import *
from .squelette import Squelette

class Module(BaseModule):
    
    """Module gérant la classe Personnage qui sera héritée pour construire
    des joueurs et PNJ. Les mécanismes propres au personnage (c'est-à-dire
    indépendant de la connexion et liées à l'univers) seront gérées ici.
    
    En revanche, les contextes de connexion ou de création d'un personnage
    ne se trouve pas ici (il s'agit d'informations propres à un joueur, non
    à un PNJ.
    
    """
    
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "perso", "primaire")
        self.cfg_stats = None
        self.commandes = []
        self.squelettes = {}
        self.races = []
    
    def config(self):
        """Méthode de configuration.
        On récupère le fichier de configuration correspondant au module.
        
        """
        self.cfg_stats = conf_stats = type(self.importeur).anaconf.get_config(
                "stats", "perso/stats.cfg", "modele stats", cfg_stats)
        conf_stats._set_globales({
            "I0":I0,
            "IE0":IE0,
            "SM":SM,
            "SEM":SEM,
        })
        
        BaseModule.config(self)
    
    def init(self):
        """Initialisation du module"""
        # On récupère les squelettes
        squelettes = self.importeur.supenr.charger_groupe(Squelette)
        for squelette in squelettes:
            self.ajouter_squelette(squelette)
        
        # On récupère les races
        races = self.importeur.supenr.charger_groupe(Race)
        for race in races:
            self.ajouter_race(race)
        
        BaseModule.init(self)
    
    def ajouter_commandes(self):
        """Ajout des commandes dans l'interpréteur"""
        self.commandes = [
            commandes.commande.CmdCommande(),
            commandes.equipement.CmdEquipement(),
            commandes.qui.CmdQui(),
            commandes.raedit.CmdRaedit(),
            commandes.score.CmdScore(),
            commandes.skedit.CmdSkedit(),
        ]
        
        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)
        
        # Ajout de l'éditeur 'skedit'
        self.importeur.interpreteur.ajouter_editeur(EdtRaedit)
        self.importeur.interpreteur.ajouter_editeur(EdtSkedit)
    
    def creer_squelette(self, cle):
        """Création d'un squelette"""
        squelette = Squelette(cle)
        self.ajouter_squelette(squelette)
        return squelette
    
    def ajouter_squelette(self, squelette):
        """Ajoute le squelette aux squelettes existants"""
        self.squelettes[squelette.cle] = squelette
    
    def supprimer_squelette(self, cle):
        """Supprime le squelette existant"""
        squelette = self.squelettes[cle]
        del self.squelettes[cle]
        squelette.detruire()
    
    def creer_race(self, nom):
        """Crée la race du nom indiqué"""
        race = Race(nom)
        self.ajouter_race(race)
        return race
    
    def ajouter_race(self, race):
        """Ajout de la race au dictionnaire des races existantes"""
        self.races.append(race)
    
    def supprimer_race(self, nom):
        """Suppression de la race 'nom'"""
        race = None
        indice = None
        for i, t_race in enumerate(self.races):
            if race.nom.lower() == nom.lower():
                race = t_race
                indice = i
        
        del self.races[indice]
        race.detruire()


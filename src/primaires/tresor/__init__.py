# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Ce fichier contient le module primaire tresor."""

from collections import namedtuple

from abstraits.module import *
from primaires.format.fonctions import aff_flottant
from . import commandes
from .config import cfg_tresor
from .tresor import Tresor

# constantes
t_stats = namedtuple("Tresor", ["argent_total", "argent_joueurs",
        "joueur_max", "valeur_max", "fluctuation", "nb_jours_fluctuation",
        "pc_joueurs_total", "pc_joueur_max_total"])

class Module(BaseModule):
    
    """Classe représentant le module 'tresor'.
    
    Ce module conserve des informations sur le marché financier du MUD.
    Il définit notamment certaines commandes pour consulter et modifier
    le trésor global (l'argent en jeu) et l'argent de chacun. Notez que
    ce module est un module primaire : d'autres informations peuvent être
    contenues dans d'autres modules.
    
    """
    
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "tresor", "primaire")
    
    def config(self):
        """Méthode de configuration.
        
        On récupère le fichier de configuration correspondant au module.
        
        """
        self.cfg = type(self.importeur).anaconf.get_config("tresor", \
                "tresor/monnaie.cfg", "modele tresor", cfg_tresor)
        
        BaseModule.config(self)
    
    def init(self):
        """Initialisation du module"""
        self.tresor = self.importeur.supenr.charger_unique(Tresor)
        if self.tresor is None:
            self.tresor = Tresor()
        
        BaseModule.init(self)
    
    def ajouter_commandes(self):
        """Ajoute les commandes à l'interpréteur."""
        self.commandes = [
            commandes.tresor.CmdTresor(),
        ]
        
        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)
    
    def preparer(self):
        """Préparation du module."""
        self.tresor.mettre_a_jour()
    
    def aff_montant(self, montant):
        """Retourne le montant arrondi si nécessaire."""
        if montant >= 1000000000000:
            montant = str(round(montant, -12))
            montant = montant[-12] + "T"
        elif montant >= 1000000000:
            montant = str(round(montant, -9))
            montant = montant[-9] + "G"
        elif montant >= 1000000:
            montant = str(round(montant, -6))
            montant = montant[-6] + "M"
        elif montant >= 1000:
            montant = str(round(montant, -3))
            montant = montant[-3] + "K"
        else:
            montant = str(montant)
        
        unite = self.cfg.unite
        return montant + unite
    
    def get_stats(self):
        """Retourne les stats dans un namedtuple exploitable."""
        stats = self.tresor
        nb_jours_fluctuation = self.cfg.nb_jours_fluctuation
        argent_total = self.aff_montant(stats.argent_total)
        argent_joueurs = self.aff_montant(stats.argent_joueurs)
        joueur_max = stats.joueur_max and stats.joueur_max.nom or "inconnu"
        valeur_max = self.aff_montant(stats.valeur_max)
        pc_joueurs_total = aff_flottant(stats.pc_joueurs_total)
        pc_joueur_max_total = aff_flottant(stats.pc_joueur_max_total)
        pc_fluctuation = aff_flottant(stats.pc_fluctuation)
        return t_stats(
                argent_total=argent_total,
                argent_joueurs=argent_joueurs,
                joueur_max=joueur_max,
                valeur_max=valeur_max,
                fluctuation=pc_fluctuation,
                nb_jours_fluctuation=str(nb_jours_fluctuation),
                pc_joueurs_total=pc_joueurs_total,
                pc_joueur_max_total=pc_joueur_max_total,
        )

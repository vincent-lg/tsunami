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


"""Fichier contenant le module secondaire napeche."""

from abstraits.module import *
from corps.fonctions import valider_cle
from .banc import Banc

class Module(BaseModule):
    
    """Module secondaire définissant la pêche."""
    
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "peche", "secondaire")
        self.commandes = []
        self.bancs = {}
    
    def config(self):
        """Configuration du module."""
        pecher = self.importeur.perso.ajouter_etat("pecher")
        pecher.msg_refus = "Vous êtes en train de pêcher"
        pecher.msg_visible = "{personnage} pêche ici"
        
        BaseModule.config(self)
    
    def init(self):
        """Chargement des bancs de poisson."""
        importeur.perso.ajouter_talent("peche_terre", "pêche à quai",
                "survie", 0.45)
        importeur.perso.ajouter_talent("peche_mer", "pêche embarquée",
                "survie", 0.42)
        
        bancs = self.importeur.supenr.charger_groupe(Banc)
        for banc in bancs:
            self.bancs[banc.cle] = banc
        
        importeur.diffact.ajouter_action("bancs", 60,
                self.tick_bancs)
        
        BaseModule.init(self)
    
    def ajouter_commandes(self):
        """Ajout des commandes dans l'interpréteur"""
        self.commandes = [
        ]
        
        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)
    
    def creer_banc(self, cle):
        """Crée un banc de poisson et l'ajoute dans le dictionnaire.
        
        Retourne le banc créé.
        
        Lève une exception KeyError si le banc existe déjà.
        
        """
        valider_cle(cle)
        if cle in self.bancs:
            raise KeyError("le banc de poisson '{}' existe déjà".format(cle))
        
        banc = Banc(cle)
        self.ajouter_banc(banc)
        return banc
    
    def ajouter_banc(self, banc):
        """Ajoute le banc de poisson dans le dictionnaire."""
        self.bancs[banc.cle] = banc
    
    def supprimer_banc(self, cle):
        """Supprime le banc de poisson portant la clé passée en paramètre."""
        if cle not in self.bancs:
            raise KeyError("le banc de poisson '{}' est inconnue".format(
                    cle))
        
        banc = self.bancs[cle]
        del self.bancs[cle]
        banc.detruire()
    
    def tick_bancs(self):
        """Tick les bancs."""
        importeur.diffact.ajouter_action("bancs", 60,
                self.tick_bancs)
        for banc in self.bancs.values():
            banc.tick()

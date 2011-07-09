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


"""Fichier contenant le module primaire pnj."""

from abstraits.module import *
from .prototype import Prototype
from .pnj import PNJ
from . import commandes
from . import masques
from .editeurs.pedit import EdtPedit

class Module(BaseModule):
    
    """Cette classe contient les informations du module primaire pnj.
    Comme son nom l'indique, ce module gère les PNJ de l'univers,
    personnages non joueurs, hérités de Personnage mais distincts des
    joueurs dans le sens où ils sont animés par l'univers et non par
    des joueurs connectés.
    
    Ce module gère également les prototypes de PNJ. Plusieurs PNJ peuvent
    être modelés sur le même prototype (être du même nom, de la même race,
    avoir le même équipement, par exemple deux gardes d'une Cité).
    
    """
    
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "pnj", "primaire")
        self._PNJ = {}
        self._prototypes = {}
    
    def init(self):
        """Initialisation du module"""
        prototypes = self.importeur.supenr.charger_groupe(Prototype)
        for prototype in prototypes:
            self._prototypes[prototype.cle] = prototype
        
        pnjs = self.importeur.supenr.charger_groupe(PNJ)
        for pnj in pnjs:
            self._PNJ[pnj.identifiant] = pnj
        
        BaseModule.init(self)
    
    def ajouter_commandes(self):
        """Ajout des commandes dans l'interpréteur"""
        self.commandes = [
            commandes.pedit.CmdPedit(),
            commandes.plist.CmdPlist(),
            commandes.ppurge.CmdPpurge(),
            commandes.pspawn.CmdPspawn(),
        ]
        
        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)
        
        # Ajout de l'éditeur 'redit'
        self.importeur.interpreteur.ajouter_editeur(EdtPedit)
    
    @property
    def PNJ(self):
        """Retourne un dictionnaire déréférencé des PNJ."""
        return dict(self._PNJ)
    
    @property
    def prototypes(self):
        """Retourne un dictionnaire déréférencé des prototypes."""
        return dict(self._prototypes)
    
    def creer_prototype(self, cle):
        """Crée un prototype et l'ajoute aux prototypes existants"""
        if cle in self._prototypes:
            raise ValueError("la clé {} est déjà utilisée comme " \
                    "prototype".format(cle))
        
        prototype = Prototype(cle)
        self.ajouter_prototype(prototype)
        return prototype
    
    def ajouter_prototype(self, prototype):
        """Ajoute un prototype au dictionnaire des prototypes"""
        if prototype.cle in self._prototypes:
            raise ValueError("la clé {} est déjà utilisée comme " \
                    "prototype".format(prototype.cle))
        
        self._prototypes[prototype.cle] = prototype
    
    def supprimer_prototype(self, cle):
        """Supprime le prototype cle"""
        prototype = self._prototypes[cle]
        del self._prototypes[cle]
        prototype.detruire()
    
    def creer_PNJ(self, prototype):
        """Crée un PNJ depuis le prototype prototype.
        Le PNJ est ensuite ajouté à la liste des PNJ existants.
        
        """
        pnj = PNJ(prototype)
        self.ajouter_PNJ(pnj)
        return pnj
    
    def ajouter_PNJ(self, pnj):
        """Ajoute le PNJ à la liste des PNJ"""
        if pnj.identifiant in self._PNJ:
            raise ValueError("l'identifiant {} est déjà utilisé comme " \
                    "PNJ".format(pnj.identifiant))
        
        self._PNJ[pnj.identifiant] = pnj
    
    def supprimer_PNJ(self, identifiant):
        """Supprime le PNJ de la liste des PNJ."""
        pnj = self._PNJ[identifiant]
        del self._PNJ[identifiant]
        pnj.detruire()

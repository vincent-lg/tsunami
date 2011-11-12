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


"""Fichier contenant le module secondaire navigation."""

from abstraits.module import *
from .navire import Navire
from corps.fonctions import valider_cle
from primaires.format.fonctions import format_nb
from .modele import ModeleNavire

class Module(BaseModule):
    
    """Module secondaire définissant la navigation.
    
    Ce module définit les navires, modèles de navires et objets liés.
    
    """
    
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "navigation", "secondaire")
        self.modeles = {}
        self.navires = {}
        self.nav_logger = type(self.importeur).man_logs.creer_logger(
                "navigation", "navires", "navires.log")
    
    def init(self):
        """Chargement des navires et modèles."""
        # On récupère les modèles
        modeles = self.importeur.supenr.charger_groupe(ModeleNavire)
        for modele in modeles:
            self.modeles[modele.cle] = modele
        
        nb_modeles = len(modeles)
        self.nav_logger.info(format_nb(nb_modeles,
                "{nb} modèle{s} de navire récupéré{s}"))
        
        # On récupère les navires
        navires = self.importeur.supenr.charger_groupe(Navire)
        for navire in navires:
            self.navires[navire.cle] = navire
        
        nb_navires = len(navires)
        self.nav_logger.info(format_nb(nb_navires,
                "{nb} navire{s} récupéré{s}"))
        
        BaseModule.init(self)
    
    def creer_modele(self, cle):
        """Crée un modèle de navire et l'ajoute dans le dictionnaire.
        
        Retourne le modèle créé.
        
        Lève une exception KeyError si le modèle existe déjà.
        
        """
        valider_cle(cle)
        if cle in self.modeles:
            raise KeyError("le modèle de navire {} existe déjà".format(cle))
        
        modele = ModeleNavire(cle)
        self.ajouter_modele(modele)
        return modele
    
    def ajouter_modele(self, modele):
        """Ajoute le modèle de navire dans le dictionnaire."""
        self.modeles[modele.cle] = modele
    
    def supprimer_modele(self, cle):
        """Supprime le modèle de navire portant la clé passée en paramètre."""
        if cle not in self.modeles:
            raise KeyError("le modèle de navire de clé {} est inconnue".format(
                    cle))
        
        modele = self.modeles[cle]
        del self.modeles[cle]
        modele.detruire()
    
    def creer_navire(self, modele):
        """Crée un navire sur le modèle.
        
        Retourne le navire créé.
        
        """
        navire = Navire(modele)
        print("Navire {} créé".format(navire.cle))
        self.ajouter_navire(navire)
        return navire
    
    def ajouter_navire(self, navire):
        """Ajoute le navire à la liste."""
        self.navires[navire.cle] = navire
    
    def supprimer_navire(self, cle):
        """Supprime le navire dont la clé est passée en paramètre."""
        if cle not in self.navires:
            raise KeyError("le navire de clé {} est introuvable".format(cle))
        
        navire = self.navires[cle]
        navire.detruire()
        del self.navires[cle]

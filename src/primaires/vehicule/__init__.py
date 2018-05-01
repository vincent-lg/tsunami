# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 DAVY Guillaume
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


"""Fichier contenant le module primaire vehicule"""

from abstraits.module import *
from .vehicule import Vehicule
from .vecteur import Vecteur

import time

# Nombre de seconde virtuelle qui s'écoule en une seconde
VIRTSEC = 1

class Module(BaseModule):
    
    """Classe utilisée pour gérer des véhicules.
    
    """
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "vehicule", "primaire")
        self.commandes = []
        
        self.vehicules = []
        
        self.temps_precedant = time.time()
        
        self.map = {}
    
    def ajouter_vehicule(self, vehicule):
        self.vehicules.append(vehicule)
    
    def boucle(self):
        """A chaque tour de boucle synchro, on fait avancer les vehicules
        
        """
        seconde_virtuelle = (time.time() - self.temps_precedant) * VIRTSEC
        
        self.map = {}
        for vehicule in self.vehicules:
            masque = vehicule.get_prochaine_coordonnees(seconde_virtuelle)
            impact = [x for x in masque if x in self.map]
            if len(impact):
                vehicule.collision(impact)
            vehicule.avancer(seconde_virtuelle)
            for coords in masque:
                self.map[coords] = vehicule
        self.temps_precedant = time.time()

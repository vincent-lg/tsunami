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


"""Fichier contenant le module primaire salle."""

from abstraits.module import *
from .salle import Salle

class Module(BaseModule):
    """Classe utilisée poru gérer des salles.
    Dans la terminologie des MUDs, les salles sont des "cases" avec une
    description et une liste de sorties possibles, que le joueur peut
    emprunter. L'ensemble des salles consiste l'univers, auquel il faut
    naturellement rajouté des NPCs et objets pour qu'il soit riche un minimum.
    
    Pour plus d'informations, consultez le fichier
    src/primaires/salle/salle.py contenant la classe Salle.
    
    """
    
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "salle", "primaire")
        self._salles = {} # ident:salle
        self.logger = type(self.importeur).man_logs.creer_logger( \
                "salles", "salles")
    
    def init(self):
        """Méthode d'initialisation du module"""
        # On récupère les salles
        salles = self.importeur.supenr.charger_groupe(Salle)
        
        s = ""
        if len(salles) > 1:
            s = "s"
        
        ###DEBUG
        if len(salles) == 0:
            self.ajouter_salle("picte", "1")
        
        self.logger.info("{} salle{s} récupérée{s}".format(len(salles), s=s))
        
        BaseModule.init(self)
    
    def ajouter_salle(self, zone, mnemo, x=0, y=0, z=0, valide=True):
        """Permet d'ajouter une salle"""
        salle = Salle(zone, mnemo)
        salle.coords.x = x
        salle.coords.y = y
        salle.coords.z = z
        salle.coords.valide = valide
        self._salles[salle.ident] = salle
        print(self._salles)
        return salle

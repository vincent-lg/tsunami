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


"""Fichier contenant le contexte controler."""

from primaires.joueur.contextes.connexion.mode_connecte import ModeConnecte
from primaires.pnj.instance_controler import InstanceControler

class Controler(ModeConnecte):
    
    """Contexte permettant de contrôler un PNJ.
    
    Par défaut, le PNJ contrôlé est dans le mode connecté statique.
    
    """
    
    nom = ""
    def __init__(self, joueur, pnj):
        instance_connexion = None
        if joueur and pnj:
            instance_connexion = InstanceControler(joueur, pnj)
        
        ModeConnecte.__init__(self, instance_connexion)
        self.s_pere = instance_connexion
        self.joueur = joueur
        self.pnj = pnj
        if pnj:
            pnj.instance_connexion = instance_connexion
    
    def __getnewargs__(self):
        return (None, None)
    
    def _get_unom(self):
        return "ctrl_pnj(" + self.pnj.identifiant + ")"
    
    def _set_unom(self, nom):
        pass
    unom = property(_get_unom, _set_unom)
    
    def _get_pere(self):
        return self.s_pere
    def _set_pere(self, pere):
        pass
    pere = property(_get_pere, _set_pere)
    
    def opt_quitter(self):
        """Quitte le contexte."""
        if self.pnj:
            self.pnj.decontroller()
        if self.joueur:
            self.joueur << "Vous quittez le contrôle du PNJ {}.".format(
                    self.pnj.identifiant)
    
    def interpreter(self, msg):
        """Méthode d'interprétation du contexte"""
        if msg.startswith("/"):
            msg = msg[1:].lower()
            if msg == "q":
                self.opt_quitter()
            else:
                self.pere << "|err|Option inconnue.|ff|"
        else:
            ModeConnecte.interpreter(self, msg)

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


"""Fichier contenant le contexte éditeur EdtCouleur"""

from primaires.interpreteur.editeur.uniligne import Uniligne
from primaires.format.constantes import COULEURS

class EdtCouleur(Uniligne):
    
    """Classe définissant le contexte éditeur 'couleur'.
    Ce contexte permet d'éditer la couleur d'un canal.
    
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Uniligne.__init__(self, pere, objet, attribut)
    
    def accueil(self):
        """Message d'accueil du contexte"""
        canal = self.objet
        msg = self.aide_courte
        msg += "Couleurs disponibles : "
        for nom, clr in COULEURS.items():
            msg += clr + nom + "|ff|, "
            if nom == "blanc": # on insère un saut de ligne à l'arrache
                msg += "\n"
        msg = msg[0:-2] + "."
        msg += "\nCouleur actuelle : " + canal.clr + canal.clr_nom + "|ff|"
        return msg
    
    def interpreter(self, msg):
        """Interprétation du message"""
        msg = msg.lower()
        if not msg in COULEURS:
            self.pere.envoyer("|err|Cette couleur n'existe pas.|ff|")
        else:
            self.objet.clr = COULEURS[msg]
            self.actualiser()

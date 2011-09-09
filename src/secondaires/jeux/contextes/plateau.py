# -*-coding:Utf-8 -*

# Copyright (c) 2010 DAVY Guillaume
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


"""Fichier contenant le contexte 'jeux:plateau'"""

from primaires.format.constantes import ponctuations_finales

from primaires.interpreteur.contexte import Contexte

class Plateau(Contexte):
    
    """Contexte dans lequel on peut jouer à un jeu.
    
    """
    
    def __init__(self, pere, objet, partie):
        """Constructeur du contexte"""
        Contexte.__init__(self, pere)
        self.objet = objet
        self.partie = partie
        self.personnage = None
        self.opts.prompt_prf = ""
        
        if self.pere:
            self.personnage = self.pere.joueur
    
    def __getnewargs__(self):
        return (None, None, None)
    
    def get_prompt(self):
        """Message de prompt."""
        return "-> "
    
    def accueil(self):
        """Message d'accueil du contexte."""
        msg = "Vous êtes en train de jouer à {} :\n".format(
                self.objet.nom_singulier)
        msg += "Tapez |cmd|/q|ff| pour quitter la partie.\n"
        msg += self.partie.afficher(self.personnage)
        return msg
    
    def interpreter(self, msg):
        """Interprétation du message."""
        if msg.startswith("/"):
            # C'est une option
            msg = msg[1:].lower()
            if hasattr(self.partie.jeu, "opt_" + msg):
                getattr(self.partie.jeu, "opt_" + msg)(self.personnage)
                if msg == "q":
                    self.personnage.contextes.retirer()
                    self.objet.partie.detruire()
            else:
                self.pere << "|err|Option invalide.|ff|"
        else:
            self.partie.jeu.jouer(self.personnage, msg)

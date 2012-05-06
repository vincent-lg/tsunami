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


"""Fichier contenant le contexte-éditeur EdtFils"""

from primaires.interpreteur.editeur.uniligne import Uniligne
from primaires.format.fonctions import supprimer_accents

class EdtFils(Uniligne):
    
    """Classe définissant le contexte-éditeur 'fils'.
    Ce contexte permet de hiérarchiser les sujets d'aide.
    
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur."""
        Uniligne.__init__(self, pere, objet, attribut)
        self.ajouter_option("u", self.opt_bouger_up)
        self.ajouter_option("d", self.opt_bouger_down)
    
    def opt_bouger_up(self, arguments):
        """Option permettant de bouger un sujet vers le haut de la liste.
        Syntaxe : /u <sujet>
        
        """
        sujet = self.objet
        cle_fils = arguments
        sujet_fils = importeur.information.sujets.get(cle_fils)
        if not sujet_fils or not sujet.est_fils(sujet_fils):
            self.pere << "|err|Le sujet {} n'est pas fils du sujet " \
                    "courant.|ff|".format(cle_fils)
            return
        try:
            sujet.echanger_fils(sujet_fils)
        except ValueError:
            self.pere << "|err|Le sujet est déjà en haut de la liste.|ff|"
            return
        self.actualiser()
    
    def opt_bouger_down(self, arguments):
        """Option permettant de bouger un sujet vers le bas de la liste.
        Syntaxe : /d <sujet>
        
        """
        sujet = self.objet
        cle_fils = arguments
        sujet_fils = importeur.information.sujets.get(cle_fils)
        if not sujet_fils or not sujet.est_fils(sujet_fils):
            self.pere << "|err|Le sujet {} n'est pas fils du sujet " \
                    "courant.|ff|".format(cle_fils)
            return
        try:
            sujet.echanger_fils(sujet_fils, bas=True)
        except ValueError:
            self.pere << "|err|Le sujet est déjà en bas de la liste.|ff|"
            return
        self.actualiser()
    
    def interpreter(self, msg):
        """Interprétation du message"""
        sujet = self.objet
        sujet_fils = importeur.information.sujets.get(msg)
        if not sujet_fils:
            self.pere << "|err|Le sujet '{}' n'existe pas.|ff|".format(msg)
        elif sujet_fils is sujet:
            self.pere << "|err|Vous ne pouvez affilier un sujet à " \
                    "lui-même.|ff|"
        elif sujet.est_lie(sujet_fils):
            self.pere << "|err|Le sujet '{}' est déjà lié au sujet " \
                    "courant.|ff|".format(msg)
        else:
            if sujet.est_fils(sujet_fils):
                sujet.supprimer_fils(sujet_fils)
            elif sujet_fils.pere is not None:
                self.pere << "|err|Le sujet '{}' est déjà affilié au " \
                        "sujet '{}'.|ff|".format(msg, sujet_fils.pere.cle)
            else:
                sujet.ajouter_fils(sujet_fils)
                self.actualiser()

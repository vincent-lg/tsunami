# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 LE GOFF Vincent
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


"""Fichier contenant le contexte 'communication:invitation'"""

from primaires.interpreteur.contexte import Contexte

class Invitation(Contexte):
    
    """Contexte d'invitation.
    
    """
    
    def __init__(self, pere):
        """Constructeur du contexte"""
        Contexte.__init__(self, pere)
        self.opts.prompt_prf = ""
        self.opts.prompt_clr = ""
        self.emetteur = None
        self.canal = None
    
    def get_prompt(self):
        return ">"
    
    def accueil(self):
        """Message d'accueil du contexte"""
        res = "\n|vrc|" + self.emetteur.nom + " vous invite à rejoindre le " \
            "canal " + str(self.canal) + ".\nEntrez |ff||ent|o|ff||vrc| si " \
            "vous acceptez, |ff||ent|n|ff||vrc| dans le cas contraire.|ff|"
        return res
    
    def interpreter(self, msg):
        """Méthode d'interprétation du contexte"""
        joueur = self.pere.joueur
        msg = msg.lower()
        if msg == "o":
            # On tente de connecter joueur
            self.canal.rejoindre_ou_quitter(joueur, forcer=True)
            self.fermer()
        elif msg == "n":
            joueur << "|att|Vous avez refusé l'invitation.|ff|"
            self.fermer()
        else:
            joueur << "|err|Vous devez accepter ou refuser.|ff|"

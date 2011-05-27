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


"""Package contenant la commande 'afk'"""

from primaires.interpreteur.commande.commande import Commande
from primaires.format.fonctions import couper_phrase

class CmdAfk(Commande):
    
    """Commande 'afk'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "afk", "afk")
        self.groupe = "joueur"
        self.schema = "(<message>)"
        self.aide_courte = "passe AFK"
        self.aide_longue = \
            "Cette commande permet de passer AFK (Away From Keyboard). " \
            "Vous signalez ainsi aux autres joueurs que vous êtes absent " \
            "pour le moment ; la raison de cette absence, si spécifiée en " \
            "argument, sera affichée dans la liste de la commande %qui%. " \
            "Lorsque vous revenez, utilisez à nouveau la commande sans " \
            "argument pour revenir à l'état normal."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        if dic_masques["message"] is not None:
            message = dic_masques["message"].message
            if len(message) > 20:
                message = couper_phrase(message, 20)
            personnage << "Vous passez AFK ({}).".format(message)
            personnage.afk = message
        else:
            if not personnage.afk:
                personnage << "Vous passez AFK."
                personnage.afk = "afk"
            else:
                personnage << "Vous n'êtes plus AFK."
                personnage.afk = ""

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


"""Ce fichier contient la classe Conversation détaillée plus bas."""

import datetime

from abstraits.obase import BaseObj
from primaires.format.fonctions import couper_phrase

class Conversation(BaseObj):

    """Cette classe contient deux joueurs en conversation.
    Elle est notamment utile au reply.
    
    """
    
    def __init__(self, emetteur, cible, phrase):
        """Constructeur de la classe"""
        self.emetteur = emetteur
        self.cible = cible
        self._phrase = phrase
        self.focus = False
        self.date = datetime.datetime.now()
        # On déduit l'id
        conversations = type(self).importeur.communication.conversations
        if emetteur:
            p_conversations = conversations.get_conversations_pour(emetteur)
        self.id = len(p_conversations) + 1
    
    def __getnewargs__(self):
        return (None, None, "")
    
    def _get_phrase(self):
        """Retourne la phrase mise en forme"""
        return couper_phrase(self._phrase, 40)
    
    def _set_phrase(self, phrase):
        """Stocke phrase dans self._phrase"""
        self._phrase = phrase
    
    phrase = property(_get_phrase, _set_phrase)
    
    def __str__(self):
        return "Conversation entre {} et {} : {}".format(self.emetteur.nom,
                self.cible.nom, self.phrase)
    
    def ch_focus(self):
        """Place le focus sur la conversation courante"""
        if self.focus:
            self.focus = False
        else:
            # On parcourt tous les correspondants pour redéfinir leur focus
            conversations = type(self).importeur.communication.conversations
            for conversation in conversations.iter():
                if self.emetteur is conversation.emetteur:
                    if conversation.focus:
                        conversation.focus = False
            self.focus = True

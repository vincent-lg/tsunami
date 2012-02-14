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


"""Ce fichier contient la classe Conversations détaillée plus bas."""

import datetime
from datetime import timedelta

from abstraits.obase import BaseObj
from .conversation import Conversation

class Conversations(BaseObj):

    """Classe conteneur des conversations en cours.
    Cette classe liste tous les items Conversation utilisables dans l'univers
    à un instant donné.
    
    Voir : ./conversation.py
    
    """
    
    enregistrer = True
    def __init__(self, parent=None):
        """Constructeur du conteneur"""
        BaseObj.__init__(self)
        self._conversations = []
    
    def __getnewargs__(self):
        return ()
    
    def iter(self):
        """Boucle sur les conversations contenues"""
        return list(self._conversations)
    
    def ajouter_ou_remplacer(self, emetteur, cible, phrase):
        """Ajoute ou actualise une conversation à la liste"""
        if emetteur is cible:
            raise ValueError("l'émetteur {} est identique à la " \
                    "cible".format(emetteur))
        
        if self.conversation_existe(emetteur, cible):
            cle = self.get_cle_conversation(emetteur, cible)
            self._conversations[cle].phrase = phrase
            self._conversations[cle].date = datetime.datetime.now()
            conversation = self._conversations[cle]
        else:
            conversation = Conversation(emetteur, cible, phrase)
            self._conversations.insert(0, conversation)
    
    def conversation_existe(self, emetteur, cible):
        """Renvoie True si la conversation existe, False sinon"""
        return self.get_cle_conversation(emetteur, cible) != -1
    
    def get_cle_conversation(self, emetteur, cible):
        """Renvoie la cle d'une conversation"""
        i = 0
        for conversation in self._conversations:
            if conversation.emetteur == emetteur and \
                    conversation.cible is cible:
                return i
            i += 1
        
        return -1
    
    def get_conversations_pour(self, personnage):
        """Récupère toutes les conversations impliquant 'personnage'"""
        conversations_pour = []
        for conversation in self._conversations:
            if personnage is conversation.emetteur:
                conversations_pour.append(conversation)
        
        return conversations_pour
    
    def vider_conversations_pour(self, personnage):
        """Vide les conversations impliquant 'personnage'"""
        for conversation in tuple(self._conversations):
            if personnage is conversation.emetteur or \
                    personnage is conversation.cible:
                auj = datetime.datetime.now()
                if auj - conversation.date > timedelta(hours=1):
                    self._conversations.remove(conversation)

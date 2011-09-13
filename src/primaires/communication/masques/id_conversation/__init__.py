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


"""Fichier contenant le masque <id_corresp>."""

from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation

class IdConversation(Masque):
    
    """Masque <id_conversation>.
    On attend le numéro d'une conversation (voir commande reply) en paramètre.
    
    """
    
    nom = "id_conversation"
    nom_complet = "ID d'une conversation"
    
    def init(self):
        """Initialisation des attributs du masque"""
        self.id_conversation = None
        self.cible = None
        self.perte_focus = False
    
    def repartir(self, personnage, masques, commande):
        """Répartition du masque."""
        id_conversation = liste_vers_chaine(commande)
        if not id_conversation:
            raise ErreurValidation( \
                "Vous devez préciser le numéro d'un correspondant.", False)
        
        id_conversation = id_conversation.split(" ")[0]
        if not id_conversation.isdigit() and not id_conversation == "-":
            raise ErreurValidation( \
                "L'ID {} n'est pas valide.".format(id_conversation), False)
        
        self.a_interpreter = id_conversation
        commande[:] = commande[len(id_conversation):]
        masques.append(self)
        return True
    
    def valider(self, personnage, dic_masques):
        """Validation du masque"""
        Masque.valider(self, personnage, dic_masques)
        id_conversation = self.a_interpreter
        conversations = type(self).importeur.communication.conversations
        p_conversations = conversations.get_conversations_pour(personnage)
        cible = None
        
        if id_conversation == "-":
            self.perte_focus = True
            return True
        
        try:
            id_conversation = int(id_conversation)
        except ValueError:
            return False
        
        if id_conversation < 1 or id_conversation > len(p_conversations):
            raise ErreurValidation(
                "|err|Le numéro spécifié ne correspond à aucun personnage.|ff|")
        
        try:
            cible = p_conversations[id_conversation - 1].cible
        except IndexError:
            raise ErreurValidation(
                "|err|Le numéro spécifié ne correspond à aucun personnage.|ff|")
        else:
            self.id_conversation = len(p_conversations) + 1 - id_conversation
            self.cible = cible
            return True

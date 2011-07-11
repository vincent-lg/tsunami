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


"""Ce fichier contient la classe BoiteMail détaillée plus bas."""

from abstraits.unique import Unique
from .mudmail import *

class BoiteMail(Unique):

    """Boîte mail du moteur.
    Cette classe contient tous les mudmails et permet d'interagir avec.
    
    Voir : ./mudmail.py
    
    """
    
    def __init__(self):
        """Constructeur du conteneur"""
        Unique.__init__(self, "communication", "mails")
        self._mails = {}
    
    def __getnewargs__(self):
        return ()
    
    def __len__(self):
        """Retourne le nombre de mails"""
        return len(self._mails)
    
    def __getitem__(self, id):
        """Récupère un mail à partir de son id"""
        return self._mails[id]
    
    def __setitem__(self, id, mail):
        """Modifie un mail"""
        self._mails[id] = mail
        self.enregistrer()
    
    def __delitem__(self, id):
        """Supprime un mail"""
        del self._mails[id]
        self.enregistrer()
    
    def creer_mail(self, expediteur):
        """Cree un message vide et le retourne"""
        mail = MUDmail(self, expediteur)
        self._mails[mail.id] = mail
        self.enregistrer()
        return mail.id
    
    def get_mails_pour(self, personnage, etat, exp=True):
        """Renvoie la liste des mails de personnage"""
        ret = []
        for mail in self._mails.values():
            if exp: # on récupère les mails dont perso est expediteur
                if mail.expediteur == personnage and mail.etat == etat:
                    ret.append(mail)
            else: # ou ceux dont il est destinataire
                if mail.destinataire == personnage and mail.etat == etat:
                    ret.append(mail)
        return ret

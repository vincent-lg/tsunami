# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
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

from abstraits.obase import BaseObj
from .mudmail import *

class BoiteMail(BaseObj):

    """Boîte mail du moteur.

    Cette classe contient tous les mudmails et permet d'interagir avec.

    Voir : ./mudmail.py

    """

    enregistrer = True
    def __init__(self):
        """Constructeur du conteneur"""
        BaseObj.__init__(self)
        self._mails = {}
        self._construire()

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

    def __delitem__(self, id):
        """Supprime un mail"""
        del self._mails[id]

    @property
    def id_suivant(self):
        """Retourne l'ID maximum enregistré + 1."""
        return max(self._mails.keys() or (0, )) + 1

    def creer_mail(self, expediteur, source=None):
        """Cree un message vide et le retourne"""
        mail = MUDmail(self, expediteur, source=source)
        mail.id = self.id_suivant
        self._mails[mail.id] = mail
        return mail

    def get_mails_pour(self, personnage, etat):
        """Renvoie la liste des mails de personnage"""
        ret = []
        for mail in self._mails.values():
            if etat == RECU or etat == ARCHIVE:
                if mail.destinataire == personnage and mail.etat == etat:
                    ret.append(mail)
            else:
                if mail.expediteur == personnage and mail.etat == etat:
                    ret.append(mail)
        return ret

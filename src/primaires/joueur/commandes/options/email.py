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


"""Fichier contenant le paramètre 'email' de la commande 'options'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmEmail(Parametre):

    """Commande 'options email'."""

    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "email", "email")
        self.tronquer = True
        self.schema = "<etat>"
        self.aide_courte = "active / désactive l'envoi d'e-mails"
        self.aide_longue = \
            "Cette commande permet d'activer ou désactiver l'envoi " \
            "d'e-mails à ce compte en cas de réception d'un UmdMail. " \
            "Si cette option est active, un e-mail sera envoyé lors " \
            "de l''envoi de MudMails, comme par exemple un commentaire de " \
            "rapport. Si cette option est inactive, les MudMails seront " \
            "toujours reçus par les joueurs du compte, mais un e-mail " \
            "de notification ne sera pas envoyé à la réception de MudMails. " \
            "Pour activer l'option, précisez en paramètre |ent|on|ff|. " \
            "Pour la désactiver, précisez |ent|off|ff| en paramètre."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre."""
        etat = dic_masques["etat"].flag
        if personnage.compte.email == etat:
            personnage << "|att|C'est déjà le cas.|ff|"
        else:
            personnage.compte.email = etat
            if etat:
                personnage << "Envoi d'e-mails activé."
            else:
                personnage << "Envoi d'e-mails désactivé."

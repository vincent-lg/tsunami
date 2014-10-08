# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Ce fichier contient la classe Newsletter, détaillée plus bas."""

from datetime import datetime

from abstraits.obase import BaseObj
from primaires.format.description import Description
from .constantes import *

class Newsletter(BaseObj):

    """Classe représentant une news letter avec ses statuts.

    Une news letter contient :
        sujet -- son sujet (sujet de l'e-mail envoyé)
        contenu -- le contenu de la NL (contenu de l'e-mail)
        statut -- le statut de la NL [1]

    Les méthodes utiles sont :
        envoyer -- envoie la NL à tous les comptes inscrits

    [1] Le statut de la NL est une chaîne contenant :
        * brouillon : la NL est encore en brouillon, donc éditable (par défaut)
        * envoyée : la NL a été envoyée

    """

    enregistrer = True
    def __init__(self, sujet):
        """Constructeur de la News Letter."""
        BaseObj.__init__(self)
        self.sujet = sujet
        self.contenu = Description(parent=self, scriptable=False)
        self.statut = "brouillon"
        self.editee = False
        self.date_creation = datetime.now()
        self.date_envoi = None
        self.nombre_envois = 0
        self._construire()

    def __getnewargs__(self):
        return ("aucun", )

    def __repr__(self):
        return "<news letter {}>".format(repr(self.sujet))

    @property
    def brouillon(self):
        return self.statut == "brouillon"

    @property
    def envoyee(self):
        return self.statut == "envoyée"

    def envoyer(self):
        """Envoi la News Letter aux comptes inscrits.

        Les comptes inscrits sont ceux ayant l'option 'newsletter' à True.

        """
        inscrits = [compte for compte in importeur.connex.comptes.values() if \
                compte.newsletter and compte.adresse_email and compte.ouvert]
        destinateur = "news"
        sujet = self.sujet
        contenu = str(self.contenu)
        nb = 0
        self.statut = "envoyée"
        self.date_envoi = datetime.now()
        if not importeur.email.serveur_mail:
            return 0

        for compte in inscrits:
            destinataire = compte.adresse_email
            corps = contenu + bas_page.format(nom_compte=compte.nom).rstrip()
            importeur.email.envoyer(destinateur, destinataire, sujet, corps)
            nb += 1

        self.nombre_envois = nb
        return nb

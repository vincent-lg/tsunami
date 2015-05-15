# -*-coding:Utf-8 -*

# Copyright (c) 2015 LE GOFF Vincent
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


"""Fichier contenant le module primaire evt."""

from abstraits.module import *
from primaires.evt import commandes
from primaires.evt.evenement import Evenement

class Module(BaseModule):

    """Cette classe représente le module primaireevt.

    Ce module gère les évènements. Un évènement est un hook lié à
    un message d'avertissement destiné aux immortels. Les immortels
    peuvent soient s'abonner soit se désabonner de certains
    évènements. Il y a par un exemple un évènement lié à la
    connexion ou déconnexion d'un joueur.

    """

    def __init__(self, importeur):
        """Constructeur du module."""
        BaseModule.__init__(self, importeur, "evt", "primaire")
        self.evenements = {}

    def init(self):
        """Initialisation du module."""
        evts = importeur.supenr.charger_groupe(Evenement)
        for evt in evts:
            self.evenements[evt.cle] = evt

        BaseModule.init(self)

    def ajouter_commandes(self):
        """Ajoute les commandes à l'interpréteur."""
        self.commandes = [
            commandes.evenement.CmdEvenement(),
        ]

        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)

    def ajouter_evenement(self, cle, aide, message, hook):
        """Ajoute un nouvel évènement.

        Paramètres à entrer :
            cle -- la clé (unique) de l'évènement
            aide -- le message d'aide de l'évèneemnt
            message -- le message à afficher
            hook -- l'hook auquel connecter l'évènement

        """
        cle = cle.lower()
        if cle in self.evenements:
            evt = self.evenements[cle]
            evt.aide = aide
            evt.message = message
            importeur.hook[hook].ajouter_evenement(evt.exc_hook)
            return

        evt = Evenement(cle, aide, message)
        self.evenements[cle] = evt
        importeur.hook[hook].ajouter_evenement(evt.exc_hook)

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


"""Fichier contenant le module primaire format."""

from abstraits.module import *
from primaires.format import commandes
from primaires.format.config import cfg_charte
from primaires.format.description_flottante import DescriptionFlottante
from primaires.format.editeurs.floatedit import EdtFloatedit
from primaires.format.message import Message

class Module(BaseModule):

    """Cette classe décrit le module primaire Format.

    Ce module est particulièrement chargé du formatage,
    notamment des messages à envoyer aux clients.

    """

    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "format", "primaire")

    def config(self):
        """Configuration du module.

        On crée le fichier de configuration afin de l'utiliser plus tard
        pour la mise en forme.

        """
        type(self.importeur).anaconf.get_config("charte_graph", \
            "format/charte.cfg", "modele charte graphique", cfg_charte)

        # Ajout des hooks
        importeur.hook.ajouter_hook("description:ajouter_variables",
                "Hook appelé pour ajouter des variables aux descriptions")

        BaseModule.config(self)
        self.descriptions_flottantes = {}

    def init(self):
        """Initialisation du module.

        On récupère les descriptions flottantes.

        """
        flottantes = self.importeur.supenr.charger_groupe(DescriptionFlottante)
        for flottante in flottantes:
            self.descriptions_flottantes[flottante.cle] = flottante

        BaseModule.init(self)

    def ajouter_commandes(self):
        """Ajout des commandes dans l'interpréteur"""
        self.commandes = [
            commandes.flottantes.CmdFlottantes(),
        ]

        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)

        # Ajout des éditeurs
        self.importeur.interpreteur.ajouter_editeur(EdtFloatedit)

    def formater(self, message):
        """Retourne le message formaté.

        Voir : primaires.format.message

        """
        nv_message = Message(message, \
                        type(self.importeur).anaconf.get_config("charte_graph"))
        return nv_message

    def creer_description_flottante(self, cle):
        """Crée une description flottante."""
        if cle in self.descriptions_flottantes:
            raise KeyError(cle)

        flottante = DescriptionFlottante(cle)
        self.descriptions_flottantes[cle] = flottante
        return flottante

    def supprimer_description_flottante(self, cle):
        """Supprime la description flottante indiquée."""
        if cle not in self.descriptions_flottantes:
            raise KeyError(cle)

        flottante = self.descriptions_flottantes.pop(cle)
        flottante.detruire()

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


"""Fichier contenant le module secondaire client.

Ce module est utilisé pour permettre la compatibilité avec
le client web et l'interprétation d'options clients.

"""

from abstraits.module import *

from secondaires.client.config import CFG_CLIENT

class Module(BaseModule):

    """Module utilisé pour interpréter les options du client web.

    Les options sont des commandes basiques commençant par le signe
    '#'. Seuls certains clients avec une IP précise doivent pouvoir
    les entrer. Voir la configuration pour plus d'informations.

    """

    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "client", "secondaire")
        self.adresses = []
        self.options = {
                "encoding": self.opt_encodage,
        }

    def config(self):
        """Méthode de configuration.

        On récupère le fichier de configuration correspondant au module.

        """
        cfg = importeur.anaconf.get_config("client",
                "client/client.cfg", "modele client", CFG_CLIENT)
        self.adresses = cfg.adresses_ip
        BaseModule.config(self)

    def init(self):
        """Chargement du module."""
        self.importeur.hook["connex:cmd"].ajouter_evenement(
                self.interpreter_option)

    def interpreter_option(self, instance_connexion, commande):
        """Traite les options du client Web."""
        if instance_connexion.adresse_ip in self.adresses and \
                commande.startswith("#"):
            commande = commande[1:]
            mot = commande.split(" ")[0].lower()
            reste = " ".join(commande.split(" ")[1:])
            if mot in self.options:
                methode = self.options[mot]
                methode(instance_connexion, reste)
                return True

    def opt_encodage(self, instance, encodage):
        """Modifie l'encodage du client."""
        client = instance.client
        client.encodage = encodage
        client.modifier_encodage = False

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


"""Package contenant la commande 'reboot'."""

from primaires.interpreteur.commande.commande import Commande
from primaires.information.commandes.reboot.ajouter import PrmAjouter
from primaires.information.commandes.reboot.programmer import PrmProgrammer
from primaires.information.commandes.reboot.supprimer import PrmSupprimer

class CmdReboot(Commande):

    """Commande 'reboot'."""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "reboot", "reboot")
        self.groupe = "administrateur"
        self.nom_categorie = "info"
        self.aide_courte = "cré un reboot programmé"
        self.aide_longue = \
            "Cette commande crée ou manipule un reboot programmé. " \
            "Un reboot programmé est utile pour arrêter le MUD à un " \
            "moment fixe, mais il permet aussi de publier des versions " \
            "en différé. Ainsi, il est possible de créer un reboot " \
            "différé, de décrire les modifications (les joueurs ne " \
            "pourront pas les voir à ce stade), de programmer le reboot " \
            "pour dans X minutes. Au redémarrage du MUD, les versions " \
            "du reboot seront intégrées au système de version : les " \
            "joueurs pourront donc les voir après reboot. Ces deux " \
            "fonctionnalités sont indépendantes : il vous est possible " \
            "de spécifier des versions différées, mais garder le " \
            "contrôle sur le moment du reboot. Ou bien, vous pouvez " \
            "programmer un reboot sans versions."

    def ajouter_parametres(self):
        """Ajout des paramètres"""
        self.ajouter_parametre(PrmAjouter())
        self.ajouter_parametre(PrmProgrammer())
        self.ajouter_parametre(PrmSupprimer())

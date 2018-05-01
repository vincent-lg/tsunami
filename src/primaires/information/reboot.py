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


"""Ce fichier contient la classe Reboot détaillée plus bas."""


class Reboot:

    """Classe représentant un reboot programmé.

    Un reboot programmé contient des informations qui seront mises
    en lignes au reboot, comme des versions. Cette classe est
    également responsable de programmer un redémarrage du MUD.

    """

    def __init__(self):
        self.actif = True
        self.versions = []
        self.temps = None

    def __repr__(self):
        return "<Reboot>"

    def programmer(self, temps):
        """Prépare un reboot pour dans X minutes IRL."""
        messages = {
                10: "Reboot imminent.",
                60: "Reboot dans une minute.",
                180: "Reboot dans trois minutes.",
                300: "Reboot dans cinq minutes.",
                600: "Reboot dans dix minutes.",
                1800: "Reboot dans une demie heure.",
                3600: "Reboot dans une heure.",
        }

        for secondes, message in sorted(messages.items(), reverse=True):
            if secondes <= temps:
                importeur.diffact.ajouter_action("reboot_{}".format(
                        secondes), temps - secondes, self.notifier, message)

        importeur.diffact.ajouter_action("reboot_mtn", temps, self.reboot)

    def notifier(self, message):
        """Envoie le message au canal 'info'."""
        if self.actif:
            try:
                canal = importeur.communication.canaux["info"]
            except KeyError:
                return
            else:
                canal.envoyer_imp(message)

    def reboot(self):
        """Fait rebooter le MUD si le reboot différé est actif."""
        if self.actif:
            type(importeur).serveur.lance = False

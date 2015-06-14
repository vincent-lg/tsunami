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


"""Ce fichier contient la classe Evenement détaillée plus bas."""

from abstraits.obase import *
from primaires.joueur.joueur import Joueur

class Evenement(BaseObj):

    """Classe définissant un évènement.

    Un évènement est la liaison entre un hook et un message
    envoyé aux immortels inscrits à l'évènement. La méthode 'exc_hook'
    est reliée à l'hook.

    """

    enregistrer = True

    def __init__(self, cle, aide, message):
        """Constructeur de la classe."""
        BaseObj.__init__(self)
        self.cle = cle
        self.aide = aide
        self.message = message
        self.inscrits = []
        self._construire()

    def __getnewargs__(self):
        return ("", "", "")

    def exc_hook(self, *args, **kwargs):
        """Méthode générique appelé pour gérer l'évènement."""
        message = self.message.format(*args, **kwargs)

        # Envoie le message aux immortels inscrits
        for connecte in importeur.connex.joueurs_connectes:
            if connecte.est_immortel() and connecte in self.inscrits:
                connecte.sans_prompt()
                connecte.envoyer("|bl|_-_|ff| " + message)

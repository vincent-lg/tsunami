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


"""Fichier contenant la classe ConsoleInteractive détaillée plus bas."""

from code import InteractiveConsole
import sys
import traceback

class ConsoleInteractive:

    """Classe représentant une console interactive.

    Dans cette console peut être entrée du code Python. Si Kassie est
    lancé avec l'option -i (--interactif), à chaque tour de boucle
    l'utilisateur pourra entrer du code Python et voir le résultat affiché
    à l'écran.

    Cette console est utile si le réseau est inactif sur la machine (ou
    inopérant) et que vous souhaitez tester Kassie malgré tout.

    """

    def __init__(self, importeur):
        """Constructeur."""
        self.espace = {
            "importeur": importeur,
            "fermer": self.fermer,
        }
        self.console = InteractiveConsole(self.espace)
        self.prompt = ">>> "
        self.ouverte = True

    def fermer(self):
        """Ferme la console."""
        self.ouverte = False

    def boucle(self):
        """A chaque tour de boucle."""
        if self.ouverte:
            try:
                code = input(self.prompt)
            except (KeyboardInterrupt, EOFError):
                importeur.serveur.lance = False
                return

            try:
                ret = self.console.push(code)
            except Exception:
                print(traceback.format_exc())
            else:
                self.prompt = "... " if ret else ">>> "


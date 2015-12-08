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

from code import InteractiveConsole, InteractiveInterpreter
import sys
import time
import traceback
from threading import Thread

class ConsoleInteractive:

    """Classe représentant une console interactive.

    Dans cette console peut être entrée du code Python. Si Kassie est
    lancée avec l'option -i (--interactif), à chaque tour de boucle
    l'utilisateur pourra entrer du code Python et voir le résultat affiché
    à l'écran. Ce mode n'est maintenant plus bloquant :
    l'utilisateur peut ne rien entrer pendant des heures, le MUD
    continuera à tourner. Cependant, le résultat des logs ne sera
    pas affiché dans ce contexte. Il appartiendra à l'utilisateur de
    regarder la console autrement (de faire un 'tail -f' sur un
    fichier de retour, par exemple).

    Cette console est utile si le réseau est inactif sur la machine (ou
    inopérant) et que vous souhaitez tester Kassie malgré tout.
    Elle est aussi très pratique pour des opérations de débuggage,
    correction de bugs ponctuels ou tests de certaines conditions.
    Elle doit cependant être utilisée avec autant de prudence que
    la commande 'systeme', car elle donne un accès complet à Python
    et l'univers.

    """

    def __init__(self, importeur):
        """Constructeur."""
        self.console = Console(type(importeur).espace)
        self.prompt = ">>> "

    def input(self):
        """Récupère l'input de l'utilisateur."""
        sys.__stdout__.write(self.prompt)
        sys.__stdout__.flush()
        try:
            code = input()
        except (KeyboardInterrupt, EOFError):
            importeur.serveur.lance = False
            return

        stdout = sys.stdout
        stderr = sys.stderr
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        try:
            ret = self.console.push(code)
        except Exception:
            print(traceback.format_exc())
        else:
            self.prompt = "... " if ret else ">>> "
        finally:
            sys.stdout = stdout
            sys.stderr = stderr


class ThreadConsole(Thread):

    """Support pour une console dans un thread différent."""

    def __init__(self, console):
        Thread.__init__(self)
        self.console = console

    def run(self):
        """Lance le thread."""
        while importeur.serveur.lance:
            if len(self.console.console.codes):
                time.sleep(0.02)
            else:
                self.console.input()

class Console(InteractiveConsole):

    """Exécute le code en différé."""

    def __init__(self, espace):
        InteractiveConsole.__init__(self, espace)
        self.codes = []

    def runcode(self, code):
        """Diffère l'exécution du code."""
        self.codes.append(code)

    def runcodes(self):
        """Exécute les codes en attente."""
        codes = list(self.codes)
        self.codes.clear()

        # Rétablit sus.stdout et sys.stderr
        stdout = sys.stdout
        stderr = sys.stderr
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        for code in codes:
            InteractiveInterpreter.runcode(self, code)

        sys.stdout = stdout
        sys.stderr = stderr

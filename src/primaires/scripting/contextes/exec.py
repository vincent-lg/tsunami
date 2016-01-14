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


"""Fichier contenant le contexte 'exec'"""

from code import InteractiveConsole
import sys
from textwrap import dedent
import traceback

from primaires.interpreteur.contexte import Contexte
from primaires.scripting.evenement import Evenement
from primaires.scripting.test import Test

class Exec(Contexte):

    """Contexte permettant d'entrer du scripting à la volée.

    Ce contexte fonctionne de façon similaire au contexte 'système',
    mais au lieu de permettre d'entrer du code Python, il permet
    d'entrer du code scripting. Le fonctionnement reste le même,
    cependant, et il peut s'avérer tout autant dangereux.

    """

    nom = "scripting:exec"

    def __init__(self, pere):
        """Constructeur du contexte"""
        Contexte.__init__(self, pere)
        self.opts.prompt_prf = ""
        self.opts.prompt_clr = ""
        self.opts.nl = False
        self.evenement = Evenement(None, "exec")
        self.test = Test(self.evenement)
        variables = self.test.get_globales(self.evenement)
        self.console = InteractiveConsole(variables)
        self.py_prompt = ">>> "

        if pere:
            variables = self.evenement.espaces.variables
            joueur = pere.joueur
            salle = joueur.salle
            variables.update({
                    "joueur": joueur,
                    "salle": salle,
            })

    def __getstate__(self):
        attrs = Contexte.__getstate__(self)
        attrs["py_prompt"] = ">>> "
        if "console" in attrs:
            del attrs["console"]

        return attrs

    def get_prompt(self):
        """Retourne le prompt"""
        return self.py_prompt

    def accueil(self):
        """Message d'accueil du contexte"""
        res = dedent("""
            |tit|Console scripting :|ff|

            Vous pouvez entrer ici du code scripting classique et
            voir le résultat. C'est une façon simple et parfois pratique
            de tester un script avant de le mettre en ligne. Ce peut
            être aussi un moyen très pratique pour exécuter du scripting
            à la volée et faire des choses non permises par les commandes
            (comme illuminer toutes les salles d'une certaine zone
            et mnémonique).

            Les alertes seront affichées directement dans la console
            plutôt qu'envoyées au système.""".lstrip("\n"))

        return res

    def interpreter(self, msg):
        """Méthode d'interprétation du contexte"""
        if msg.startswith("/"):
            msg = msg[1:]
            parties = msg.split(" ")
            opt = parties[0].lower()
            reste = " ".join(parties[1:])
            if hasattr(self, "opt_{}".format(opt)):
                getattr(self, "opt_{}".format(opt))(reste)
            else:
                self.pere << "|err|Option inconnue.|ff|"
        else:
            # Exécution du code
            ret = False
            try:
                instruction = self.test.ajouter_instruction(msg)
            except Exception as err:
                self.pere << str(err)
                return

            py_code = (" " * 4 * instruction.niveau) + instruction.code_python
            sys.stdin = self.pere
            sys.stdout = self.pere
            sys.stderr = self.pere
            nb_msg = self.pere.nb_msg
            try:
                ret = self.console.push(py_code)
                self.py_prompt = "... " if ret else ">>> "
            except Exception:
                self.pere << traceback.format_exc()
            else:
                if nb_msg == self.pere.nb_msg:
                    self.pere.envoyer("")
            finally:
                sys.stdin = sys.__stdin__
                sys.stdout = sys.__stdout__
                sys.stderr = sys.__stderr__

    def opt_q(self, arguments):
        """Quitte le contexte."""
        self.fermer()
        self.pere << "Fermeture de la console Python."

    def opt_v(self, arguments):
        """Affiche les variables.

        Syntaxe :
            /v (<variable>)

        """
        variables = self.evenement.espaces.variables
        if arguments:
            try:
                variable = variables[arguments]
            except KeyError:
                self.pere << "|err|Variable {} introuvable.|ff|".format(
                        repr(arguments))
                return
            if variable is None:
                self.pere << "Valeur nulle."
            elif variable is True:
                self.pere << "VRAI"
            elif variable is False:
                self.pere << "FAUX"
            else:
                self.pere << str(variable)

            return

        # On affiche toutes les variables
        variables = tuple(variables.keys())
        variables = sorted(variables)
        self.pere << "Variables définies : {}".format(" ".join(variables))

# -*-coding:Utf-8 -*

# Copyright (c) 2014 LE GOFF Vincent
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
# LIABLE FOR ANY orthographeCT, INorthographeCT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Package contenant la commande 'orthographe'."""

from primaires.interpreteur.commande.commande import Commande

class CmdOrthographe(Commande):

    """Commande 'orthographe'."""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "orthographe", "misspelling")
        self.schema = "<message>"
        self.aide_courte = "envoie un rapport de faute d'orthographe"
        self.aide_longue = \
            "Cette commande permet de créer un rapport de faute " \
            "d'orthographe très facilement. Il suffit en effet d'entrer " \
            "cette commande avec le texte de la faute et la correction. " \
            "Par exemple |cmd|%orthographe% parmis / parmi|ff| pour " \
            "indiquer que dans la description de la salle à cet endroit " \
            "se trouve une faute : parmis (écrit avec un s) alors qu'il " \
            "devrait être écrit sans s. Notez que cette syntaxe n'est " \
            "pas obligatoire et ne sera pas analysée par le système, vous " \
            "pouvez aussi rapporter des fautes d'orthographes dans " \
            "d'autres descriptions, celles de PNJ, de joueurs ou autre. " \
            "Mais dans ce cas, il vous faut en préciser l'origine " \
            "(l'administrateur réceptionnant le rapport n'aura que " \
            "l'information de la salle dans laquelle le rapport a été " \
            "émis). Essayez de vous limiter à une description par " \
            "commande : si vous voyez plusieurs fautes dans la salle, " \
            "par exemple, vous pouvez n'appeler cette commande " \
            "qu'une seule fois en précisant les fautes, mais si les " \
            "fautes se trouvent dans plusieurs salles différentes, " \
            "préférez faire une commande par salle."

    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande"""
        titre = "Faute d'orthographe"
        description = dic_masques["message"].message
        if len(description) < 10:
            personnage << "|err|Cette description de faute est trop " \
                    "courte.|ff|"
            return

        rapport = importeur.rapport.creer_rapport(titre, personnage)
        rapport.type = "bug"
        rapport.categorie = "faute"
        rapport.description.paragraphes.extend(description.split("\n"))
        personnage << "Le rapport de faute d'orthographe #{} a bien " \
                "été envoyé.".format(rapport.id)

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


"""Package contenant la commande 'enregistrer'"""

import traceback

from primaires.interpreteur.commande.commande import Commande

## Constantes
AIDE = """
Cette commande force l'enregistrement si la sauvegarde est en mode
binaire (pickle). L'enregistrement initié peut prendre un certain
temps (ceci dépend de la taille de la sauvegarde).
""".strip("\n")

class CmdEnregistrer(Commande):

    """Commande 'enregistrer'."""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "enregistrer", "save")
        self.groupe = "administrateur"
        self.aide_courte = "force l'enregistrement"
        self.aide_longue = AIDE

    def peut_executer(self, personnage):
        """Ne peut exécuter si le mode n'es tpas enregistrer."""
        return importeur.supenr.mode == "pickle"

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        for joueur in importeur.connex.joueurs_connectes:
            joueur.sans_prompt()
            joueur << "Sauvegarde en cours, veuillez patienter..."
            joueur.instance_connexion.envoyer_file_attente()

        try:
            importeur.supenr.enregistrer()
        except Exception as err:
            trace = traceback.format_exc()
            personnage << "|err|L'enregistrement a rencontré une " \
                    "erreur :|ff|\n" + trace
        else:
            for joueur in importeur.connex.joueurs_connectes:
                joueur << "... Sauvegarde effectuée, merci !"

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


"""Package contenant la commande 'lever'."""

from primaires.interpreteur.commande.commande import Commande

class CmdLever(Commande):

    """Commande 'lever'"""

    def __init__(self):
        """Constructeur de la commande."""
        Commande.__init__(self, "lever", "stand")
        self.nom_categorie = "bouger"
        self.aide_courte = "permet de se relever"
        self.aide_longue = \
            "Cette commande permet de se lever quand vous êtes assis " \
            "ou couché."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        personnage.agir("lever")
        if "allonge" not in personnage.etats and "assis" not in \
                personnage.etats:
            personnage << "|err|Vous n'êtes ni assis ni allongé.|ff|"
            return

        repos = personnage.etats.get("assis")
        if repos is None:
            repos = personnage.etats.get("allonge")

        if repos.sur:
            repos.sur.script["lève"]["avant"].executer(personnage=personnage, salle=personnage.salle)

        personnage.etats.retirer("assis")
        personnage.etats.retirer("allonge")
        personnage << "Vous vous levez."
        personnage.salle.envoyer("{} se lève.", personnage)

        if repos.sur:
            repos.sur.script["lève"]["après"].executer(personnage=personnage, salle=personnage.salle)


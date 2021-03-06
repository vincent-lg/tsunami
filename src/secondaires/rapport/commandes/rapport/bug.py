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


"""Package contenant le paramètre 'bug' de la commande 'rapport'."""

from primaires.interpreteur.masque.parametre import Parametre
from primaires.interpreteur.editeur.presentation import Presentation

class PrmBug(Parametre):

    """Commande 'rapport bug'"""

    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "bug", "bug")
        self.groupe = "joueur"
        self.schema = "(<message>)"
        self.aide_courte = "crée un rapport de bug"
        self.aide_longue = \
            "Cette commande permet de créer un nouveau rapport de " \
            "bug. Vous devez préciser en argument le titre du rapport " \
            "à créer. Un éditeur s'ouvrira alors pour vous permettre " \
            "de renseigner plus précisément le bug rencontré."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        if dic_masques["message"] is None:
            commande, trace = importeur.rapport.traces.get(personnage,
                    (None, None))
            if trace is None:
                personnage << "|err|Aucune erreur n'a été rapportée pour " \
                        "votre joueur.\nVous devez donc préciser un titre " \
                        "pour le bug que vous voulez rapporter.|ff|"
                return

            titre = "Erreur durant la commande {}".format(repr(commande))
            description = trace
        else:
            titre = dic_masques["message"].message
            description = ""

        rapport = importeur.rapport.creer_rapport(titre, personnage,
                ajouter=False)
        rapport.type = "bug"
        if description:
            rapport.description.paragraphes.extend(description.split("\n"))

        editeur = importeur.interpreteur.construire_editeur(
                "bugedit", personnage, rapport)
        personnage.contextes.ajouter(editeur)
        editeur.actualiser()

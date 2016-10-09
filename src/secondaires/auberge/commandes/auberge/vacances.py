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


"""Fichier contenant le paramètre 'vacances' de la commande 'auberge'."""

from primaires.format.tableau import Tableau, DROITE
from primaires.interpreteur.masque.parametre import Parametre

class PrmVacances(Parametre):

    """Commande 'auberge vacances'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "vacances", "vacations")
        self.schema = "(<cle>)"
        self.aide_courte = "affiche les joueurs en vacances"
        self.aide_longue = \
                "Cette commande permet de voir les joueurs actuellent " \
                "en vacances. Sans paramètre, elle affiche la liste " \
                "des joueurs en vacances. Vous pouvez préciser en " \
                "paramètre |ent|clear|ff| pour effacer la liste des " \
                "joueurs actuellement en vacances."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        cle = ""
        if dic_masques["cle"]:
            cle = dic_masques["cle"].cle

        if cle.lower() == "clear":
            for auberge in importeur.auberge.auberges.values():
                auberge.vacances[:] = []

            personnage << "Suppression de la liste des joueurs en vacances."
            return

        # Créqation du tableau
        msg = "Liste des joueurs en mode vacances :"
        vacances = importeur.auberge.vacances
        if vacances:
            for joueur in vacances:
                msg += "\n* " + joueur.nom
        else:
            msg += "\n  Aucun joueur n'est enregistré dans le mode vacances."

        personnage << msg

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


"""Package contenant la commande 'evenement'."""

from primaires.format.fonctions import oui_ou_non
from primaires.format.tableau import Tableau
from primaires.interpreteur.commande.commande import Commande

class CmdEvenement(Commande):

    """Commande 'evenement'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "évènement", "event")
        self.groupe = "administrateur"
        self.nom_categorie = "batisseur"
        self.schema = "(<cle>)"
        self.aide_courte = "consulte les évènements"
        self.aide_longue = \
            "Cette commande permet de lister les évènements existants, " \
            "ainsi que s'inscrire ou se désinscrire d'un évènement. " \
            "Sans argument, cette commande affiche un tableau des " \
            "évènements actuels, montrant ceux auxquels vous êtes " \
            "inscrits. Vous pouvez également préciser en paramètre " \
            "le nom dun évènement pour s'y inscrire, ou s'en désinscrire, " \
            "si vous y êtes déjà inscrit."

    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande."""
        if dic_masques["cle"]:
            cle = dic_masques["cle"].cle
            if cle not in importeur.evt.evenements:
                personnage << "|err|Évènement {} inconnu.|ff|".format(
                        repr(cle))
                return

            evt = importeur.evt.evenements[cle]
            if personnage in evt.inscrits:
                evt.inscrits.remove(personnage)
                personnage << "Vous êtes désinscrit de l'évènement {}.".format(
                        cle)
            else:
                evt.inscrits.append(personnage)
                personnage << "Vous êtes inscrit à l'évènement {}.".format(
                        cle)

            return

        tableau = Tableau()
        tableau.ajouter_colonne("Clé")
        tableau.ajouter_colonne("Aide")
        tableau.ajouter_colonne("Inscrit")

        for evt in sorted(importeur.evt.evenements.values(),
                key=lambda e: e.cle):
            inscrit = oui_ou_non(personnage in evt.inscrits)
            tableau.ajouter_ligne(evt.cle, evt.aide, inscrit)

        personnage << tableau.afficher()

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
# ARE DISCLAIMED. IN NO Ediligence SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant le paramètre 'liste' de la commande 'diligence'."""

from primaires.format.fonctions import oui_ou_non
from primaires.format.tableau import Tableau, DROITE
from primaires.interpreteur.masque.parametre import Parametre

class PrmListe(Parametre):

    """Commande 'diligence liste'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "liste", "list")
        self.aide_courte = "liste les diligences maudites"
        self.aide_longue = \
            "Cette commande liste les diligences maudites, permet " \
            "de savoir si elles sont ouvertes ou à l'état de brouillon, " \
            "et connaître d'autres informations génériques."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        diligences = list(importeur.diligence.diligences.values())
        diligences = sorted(diligences, key=lambda d: d.cle)
        if len(diligences) == 0:
            personnage << "|att|Aucune diligence maudite définie.|ff|"
            return

        tableau = Tableau()
        tableau.ajouter_colonne("Clé")
        tableau.ajouter_colonne("Ouverte")
        tableau.ajouter_colonne("Salles", DROITE)
        tableau.ajouter_colonne("Nombre en jeu", DROITE)
        for diligence in diligences:
            zones = [z for z in importeur.salle.zones.values() if \
                    z.cle.startswith(diligence.cle + "_")]
            nb = len(zones)
            tableau.ajouter_ligne(diligence.cle, oui_ou_non(
                    diligence.ouverte), len(diligence.salles), nb)

        personnage << tableau.afficher()

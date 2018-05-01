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


"""Package contenant la commande 'route liste'."""

from primaires.format.tableau import Tableau, DROITE
from primaires.interpreteur.masque.parametre import Parametre

class PrmListe(Parametre):

    """Commande 'route liste'"""

    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "liste", "list")
        self.aide_courte = "affiche la liste des routes"
        self.aide_longue = \
            "Cette commande permet d'afficher la liste des " \
            "routes. Dans ce tableau se trouve l'origine de la route, " \
            "sa destination, sa taille (c'est-à-dire le nombre de " \
            "salles intermédiaires, en comptant la salle finale de " \
            "la liste). Les routes en construction n'ont pas de " \
            "destination définie."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande."""
        routes = list(importeur.route.routes.values())
        routes.sort(key=lambda t: t.ident)
        if not routes:
            personnage << "|att|Aucune route n'a été créée.|ff|"
            return

        tableau = Tableau("Routes existantes")
        tableau.ajouter_colonne("ID", DROITE)
        tableau.ajouter_colonne("Origine")
        tableau.ajouter_colonne("Destination")
        tableau.ajouter_colonne("Taille", DROITE)

        for i, route in enumerate(routes):
            origine = route.origine
            origine = origine.ident if origine else "|att|inconnue|ff|"
            destination = route.destination
            destination = destination.ident if destination else \
                    "|att|inconnue|ff|"
            tableau.ajouter_ligne(i + 1, origine, destination,
                    str(len(route.salles)))

        personnage << tableau.afficher()

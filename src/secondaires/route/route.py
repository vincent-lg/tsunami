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


"""Fichier contenant la classe Route, détaillée plus bas."""

from abstraits.obase import BaseObj
from secondaires.route.description import DescriptionRoute

class Route(BaseObj):

    """Classe représentant une route.

    Une route relie deux salles (origine et destination) et
    indique les sorties intermédiaires qui doivent être prises pour
    se déplacer d'origine à destination.

    """

    enregistrer = True

    def __init__(self, origine):
        """Constructeur de la fiche."""
        BaseObj.__init__(self)
        self.origine = origine
        self.destination = None
        self.salles = []
        self.sorties = []
        self._construire()

    def __getnewargs__(self):
        return (None, )

    def __repr__(self):
        return "<Route {}>".format(self.str_ident)

    def __str__(self):
        return self.str_ident

    def __len__(self):
        return len(self.sorties)

    def __eq__(self, route):
        """Aide à la comparaison : ==."""
        return self.origine is route.origine and self.salles == route.salles

    def __ne__(self, route):
        """Aide à la comparaison : !=."""
        return not (self == route)

    def __ge__(self, route):
        """Aide à la comparaison : <=."""
        return len(self) <= len(route)

    def __gt__(self, route):
        """Aide à la comparaison : <."""
        return len(self) < len(route)

    def __le__(self, route):
        """Aide à la comparaison : >=."""
        return len(self) >= len(route)

    def __lt__(self, route):
        """Aide à la comparaison : >."""
        return len(self) > len(route)

    def __hash__(self):
        return hash(self.ident)

    @property
    def finie(self):
        return self.destination is not None

    @property
    def ident(self):
        origine = self.origine
        ident = []
        if self.origine:
            ident.append(self.origine.ident)
            if self.destination:
                ident.append(self.destination.ident)

        return tuple(ident)

    @property
    def str_ident(self):
        ident = self.ident
        if len(ident) == 2:
            return "de {} à {}".format(ident[0], ident[1])
        elif len(ident) == 1:
            return "de {} à ...".format(ident[0])
        else:
            return "inconnue"

    @property
    def enfants(self):
        """Retourne les routes enfants de self.

        Ces routes sont celles dont l'origine est la destination
        de self (incluant donc la route contraire de self).

        """
        routes = list(importeur.route.routes.values())
        return [r for r in routes if r.finie and r.origine is self.destination]

    @property
    def description(self):
        """Retourne la description de la route."""
        description = DescriptionRoute(self.origine)
        description.ajouter_route(self)
        if self.destination:
            description.completer(self.destination)

        return description

    def precede(self, origine, destination):
        """Retourne true si origine précède destination."""
        salles = [self.origine]
        salles.extend(self.salles)
        return salles.index(origine) < salles.index(destination)

    def ajouter_sortie(self, salle):
        """Cherche à ajouter une nouvelle sortie.

        La salle passée en paramètre est la salle à ajouter à la*
        route en construction. La dernière salle est récupérée.
        Une sortie directe doit être trouvée entre la dernière
        salle de la route et la nouvelle salle.

        """
        if self.finie:
            raise ValueError("Cette route est déjà finie")

        derniere = self.origine
        if self.salles:
            derniere = self.salles[-1]

        # Cherche à récupérer la sortie entre 'derniere' et 'salle'
        direction = ""
        for sortie in derniere.sorties:
            if sortie.salle_dest is salle:
                direction = sortie.direction
                break

        if direction == "":
            raise ValueError("Impossible de trouver une sortie entre " \
                    "{} et {}".format(derniere, salle))

        self.sorties.append(direction)
        self.salles.append(salle)
        return direction

    def completer(self, reciproque=True):
        """Complète la route.

        La dernière salle entrée est utilisée.

        Si le paramètre 'reciproque' est à True, la route en sens
        contraire est également créée.

        """
        if self.finie:
            raise ValueError("Cette route est déjà finie")

        if not self.salles:
            raise ValueError("Il n'y a pas de salles enregistrées " \
                    "dans cette route")

        del importeur.route.routes[self.ident]
        derniere = self.salles[-1]
        self.destination = derniere
        importeur.route.ajouter_route(self)

        if reciproque:
            route = importeur.route.creer_route(derniere)
            for salle in tuple(reversed(self.salles))[1:]:
                route.ajouter_sortie(salle)

            route.ajouter_sortie(self.origine)
            route.completer(False)

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


"""Fichier contenant la classe DescriptionRoute, détaillée plus bas."""


class DescriptionRoute:

    """Classe représentant une suite de routes.

    À la différence de la classe 'Route' (module 'route'), une
    description n'est pas destinée à être enregistrée : elle est
    simplement créée pour représenter un chemin qui peut passer
    par plusieurs routes. Une description de route a pour but :
    *   De lister linéairement les salels et sorties constituant la route ;
    *   De chercher les "raccourcis" en évitant les doublons
        ('A B C D C D E' doit être simplifié en 'A B C D E').

    """

    def __init__(self, origine):
        """Constructeur de la fiche."""
        self.origine = origine
        self.salles = []
        self.sorties = []

    def __repr__(self):
        return "<DescriptionRoute {}>".format(self.str_ident)

    def __str__(self):
        return self.str_ident

    @property
    def destination(self):
        return self.salles[-1] if self.salles else None

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

    def ajouter_route(self, route):
        """Ajoute la route indiquée."""
        if len(self.salles) == 0:
            # La description est vide, cherche l'origine dans la route
            if self.origine in route.salles:
                indice = route.salles.index(self.origine)
                self.salles.extend(route.salles[indice + 1:])
                self.sorties.extend(route.sorties[indice + 1:])
            elif self.origine is route.origine:
                self.salles.extend(route.salles)
                self.sorties.extend(route.sorties)
            else:
                raise ValueError("l'origine de la route {} ne peut " \
                        "être trouvé dans {}".format(self.origine, route))
        else:
            self.salles.extend(route.salles)
            self.sorties.extend(route.sorties)

    def completer(self, destination):
        """Termine la description de la route à la salle indiquée."""
        if destination not in self.salles:
            raise ValueError("la salle {} n'est pas présente dans " \
                    "la description indiquée".format(destination,
                    self.str_ident))

        indice = self.salles.index(destination)
        self.salles[:] = self.salles[:indice + 1]
        self.sorties[:] = self.sorties[:indice + 1]
        self.raccourcir()

    def raccourcir(self):
        """Raccourci la route.
        
        Si la route prend les salles 1 2 3 2 4 5, cette méthode
        raccourci la route à 1 2 4 5.
        
        """
        i = 0
        salles = []
        sorties = []
        while i < len(self.salles):
            salle = self.salles[i]
            sortie = self.sorties[i]
            salles.append(salle)
            sorties.append(sortie)
            i = len(self.salles) - list(reversed(self.salles)).index(
                    salle)
        
        self.salles[:] = salles
        self.sorties[:] = sorties
        
    def afficher(self, tronquer=0, ligne=False):
        """Affichage de la route."""
        chaine = "{} ({} salles) : ".format(self.origine, len(self.salles))
        coupe = False
        sep = ", " if ligne else "\n"
        for i, salle in enumerate(self.salles):
            sortie = self.sorties[i]

            if i > 0:
                chaine += sep

            chaine += "{} ({})".format(sortie, salle.ident)

            if tronquer > 0 and i >= tronquer - 1:
                chaine += ", ..."
                coupe = True
                break

        if coupe:
            sep = " " if ligne else "\n"
            chaine += "{sep}et {} ({})".format(self.sorties[-1],
                    self.salles[-1], sep=sep)

        return chaine

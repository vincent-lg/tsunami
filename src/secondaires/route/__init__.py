# -*-coding:Utf-8 -*

# Copyright (c) 2015 LE GOFF Vincent
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


"""Fichier contenant le module secondaire route."""

from abstraits.module import *
from corps.fonctions import valider_cle
from primaires.format.fonctions import format_nb
from secondaires.route.route import Route

class Module(BaseModule):

    """Module gérant les routes sur Vancia.

    Une route est un chemin reliant deux points, constitué d'une
    suite de directions. Les routes définies forment un complexe
    (une carte, un schéma, un graph) que l'on peut utiliser pour
    trouver le chemin le plus court entre deux points.

    Imaginons par exemple la liste de points suivants : A, B, C et
    D. On connaît les distances suivantes (la distance est le nombre
    de salles séparant chaque point) :
        A->B : 15 salles
        A->C : 10 salles
        B->D : 20 salles
        C->D : 10 salles

    Pour aller de A à D, on a donc deux chemins possibles : ABD
    ou ACD. ABD mesure 35 salles de long, tandis qu'ACD mesure 20
    salles. C'est donc ACD qui sera choisi en tant que chemin le
    plus court. La suite des sorties à utiliser sera d'abord les
    sorties de A à C, puis celles de C à D.

    """

    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "route", "secondaire")
        self.routes = {}
        self.logger = self.importeur.man_logs.creer_logger(
                "route", "route")
        self.en_cours = {}

    def init(self):
        """Chargement des objets du module."""
        routes = self.importeur.supenr.charger_groupe(Route)
        for route in routes:
            if route.ident:
                self.ajouter_route(route)

        self.logger.info(format_nb(len(routes),
                "{nb} route{s} récupérée{s}", fem=True))

        BaseModule.init(self)

    def creer_route(self, salle):
        """Crée une route."""
        route = Route(salle)
        self.ajouter_route(route)
        return route

    def ajouter_route(self, route):
        """Ajoute la route en cours de construction."""
        self.routes[route.ident] = route

    def supprimer_route(self, ident):
        """Supprime la route dont l'identifiant est précisé.

        L'identifiant est un tuple composé de deux chaînes :
        l'identifiant de la salle d'origine et l'identifiant de la
        salle de destination. Si la route est en construction, seul
        l'identifiant de la salle d'origine est disponible (le tuple
        a une longueur de 1 au lieu de 2).

        """
        self.routes.pop(ident).detruire()

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

from queue import PriorityQueue

from abstraits.module import *
from corps.fonctions import valider_cle
from primaires.format.fonctions import format_nb
from secondaires.route import commandes
from secondaires.route.description import DescriptionRoute
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

    def config(self):
        """Configuration du module."""
        # Extension du scripting
        self.importeur.scripting.a_charger.append(self)

        BaseModule.config(self)

    def init(self):
        """Chargement des objets du module."""
        routes = self.importeur.supenr.charger_groupe(Route)
        for route in routes:
            if route.ident:
                self.ajouter_route(route)

        self.logger.info(format_nb(len(routes),
                "{nb} route{s} récupérée{s}", fem=True))

        self.importeur.hook["personnage:deplacer"].ajouter_evenement(
                self.etendre_route)

        BaseModule.init(self)

    def ajouter_commandes(self):
        """Ajout des commandes dans l'interpréteur"""
        self.commandes = [
            commandes.route.CmdRoute(),
        ]

        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)

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

    def enregistrer(self, personnage):
        """Enregistre un point.

        Si le personnage ne dessine aucune route actuellement, en
        crée une nouvelle. Sinon, complète la route.

        """
        route = self.en_cours.get(personnage)
        if route is None:
            route = self.creer_route(personnage.salle)
            self.en_cours[personnage] = route
        else:
            del self.en_cours[personnage]
            route.completer()

        return route

    def etendre_route(self, personnage, destination, sortie, endurance):
        """Étend la route si besoin."""
        if personnage in self.en_cours:
            route = self.en_cours[personnage]
            route.ajouter_sortie(destination)
            personnage << "Ajout de {} à la route {}.".format(
                    destination, route.str_ident)

    def trouver_chemin(self, origine, destination):
        """Trouve le chemin le plus court entre deux salles.

        Les deux salles doivent se trouver dans le complexe des*
        routes (soit en tant que salle d'origine, de destination
        ou de salles intermédiaires).

        Algorithme utilisé : Dijkstra.
        (http://www.redblobgames.com/pathfinding/a-star/introduction.html)

        """
        routes_origines = []
        routes_destinations = []

        for route in self.routes.values():
            # La route contient-elle 'origine' ?
            if route.origine is origine or origine in route.salles:
                routes_origines.append(route)
            # La route contient-elle 'destination' ?
            if destination in route.salles:
                routes_destinations.append(route)

        # Si on n'a pu trouver de route, on lève une exception ValueError
        if len(routes_origines) == 0:
            raise ValueError("{} n'a pas pu être trouvé dans le " \
                    "complexe des routes".format(origine))
        if len(routes_destinations) == 0:
            raise ValueError("{} n'a pas pu être trouvé dans le " \
                    "complexe des routes".format(destination))

        # Si une route directe existe entre les deux salles, la retourne
        communes = []
        for route in routes_origines:
            if route in routes_destinations:
                communes.append(route)
        
        communes = [r for r in communes if r.precede(origine, destination)]
        if communes:
            route = communes[0]
            description = DescriptionRoute(origine)
            description.ajouter_route(route)
            description.completer(destination)
            return description

        # On explore maintenant toutes les possibilités de liaison
        couts = {}
        for route_origine in routes_origines:
            for route_destination in routes_destinations:
                start = route_origine
                goal = route_destination
                frontier = PriorityQueue()
                frontier.put(start, 0)
                came_from = {}
                cost_so_far = {}
                came_from[start] = None
                cost_so_far[start] = 0

                while not frontier.empty():
                    current = frontier.get()
                    if current is goal:
                        break

                    for next in current.enfants:
                        new_cost = cost_so_far[current] + len(next)
                        if next not in cost_so_far or new_cost < cost_so_far[
                            next]:
                            cost_so_far[next] = new_cost
                            priority = new_cost
                            frontier.put(next, priority)
                            came_from[next] = current

                current = goal
                path = [current]
                while current is not start:
                    current = came_from.get(current)
                    if current is None:
                        break

                    path.append(current)

                path.reverse()

                # Vérifie la continuité de la route
                if path[0] is route_origine and path[-1] is route_destination:
                    cout = sum(len(r) for r in path)
                    if origine in route_origine.salles:
                        indice = route_origine.salles.index(origine)
                        cout -= len(route_origine.salles) - 1 - indice

                    indice = route_destination.salles.index(destination)
                    cout -= len(route_destination.salles) - 1 - indice
                    couts[cout] = path

        # Cherche la route la plus courte
        if couts:
            courte = couts[min(couts)]
        else:
            raise ValueError("impossible de trouver la route " \
                    "entre {} et {}".format(origine, destination))

        # Création de la description de route
        description = DescriptionRoute(origine)
        for route in courte:
            description.ajouter_route(route)

        description.completer(destination)
        return description

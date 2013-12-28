# -*-coding:Utf-8 -*

# Copyright (c) 2011 LE GOFF Vincent
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


"""Fichier contenant la classe Etendue, détaillée plus bas."""

from math import fabs
from random import choice
import sys

from vector import mag

from abstraits.obase import BaseObj
from .coordonnees import Coordonnees

class Etendue(BaseObj):

    """Cette classe représente une étendue d'eau.

    Une étendue d'eau peut être un lac, une rivière, une mer ou un océan.
    A noter, cela est extrêmement important, qu'une étendue ne retient
    pas la position où elle se trouve, seulement ses délimiteurs.
    C'est pourquoi faire une étendue d'eau infinie est une mauvaise idée.

    Les étendues d'eaux peuvent être chaînées (une rivière se jète dans
    la mer).

    Attributs :
        obstacles -- dictionnaire des obstacles
        cotes -- un dictionnaire des côtes ({coord: salle}) [1]
        liens -- un dictionnaire des liens avec d'autres étendues
                ({coord: etendue})

    [1] Les côtes ici sont celles débarcables. Toutes les salles non
        débarcables sont des obstacles.

    """

    enregistrer = True
    _nom = "etendue"
    _version = 1
    def __init__(self, cle):
        """Création de l'éttendue."""
        BaseObj.__init__(self)
        self.cle = cle
        self.altitude = 0
        self.profondeur = 4
        self.obstacles = {}
        self.cotes = {}
        self.liens = {}
        self.projections = {}

    def __getnewargs__(self):
        return ("", )

    def __repr__(self):
        return "<étendue {}>".format(repr(self.cle))

    def __str__(self):
        return self.cle

    def __contains__(self, coordonnees):
        """Retourne True si les coordonnées sont des côtes de l'étendue.

        Les coordonnées peuvent être sous la forme d'un tuple ou d'un objet
        Coordonnees.

        """
        coordonnees = self.convertir_coordonnees(coordonnees)
        return coordonnees in self.points.keys()

    def __getitem__(self, item):
        """Retourne le point correspondant aux coordonnées entrées.

        Les coordonnées peuvent être :
            un tuple
            un objet de type Coordonnees

        Le retour peut être de type :
            None : c'est un obstacle
            salle : une côte débarcable
            etendue : une étendue voisine

        """
        coordonnees = self.convertir_coordonnees(item)
        return self.points[coordonnees]

    @property
    def points(self):
        """Constitution d'un dictionnaire des points."""
        points = self.obstacles.copy()
        points.update(self.cotes)
        return points

    @staticmethod
    def convertir_coordonnees(coordonnees):
        """Retourne un tuple des coordonnées en 2D.

        Le type des coordonnées peut être :
            Un tuple de N dimensions (N >= 2)
            Un objet de type Coordonnees

        """
        if isinstance(coordonnees, tuple):
            # Les tuples sont ramenés à 2 dimensions
            coordonnees = coordonnees[:2]
        elif isinstance(coordonnees, Coordonnees):
            coordonnees = coordonnees.tuple()[:2]
        else:
            raise TypeError(
                    "type de coordonnées non traité : {}".format(repr(
                    type(coordonnees))))

        return coordonnees

    def ajouter_obstacle(self, coordonnees, obstacle):
        """Ajoute l'obstacle."""
        coordonnees = self.convertir_coordonnees(coordonnees)
        if coordonnees in self.points.keys():
            raise ValueError(
                    "un point de coordonnées {} existe déjà".format(
                    coordonnees))

        self.obstacles[coordonnees] = obstacle

    def est_obstacle(self, coordonnees):
        """Retourne True si les coordonnées sont un obstacle."""
        coordonnees = self.convertir_coordonnees(coordonnees)
        return coordonnees in self.obstacles

    def est_cote(self, salle):
        """Retourne True si la salle est une côte."""
        coordonnees = self.convertir_coordonnees(salle.coords)
        return coordonnees in self.cotes.keys()

    def est_lien(self, coordonnees):
        """Retourne True si les coordonnées sont un lien."""
        coordonnees = self.convertir_coordonnees(coordonnees)
        return coordonnees in self.liens.keys()

    def ajouter_cote(self, salle):
        """Ajoute la côte accostable (peut-être une île dans l'étendue)."""
        coordonnees = self.convertir_coordonnees(salle.coords)
        if coordonnees in self.points.keys():
            raise ValueError(
                    "un point de coordonnées {} existe déjà".format(
                    coordonnees))

        self.cotes[coordonnees] = salle
        salle.etendue = self

    def ajouter_lien(self, coordonnees, etendue):
        """Ajoute le lien vers une autre étendue.

        Note : un lien lie deux étendues. Par exemple, on peut dire que le
        point (3, 4) est un lien de l'étendue riviere_picte vers
        mer_sans_fin.

        """
        coordonnees = self.convertir_coordonnees(coordonnees)
        if coordonnees in self.points.keys():
            raise ValueError(
                    "un point de coordonnées {} existe déjà".format(
                    coordonnees))

        self.liens[coordonnees] = etendue
        etendue.liens[coordonnees] = self

    def supprimer_obstacle(self, coordonnees):
        """Supprime un obstacle."""
        coordonnees = self.convertir_coordonnees(coordonnees)
        del self.obstacles[coordonnees]

    def supprimer_cote(self, salle):
        """Supprime la salle des côtes."""
        coordonnees = self.convertir_coordonnees(salle.coords)
        salle = self.cotes[coordonnees]
        salle.etendue = None
        del self.cotes[coordonnees]

    def supprimer_lien(self, coordonnees):
        """Supprime un lien."""
        coordonnees = self.convertir_coordonnees(coordonnees)
        etendue = self.liens.pop(coordonnees)
        if coordonnees in etendue.liens:
            del etendue.liens[coordonnees]

    def get_etendues_proches(self, x, y, distance, exceptions=None):
        """Retourne les étendues liées à self suffisamment proches.

        Les apramètres à préciser sont :
            x -- l'âxe X du point de départ
            y -- l'âxe Y du point de départ
            distance -- la distance maximale du point de départ

        Les liens sont parcourus pour trouver les étendues proches.
        Si des étendues sont trouvées, la même recherche est effectuée
        récursivement dessus.

        """
        exceptions = exceptions or set()
        exceptions.add(self)
        etendues = [self]
        for (bx, by), etendue in self.liens.items():
            if mag(x, y, 0, bx, by, 0) <= distance:
                if etendue not in exceptions:
                    etendues += etendue.get_etendues_proches(
                            x, y, distance, exceptions)

        return etendues

    def get_points_proches(self, x, y, distance, liens=True):
        """Retourne les points proches de la position indiquée.

        Paramètres à préciser :
            x -- la coordonnée X de la position
            y -- la coordonnée Y de la position
            distance -- la distance maximum des points recherchés
            liens -- recherche récursive dans les étendues liées

        """
        proches = {}
        altitude = self.altitude
        etendues = [self]
        if liens:
            etendues = self.get_etendues_proches(x, y, distance)

        for etendue in etendues:
            points = etendue.obstacles.copy()
            points.update(etendue.cotes)
            for (bx, by), point in points.items():
                if mag(x, y, altitude, bx, by, altitude) <= distance:
                    proches[(bx, by)] = point

        return proches

    def ajouter_multiple(self, o_x, o_y, d_x, d_y, nom_terrain):
        """Construit multiple points dans leétendue.

        Les paramètres à entrer sont :
            o_x -- l'âxe X du point d'origine
            o_y -- l'âxe Y du point d'origine
            d_x -- l'âxe X du point de destination
            o_y -- l'âxe Y du point de destination
            nom_terrain -- le nom du terrain

        La construction des multiples points est aléatoire. Le but du
        système est de créer un nombre variable de points pour relier origine
        et destination, mais il ne le fait pas nécessairement en ligne
        droite.

        """
        dir_x = d_x - o_x
        dir_y = d_y - o_y
        obstacle = importeur.salle.obstacles[nom_terrain]
        fini = False
        l_x = x = o_x
        l_y = y = o_y
        points = [(o_x, o_y)]
        def_points = self.points
        while not fini:
            if d_x > l_x:
                x = 1
            elif d_x < l_x:
                x = -1
            else:
                x = 0
            if d_y > l_y:
                y = 1
            elif d_y < l_y:
                y = -1
            else:
                y = 0

            choix = []
            if x != 0:
                nb = int(fabs(d_x - l_x))
                choix += [(l_x + x, l_y)] * nb
            if y != 0:
                nb = int(fabs(d_y - l_y))
                choix += [(l_x, l_y + y)] * nb

            point = choice(choix)
            l_x, l_y = point
            points.append((l_x, l_y))

            if l_x == d_x and l_y == d_y:
                fini = True

        nb = 0
        for x, y in points:
            coords = (x, y)
            if coords not in def_points:
                self.ajouter_obstacle(coords, obstacle)
                nb += 1

        return nb

    def verifier_continuite(self, x, y, e_x=None, e_y=None, o_x=None,
            o_y=None, obstacles=None):
        """Vérifie la continuité d'une étendue.

        Cette méthode permet de vérifier qu'une étendue d'eau est
        complète, c'est-à-dire qu'elle forme bien un cercle. Le principe
        est qu'on part du point x;y précisé en paramètre et qu'on
        essaye de faire le tour complet de l'étendue. Il doit y avoir
        un obstacle, une cote ou un lien sur les points successifs
        parcourus et on doit pouvoir revenir sur
        x;y au final.

        """
        print("Fork", x, y, e_x, e_y)
        e_x = e_x or x
        e_y = e_y or y
        o_x = o_x or x
        o_y = o_y or y
        if obstacles is None:
            obstacles = self.points.copy()
            obstacles.update(self.liens)

        complet = False
        while not complet:
            points = [
                (x + 1, y),
                (x - 1, y),
                (x, y + 1),
                (x, y - 1),
            ]

            points = [p for p in points if p not in ((x, y), (e_x, e_y))]

            # Combien de points y'a-t-il ici ?
            points = [p for p in points if p in obstacles]
            if len(points) == 0:
                raise LigneBrisee("Il n'y a aucun point après " \
                        "{}.{} (e={}.{})".format(x, y, e_x, e_y))
            elif len(points) == 1:
                t_x, t_y = points[0]
                if t_x == o_x and t_y == o_y:
                    return True
                elif (t_x, t_y) in obstacles:
                    x = t_x
                    y = t_y
                    continue
                else:
                    complet = False
                    break

            # Sinon on doit explorer plusieurs chemins
            for t_x, t_y in points:
                if t_x == o_x and t_y == o_y:
                    return True

                try:
                    self.verifier_continuite(t_x, t_y, x, y, o_x, o_y,
                            obstacles)
                except LigneBrisee as err:
                    continue
                else:
                    complet = True

            if not complet:
                break

        if not complet:
            raise LigneBrisee("Il y avait {} possibilités pour " \
                    "{}.{} mais elles sont toutes brisées".format(
                    len(points), x, y) + " " + str(erreur))

        return True

class LigneBrisee(RuntimeError):

    pass

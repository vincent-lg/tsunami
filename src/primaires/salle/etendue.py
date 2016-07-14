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


"""Fichier contenant la classe Etendue, détaillée plus bas."""

from math import fabs
from random import choice
import sys

from vector import mag

from abstraits.obase import BaseObj
from primaires.scripting.script import Script
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
    nom_scripting = "l'étendue d'eau"
    _nom = "etendue"
    _version = 1

    def __init__(self, cle):
        """Création de l'éttendue."""
        BaseObj.__init__(self)
        self.cle = cle
        self.altitude = 0
        self.profondeur = 4
        self.eau_douce = False
        self.obstacles = {}
        self.cotes = {}
        self.liens = {}
        self.segments_liens = {}
        self.origine = (None, None)
        self.contour = None
        self.script = ScriptEtendue(self)
        self._construire()

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

    def __getstate__(self):
        """Enregistrement de l'objet.

        On ne peut pas enregistrer les points tel quel car
        MongoDB n'aime pas les dictionnaires contenant des tuples en
        clés.

        """
        attrs = BaseObj.__getstate__(self)
        obstacles = {}
        for cle, point in attrs["obstacles"].items():
            obstacles["|".join([str(c) for c in cle])] = point

        attrs["obstacles"] = obstacles

        cotes = {}
        for cle, point in attrs["cotes"].items():
            cotes["|".join([str(c) for c in cle])] = point

        attrs["cotes"] = cotes

        liens = {}
        for cle, point in attrs["liens"].items():
            liens["|".join([str(c) for c in cle])] = point

        attrs["liens"] = liens

        return attrs

    def __setstate__(self, attrs):
        """Récupération de l'objet enregistré."""
        obstacles = {}
        for cle, point in attrs["obstacles"].items():
            if isinstance(cle, str):
                x, y = cle.split("|")
                cle = int(x), int(y)
            obstacles[cle] = point

        attrs["obstacles"] = obstacles

        cotes = {}
        for cle, point in attrs["cotes"].items():
            if isinstance(cle, str):
                x, y = cle.split("|")
                cle = int(x), int(y)
            cotes[cle] = point

        attrs["cotes"] = cotes

        liens = {}
        for cle, point in attrs["liens"].items():
            if isinstance(cle, str):
                x, y = cle.split("|")
                cle = int(x), int(y)
            liens[cle] = point

        attrs["liens"] = liens

        BaseObj.__setstate__(self, attrs)

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

    def determiner_segments_liens(self):
        """Détermine les segments des liens en fonctions des liens définis.

        À la différence des liens, qui ne sont que des points avec
        deux coordonnées (X, Y), le segment de lien définit un
        segment décrit par deux points. Les segments de liens sont
        utiles pour savoir, par exemple, si un navire traverse la
        ligne et change donc d'étendue.

        """
        liens = self.liens.copy()
        while liens:
            coords = list(liens.keys())[0]
            etendue = liens[coords]
            del liens[coords]
            voisins = []

            # On cherche tous les voisins
            # D'abord en variant X
            x, y = coords
            while ((x + 1), y) in liens:
                x += 1
                voisin = (x, y)
                vers = liens[voisin]
                if etendue is vers:
                    voisins.append(voisin)
                    del liens[voisin]

            x, y = coords
            while ((x - 1), y) in liens:
                x -= 1
                voisin = (x, y)
                vers = liens[voisin]
                if etendue is vers:
                    voisins.append(voisin)
                    del liens[voisin]

            if not voisins:
                # Puis en variant Y
                x, y = coords
                while (x, (y + 1)) in liens:
                    y += 1
                    voisin = (x, y)
                    vers = liens[voisin]
                    if etendue is vers:
                        voisins.append(voisin)
                        del liens[voisin]

                x, y = coords
                while (x, (y - 1)) in liens:
                    y -= 1
                    voisin = (x, y)
                    vers = liens[voisin]
                    if etendue is vers:
                        voisins.append(voisin)
                        del liens[voisin]

            # voisins fait 0 ou plus d'une coords de longueur
            if len(voisins) == 0:
                x, y = coords
                if (x - 1, y) in etendue.points:
                    origine = ((x - 1), y)
                    extremite = ((x + 1), y)
                else:
                    origine = (x, (y - 1))
                    extremite = (x, (y + 1))
            else:
                voisins.append(coords)
                origine = min(voisins)
                extremite = max(voisins)
                if origine[0] < extremite[0]:
                    origine = (origine[0] - 1, origine[1])
                    extremite = (extremite[0] + 1, extremite[1])
                else:
                    origine = (origine[0], origine[1] - 1)
                    extremite = (extremite[0], extremite[1] + 1)

            self.segments_liens[(origine, extremite)] = etendue

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

        # On détermine les segments de liens
        self.determiner_segments_liens()
        etendue.determiner_segments_liens()

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

        # On détermine les segments de liens
        self.determiner_segments_liens()
        etendue.determiner_segments_liens()

    def trouver_contour(self):
        """Recherche les contours de l'étendue."""
        x, y = self.origine
        if x is None or y is None:
            raise ValueError("Aucune origine n'est précisée")

        self.contour = self.get_contour(x, y)

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

    def get_contour(self, x, y, points=None, contour=None, ligne=None, premier=True):
        """Détermine les contours de l'étendue.

        Cette méthode retourne une liste de tuples représentant le
        contour ordonnée selon leur proximité. Le point (x, y) donné
        en paramètre est le point de départ de la recherche. Ensuite,
        cette méthode cherche les points voisins, c'est-à-dire ceux
        dont x varie de 1 ou y varie de 1, au choix (ce qui donne
        4 possibilités). Sur ces quatre possibilités, si il y en a
        une qui marche (il existe un point), la méthode recherche
        le point suivant en excluant d'office le point voisin qui
        a déjà été trouvé. Si il y en a plus d'une, la méthode cherche
        les points suivants de chaque segment récursivement. Le but
        est de trouver un contour, c'est-à-dire seulement les points
        proches constituant le tour de l'étendue (et non les îles).

        """
        if points is None:
            points = list(self.points.keys()) + list(self.liens.keys())

        if contour is None:
            contour = []

        if ligne is None:
            ligne = []

        ligne.append((x, y))
        while True:
            possibles = [
                (x - 1, y),
                (x + 1, y),
                (x, y - 1),
                (x, y + 1),
            ]

            t_contour = contour + ligne
            if len(t_contour) > 2 and t_contour[0] in possibles:
                contour.extend(ligne)
                return contour

            # On exclut les points déjà pris
            # On exclut pas le premier point qui peut nous servir
            # pour constater que la boucle est bouclée
            possibles = [p for p in possibles if p not in (contour + ligne)]

            # On cherche les points existants
            possibles = [p for p in possibles if p in points]

            # Si c'est le premier point, on en choisit un au hasard
            if len(contour + ligne) == 1:
                possibles = possibles[:1]

            # En fonction du nombre de résultat on agit différemment
            nb = len(possibles)
            if nb == 0:
                if premier:
                    raise ValueError("Aucun point voisin après {}.{}".format(x, y))

                return False
            elif nb == 1:
                # C'est parfait, on a qu'un voisin possible, on continue
                x, y = possibles[0]
                ligne.append((x, y))
            else:
                # Il y a plusieurs possibilités, on doit les explorer
                for possible in possibles:
                    t_ligne = list(ligne)
                    retour = self.get_contour(possible[0], possible[1],
                            points, contour, t_ligne, premier=False)
                    if retour:
                        return contour

                # À ce stade si on a pas trouvé la branche, on s'arrête
                if premier:
                    raise ValueError("Le point {}.{} offrant les branches " \
                            "{} ne peut former un contour complet".format(x, y,
                            possibles))

                return False

    def croise_lien(self, origine, destination):
        """Vérifie si le segment (origine, destination) croise un lien.

        La comparaison est effectuée grâce aux segments de liens
        définis dans l'étendue. Merlin/Gulfalf a contribué de façon
        significative à l'algorithme de croisement. Merci à lui.
        Si le segment croise un lien, retourne l'étendue de
        destination. Sinon retourne None.

        """
        # On inverse les coordonnées si besoin
        if origine[0] > destination[0]:
            origine, destination = destination, origine

        for (o_lien, d_lien), etendue in self.segments_liens.items():
            # Définition des segments
            # Segment AB
            (ax, ay) = origine
            (bx, by) = destination

            # Segment CD
            (cx, cy) = o_lien
            (dx, dy) = d_lien

            # Cas particulier : droite // à l'axe des ordonnées
            k1 = k2 = False

            # Calcul de l'équation du segment AB
            if ax != bx: # La droite n'est pas // à l'axe des ordonnées
                # Y = A1 X + B1
                a1 = (by - ay) / (bx - ax)
                b1 = ay - (ax * a1)
            else: # La droite est // à l'axe des ordonnées
                # X = C1
                k1 = True

            # Calcul de l'équation du segment CD
            if cx != dx: # La droite n'est pas // à l'axe des ordonnées
                # Y = A2 X + B2
                a2 = (dy - cy) / (dx - cx)
                b2 = cy - (cx * a2)
            else: # La droite est // à l'axe des ordonnées
                # X = C2
                k2 = True

            if k1 == False and k2 == False: # Cas général
                # Comparaison de la pente des 2 segments
                if a1 == a2:
                    continue
                else:
                    # On calcule leur point sécant
                    x = (b2 - b1) / (a1 - a2)
                    y = (a1 * x ) + b1

                    # Le point (X, Y) appartient bien à l'espace
                    # de points du segment AB
                    condition_ab = x >= ax and x <= bx

                    # Le point (X, Y) appartient bien à l'espace de points
                    # du segment CD
                    condition_cd = x >= cx and x <= dx

                    # Conclusion
                    if condition_ab and condition_cd:
                        return etendue
                    else:
                        continue
            elif k1 == True and k2 == False:
                # Le segment AB est // à l'axe des ordonnées
                x = ax
                y = (a2 * x) + b2
                liste_y = sorted([ay, by])
                if x >= cx and x <= dx and y >= liste_y[0] and y <= liste_y[1]:
                    return etendue
                else:
                    continue
            elif k1 == False and k2 == True:
                # Les segment CD est // à 'axe des ordonnées
                x = cx
                y = (a1 * x) + b1
                liste_y = sorted([cy, dy])
                if x >= ax and x <= bx and y >= liste_y[0] and y <= liste_y[1]:
                    return etendue
                else:
                    continue
            else:
                # Les 2 segments sont // à l'axe des ordonnées
                continue

class ScriptEtendue(Script):

    """Script et évènements propres aux étendues d'eau."""

    def init(self):
        """Initialisation du script"""
        # Événement entre
        evt_entre = self.creer_evenement("entre")
        evt_entre.aide_courte = "un navire entre dans l'étendue"
        evt_entre.aide_longue = \
            "Cet évènement est appelé quand un navire entre dans " \
            "l'étendue, venant d'une étendue différente et " \
            "traversant donc un lien entre étendues."

        # Configuration des variables de l'évènement entre
        var_centre = evt_entre.ajouter_variable("centre", "Salle")
        var_centre.aide = "la salle au centre du navire"
        var_cle = evt_entre.ajouter_variable("cle", "str")
        var_cle.aide = "la clé complète du navire (par exemple \"barque_8\")"
        var_origine = evt_entre.ajouter_variable("origine", "str")
        var_origine.aide = "la clé de l'étendue d'où vient le navire"

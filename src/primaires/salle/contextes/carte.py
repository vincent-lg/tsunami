# -*-coding:Utf-8 -*

# Copyright (c) 2013 LE GOFF Vincent
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


"""Fichier contenant le contexte d'édition d'une carte d'étendue d'eau."""

import re

from primaires.interpreteur.contexte import Contexte

# Constantes
RE_SIMPLE_REL = re.compile(r"^([A-Pa-p])([0-9]+)")
RE_SIMPLE_ABS = re.compile(r"^(-?[0-9]+)\.(-?[0-9]+)")


class CarteEtendue(Contexte):

    """Contexte permettant d'e voir et éditer la carte d'une étendue d'eau.

    Grâce à ce contexte, voir la carte d'une étendue d'eau sur
    différents plans (elle peut être assez grande) et ajouter des
    obstacles ou des liens doit être facile. Au lieu d'utiliser les
    coordonnées absolues, le contexte est programmé pour utiliser une
    grille de repérage simple (15 lignes de A à P et 20 colonnes de
    1 à 20) qui permet de préciser facilement un point repéré sur la
    carte, ou une suite de points.

    Voici les choses que l'on doit pouvoir faire :
        Place un obstacle "forêt" sur le point A8
        Trace une côte de type "falaise" de A1 à C15
        Trace un lien entre l'étendue A et B de B6 à L6
        Supprime l'obstacle A5

    Les coordonnées absolues peuvent être utilisées également. Dans
    ce cas elles sont séparées par un point :

        Trace une côte de type "montagne" de 20.-15 à 300.-10

    """

    nom = "salle:etendue:carte"

    def __init__(self, pere):
        """Constructeur du contexte"""
        Contexte.__init__(self, pere)
        self.opts.prompt_prf = ""
        self.opts.prompt_clr = ""
        self.opts.nl = False
        self.etendue = None
        self.x = None
        self.y = None
        self.nb_lignes = 16
        self.nb_col = 30

    def actualiser(self):
        """Actualise le contexte (affiche simplement l'accueil)."""
        self.pere << self.accueil()

    def accueil(self):
        """Message d'accueil du contexte"""
        if self.x is None or self.y is None:
            self.x, self.y = min(self.etendue.points.keys())

        etendue = self.etendue
        x, y = self.x, self.y
        nb_lignes = self.nb_lignes
        nb_col = self.nb_col
        limite_x = x + nb_col
        limite_y = y - nb_lignes
        res = "|tit|Carte de l'étendue {} :|ff|\n".format(
                self.etendue.cle)
        res += "\nCoin supérieur gauche : X={}, Y={}".format(
                self.x, self.y)
        res += "\nOptions disponibles :"
        res += "\n |cmd|/?|ff| pour obtenir de l'aide général sur ce contexte"
        res += "\n |cmd|/?d|ff| pour apprendre à se déplacer sur la carte"
        res += "\n |cmd|/?o|ff| pour apprendre à manipuler les obstacles"
        res += "\n |cmd|/?l|ff| pour apprendre à manipuler les liens"
        lignes = []
        haut = "  1   3   5   7   9  11  13  15  17  19  21  23  " \
                "25  27  29  "
        lignes.append(haut)
        points = etendue.points.copy()
        liens = etendue.liens.copy()
        lettres = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", \
                "K", "L", "M", "N", "O", "P"]
        for i in range(y, limite_y, -1):
            ligne = lettres[0]
            for j in range(x, limite_x):
                ligne += " "
                point = points.get((j, i))
                if point is None:
                    lien = liens.get((j, i))
                    if lien is None:
                        ligne += " "
                    else:
                        ligne += "+"
                else:
                    if hasattr(point, "nom"):
                        ligne += point.nom[0].capitalize()
                    elif hasattr(point, "nom_terrain"):
                        ligne += point.nom_terrain[0].capitalize()
                    else:
                        ligne += "?"

            ligne += " " + lettres[0]
            lignes.append(ligne)
            del lettres[0]

        lignes.append(haut)
        res += "\n\n" + "\n".join(lignes)
        return res

    def interpreter(self, msg):
        """Méthode d'interprétation du contexte"""
        options = {
            "q": self.opt_quitter,
            "i": self.opt_info,
            "a": self.opt_placer,
        }
        if msg.startswith("/"):
            opt = msg.split(" ")[0][1:].lower()
            reste = " ".join(msg.split(" ")[1:])
            if opt in options:
                return options[opt](reste)
            else:
                self.pere << "|err|Option inconnue.|ff|"
        elif msg and msg[0].lower() in "oens":
            self.deplacer(msg)
        elif msg:
            self.pere << "|err|Déplacement invalide. Entrez |cmd|/?d|err| " \
                    "pour de l'aide.|ff|"
        else:
            self.actualiser()

    def deplacer(self, msg):
        """Déplace la carte dans la direction indiquée.

        Le paramètre 'msg' peut contenir différents formats :
            s -- une page vers le sud
            s.5 -- 5 cases vers le sud
            s*5 -- 5 pages vers le sud

        """
        msg = msg.lower()
        directions = {
            "o": (-1,  0),
            "n": ( 0,  1),
            "e": ( 1,  0),
            "s": ( 0, -1),
        }

        direction = directions[msg[0]]
        x, y = direction
        msg = msg[1:]
        if msg == "":
            x *= self.nb_col
            y *= self.nb_lignes
        elif msg[0] == ".":
            try:
                nb = int(msg[1:])
                assert nb > 0
            except (ValueError, AssertionError):
                self.pere << "|err|Le nombre spécifié est invalide.|ff|"
                return
            else:
                x *= nb
                y *= nb
        elif msg[0] == "*":
            try:
                nb = int(msg[1:])
                assert nb > 0
            except (ValueError, AssertionError):
                self.pere << "|err|Le nombre spécifié est invalide.|ff|"
                return
            else:
                x *= nb * self.nb_col
                y *= nb * self.nb_lignes
        else:
            self.pere << "|err|Syntaxe invalide. Entrez |cmd|/?d|err| " \
                    "pour de l'aide.|ff|"
            return

        self.x += x
        self.y += y
        self.actualiser()

    def opt_quitter(self, reste):
        """Quitte le contexte."""
        self.fermer()
        self.pere << "Fermeture de la carte.|ff|"

    def opt_info(self, reste):
        """Cherche à donner l'information sur le point précisé."""
        coords, message = self.point_unique(reste)
        if coords is None:
            self.pere << message
            return

        etendue = self.etendue
        points = etendue.points
        msg = "Information sur le point {}.{} :\n".format(*coords)
        point = points.get(coords)
        print("Corodonnées", coords)
        lien = etendue.liens.get(coords)
        if point:
            if hasattr(point, "nom_terrain"):
                msg += "\n  Salle : {}".format(point.ident)
                msg += "\n  Terrain : {}".format(point.nom_terrain)
            else:
                msg += "\n  Obstacle de type {}".format(point.nom)
        elif lien:
            msg += "\n  Lien vers l'étendue {}".format(lien)
        else:
            self.pere << "Ce point est vide ou inexistant."
            return

        self.pere << msg

    def opt_placer(self, reste):
        """Place un nouveau point sur la carte."""
        coords, message = self.point_unique(reste)
        if coords is None:
            self.pere << message
            return

        etendue = self.etendue
        message = message.strip()
        terrain = importeur.salle.get_terrain(message)
        if not terrain:
            self.pere << "|err|Terrain {} inconnu.|ff|".format(repr(message))
            return

        obstacle = importeur.salle.obstacles[terrain.nom]
        if coords in etendue.obstacles:
            del etendue.obstacles[coords]
        if coords in etendue.liens:
            del etendue.liens[coords]

        etendue.ajouter_obstacle(coords, obstacle)
        self.actualiser()

    def point_unique(self, msg):
        """Retourne le point unique identifié par msg.

        Le point peut être identifié de deux manières :
            Soit en position relative (A8, C13, L17)
            Soit en position absolue (5.-2)

        On retourne :
            (None, None) -- le point n'a pas été trouvé
            ((x, y), reste) -- le point si trouvé

        """
        res = RE_SIMPLE_REL.search(msg)
        if res is None:
            res = RE_SIMPLE_ABS.search(msg)
            if res is None:
                return (None, "|err|Syntaxe invalide. Consultez " \
                        "|cmd|/?l|err| pour de l'aide.|ff|")
            else:
                x, y = res.groups()
                try:
                    x = int(x)
                    y = int(y)
                except ValueError:
                    return (None, "|err|Syntaxe invalide. Consultez " \
                            "|cmd|/?l|err| pour de l'aide.|ff|")
                else:
                    return ((x, y), msg[res.end():])
        else:
            lettre, nombre = res.groups()
            lettres = "abcdefghijklmnop"
            x = int(nombre) - 1
            y = lettres.index(lettre.lower())
            if x < 0:
                return (None, "|err|Syntaxe invalide. Consultez " \
                        "|cmd|/?l|err| pour de l'aide.|ff|")
            else:
                return ((self.x + x, self.y - y), msg[res.end():])

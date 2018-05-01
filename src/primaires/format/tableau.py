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


"""Fichier contenant la classe Tableau, détaillée plus bas."""

from textwrap import wrap

from primaires.format.fonctions import *

# Constantes
GAUCHE = 0
DROITE = 1
CENTRE = 2

class Tableau:

    """Classe définissant un tableau.

    Un tableau est un objet permettant de conserver des colonnes et
    des données pour chaque ligne. En sortie doit se trouver un tableau
    ASCII. Voici un exemple concret :
    >>> tableau = Tableau()
    >>> tableau.ajouter_colonne("nom")
    >>> tableau.ajouter_colonne("prix", alignement=DROITE)
    >>> tableau.ajouter_ligne("une truite", 5)
    >>> tableau.ajouter_ligne("un hareng", 10)
    >>> print(tableau)
    +------------+------+
    | Nom        | Prix |
    +------------+------+
    | une truite |    5 |
    | un hareng  |   10 |
    +------------+------+

    """

    def __init__(self, titre=None, alignement=GAUCHE):
        """Constructeur du tableau."""
        self.titre = titre
        self.alignement = alignement
        self.colonnes = []
        self.taille_colonnes = []
        self.lignes = []

    def __repr__(self):
        titre = self.titre or "sans titre"
        return "<Tableau {} avec {} colonnes et {} lignes>".format(
                repr(titre), len(self.colonnes), len(self.lignes))

    def __str__(self):
        """Retourne le tableau ASCII."""
        return self.afficher()

    def ajouter_colonne(self, nom, alignement=GAUCHE):
        """Ajoute une colonne.

        Les paramètres à préciser sont :
            nom -- le nom de la colonne
            alignement (optionnel) -- l'alignement de la colonne

        """
        if self.lignes:
            raise ValueError("Ce tableau contient déjà des lignes")

        self.colonnes.append((nom, alignement))
        self.taille_colonnes.append(len(supprimer_couleurs(nom)))

    def ajouter_ligne(self, *colonnes):
        """Ajoute une ligne.

        Le nombre d'argument doit correspondre au nombre de
        colonnes et respecter l'ordre de chacune.

        """
        if len(colonnes) != len(self.colonnes):
            raise ValueError("le nombre de colonnes spécifié est invalide")

        colonnes = tuple(str(d) for d in colonnes)
        self.lignes.append(colonnes)

    def afficher(self):
        """Affiche le tableau en format ASCII."""
        # On cherche d'abord à savoir la taille maximum des colonnes
        taille_colonnes = self.taille_colonnes
        for i, colonne in enumerate(self.colonnes):
            nom = colonne[0]
            for ligne in self.lignes:
                donnee = ligne[i]
                sc_donnee = supprimer_couleurs(donnee)
                if len(sc_donnee) > taille_colonnes[i]:
                    taille_colonnes[i] = len(sc_donnee)

        a_largeur = largeur = self.calculer_largeur()
        while largeur > 75:
            # Le tableau est trop large, on wrap certaines colonnes
            self.wrap_tableau()
            largeur = self.calculer_largeur()
            if a_largeur == largeur:
                raise ValueError("Il y a trop de colonnes")

        cadre = ""
        titre = ""
        for i, taille in enumerate(taille_colonnes):
            cadre += "-+-"
            titre += " | "
            cadre += "-" * taille
            nom, alignement = self.colonnes[i]
            nom = self.aligner(nom, taille, alignement)
            titre += nom
        cadre = cadre.lstrip("-") + "-+"
        titre = titre.lstrip(" ") + " |"

        if self.titre:
            cadre_complet = "+-" + "-" * (largeur - 4) + "-+"
            titre_tableau = "| " + self.aligner(self.titre, largeur - 4,
                    self.alignement) + " |"
            msg = "\n".join((cadre_complet, titre_tableau, cadre)) + "\n"
        else:
            msg = cadre + "\n"

        msg += "\n".join((titre, cadre))
        for i, ligne in enumerate(self.lignes):
            cellules = []
            for j, colonne in enumerate(self.colonnes):
                cellule = self.wrap_cellule(i, j)
                cellules.append(cellule)

            nb_lignes = max(len(lignes) for lignes in cellules)
            for k in range(nb_lignes):
                str_ligne = ""
                for j, lignes in enumerate(cellules):
                    try:
                        cellule = lignes[k]
                    except IndexError:
                        cellule = " " * taille_colonnes[j]

                    str_ligne += " | " + cellule
                str_ligne = str_ligne.lstrip(" ") + " |"
                msg += "\n" + str_ligne

        msg += "\n" + cadre
        return msg

    def wrap_tableau(self):
        """Wrap les colonnes du tableau."""
        largeur = self.calculer_largeur()
        while largeur > 75:
            self.wrap_large_colonne()
            largeur = self.calculer_largeur()

        return self.calculer_largeur()

    def calculer_largeur(self):
        """Retourne la largeur maximum du tableau."""
        taille_colonnes = self.taille_colonnes
        return sum(taille_colonnes) + (len(self.colonnes) + 1) * 3 - 2

    def wrap_large_colonne(self):
        """Wrap la colonne la plus large."""
        taille_colonnes = self.taille_colonnes
        large = max(taille_colonnes)
        no_colonne = taille_colonnes.index(large)
        titre = self.colonnes[no_colonne][0]
        titre = supprimer_couleurs(titre)
        largeur = self.calculer_largeur()
        taille = large - largeur + 75
        if taille < len(titre):
            taille = len(titre)

        self.taille_colonnes[no_colonne] = taille

    def wrap_cellule(self, i, j):
        """Wrap une cellule du tableau.

        Les paramètres i et j indiquent respectivement la ligne et
        la colonne.

        """
        cellule = self.lignes[i][j]
        alignement = self.colonnes[j][1]
        taille_max = self.taille_colonnes[j]
        sc_cellule = supprimer_couleurs(cellule)
        if len(sc_cellule) <= taille_max:
            lignes = [cellule]
        else:
            lignes = wrap(cellule, taille_max)

        for i, ligne in enumerate(lignes):
            lignes[i] = self.aligner(ligne, taille_max, alignement)
            if contient_couleurs(ligne):
                lignes[i] = lignes[i] + "|ff|"

        return lignes

    @staticmethod
    def aligner(msg, taille, alignement):
        """Aligne le message."""
        sc_msg = supprimer_couleurs(msg)
        taille_msg = len(sc_msg)
        manque = taille - taille_msg
        if alignement == GAUCHE:
            return msg + " " * manque
        elif alignement == DROITE:
            return " " * manque + msg
        elif alignement == CENTRE:
            gauche = True
            while len(sc_msg) < taille:
                if gauche:
                    msg = msg + " "
                else:
                    msg = " " + msg
                sc_msg = supprimer_couleurs(msg)
                gauche = not gauche
            return msg
        else:
            raise ValueError("Alignement inconnu : {}".format(repr(
                    alignement)))

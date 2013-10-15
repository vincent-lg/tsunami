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


"""Fichier contenant la classe Chemin, détaillée plus bas."""

from collections import OrderedDict

from abstraits.obase import BaseObj

# Constantes
FLAGS = {
    "circulaire": 1,
    "ne peut pas être pris à l'envers": 2,
}

class CheminPNJ(BaseObj):

    """Classe représentant un chemin de PNJ.

    Les chemins de PNJ sont une suite de salles et sorties que doit
    emprunter un PNJ pour se rendre d'un point A à un point B. Le chemin
    peut être circulaire, dans ce cas, le PNJ recommence le chemin
    quand il arrive au bout (la salle d'arrivée doit être identique
    à la salle de départ).

    """

    enregistrer = True
    def __init__(self, cle):
        """Constructeur du chemin."""
        BaseObj.__init__(self)
        self.cle = cle
        self.salles = OrderedDict()
        self.salles_retour = OrderedDict()
        self.flags = 0
        self._construire()

    def __getnewargs__(self):
        return ("inconnu", )

    def __repr__(self):
        """Affichage du chemin."""
        return "chemin {}".format(self.cle)

    def __len__(self):
        return len(self.salles)

    @property
    def salles_liste(self):
        return list(self.salles.keys())

    @property
    def origine(self):
        return self.salles and self.salles_liste[0] or None

    @property
    def destination(self):
        return self.salles and self.salles_liste[-1] or None

    def a_flag(self, nom_flag):
        """Retourne True si l'affection a le flag, False sinon."""
        valeur = FLAGS[nom_flag]
        return self.flags & valeur != 0

    def changer_flag(self, nom_flag):
        """Change la valeur du flag spécifié en paramètres."""
        self.flags = self.flags ^ FLAGS[nom_flag]

    def creer_point_depart(self, salle):
        """Crée le point de départ.

        Si des salles existent déjà dans self.salles, lève une exception
        ValueError.

        """
        if len(self.salles) > 0:
            raise ValueError("Ce chemin contient déjà des salles")

        self.salles[salle] = ""
        self.salles_retour[salle] = ""

    def ajouter_salle(self, direction):
        """Ajoute une nouvelle salle à la fin du chemin."""
        if len(self.salles) == 0:
            raise ValueError("Aucune salle dans ce chemin")

        derniere = self.destination

        # On recherche la sortie
        sortie = derniere.sorties.get(direction)
        if sortie is None or sortie.salle_dest is None:
            raise ValueError("La sortie {} n'existe pas dans la salle " \
                    "{}".format(nom, derniere))

        self.salles[derniere] = direction
        self.salles[sortie.salle_dest] = ""

        # Ajoute la sortie contraire
        if sortie.correspondante:
            self.salles_retour[sortie.salle_dest] = sortie.correspondante
            for t_salle in list(self.salles_retour.keys()):
                if t_salle is not sortie.salle_dest:
                    self.salles_retour.move_to_end(t_salle)

    def supprimer_salle(self, salle):
        """Supprime la salle spécifiée et les suivantes."""
        trouve = False
        for t_salle, nom_direction in tuple(self.salles.items()):
            if t_salle is salle:
                trouve = True

            if nom_direction and t_salle.sorties.get(
                    nom_direction).salle_dest is salle:
                self.salles[t_salle] = ""
            elif trouve:
                del self.salles[t_salle]

        # Chemin retour
        trouve = False
        for t_salle, nom_direction in tuple(
                self.salles_retour.items()):
            if nom_direction and t_salle.sorties.get(
                    nom_direction).salle_dest is t_salle:
                self.salles_retour[t_salle] = ""
            elif not trouve:
                del self.salles_retour[t_salle]

            if t_salle is salle:
                trouve = True

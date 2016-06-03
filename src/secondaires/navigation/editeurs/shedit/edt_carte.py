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


"""Fichier contenant l'éditeur EdtCarte."""

from primaires.interpreteur.editeur import Editeur
from primaires.interpreteur.editeur.env_objet import EnveloppeObjet
from .edt_salle import EdtSalle

class EdtCarte(Editeur):

    """Classe définissant l'éditeur edt_carte."""

    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.niveau = 0
        self.ajouter_option("m", self.opt_ajouter_milieu)
        self.ajouter_option("d", self.opt_supprimer_salle)
        self.ajouter_option("bab", self.opt_ajouter_babord)
        self.ajouter_option("tri", self.opt_ajouter_tribord)
        self.ajouter_option("ava", self.opt_ajouter_avant)
        self.ajouter_option("arr", self.opt_ajouter_arriere)
        self.ajouter_option("bas", self.opt_ajouter_bas)
        self.ajouter_option("hau", self.opt_ajouter_haut)
        self.ajouter_option("-", self.opt_niveau_moins)
        self.ajouter_option("+", self.opt_niveau_sup)

    def opt_ajouter_milieu(self, arguments):
        """Ajoute d'une salle au milieu du navire."""
        modele = self.objet
        if "0.0.0" in modele.salles:
            self.pere << "|err|Une salle au milieu du navire est déjà " \
                    "définie.|ff|"
        else:
            modele.ajouter_salle(0, 0, 0, "1")
            self.actualiser()

    def opt_supprimer_salle(self, arguments):
        """Supprime une salle.

        Syntaxe :
            /d mnémonique

        """
        modele = self.objet
        if modele.get_salle(arguments) is None:
            self.pere << "|err|Le mnémonique {} est introuvable.|ff|".format(
                    arguments)
        else:
            modele.supprimer_salle(arguments)
            self.actualiser()

    def opt_ajouter_babord(self, arguments):
        """Ajoute une salle à bâbord.

        Syntaxe :
            /bab <mnémonique>

        """
        modele = self.objet
        try:
            coords, salle = modele.get_salle(arguments)
        except ValueError:
            self.pere << "|err|Ce mnémonique n'existe pas.|ff|"
        else:
            coords = (coords[0] - 1, coords[1], coords[2])
            try:
                salle_2 = modele.ajouter_salle(coords[0], coords[1], coords[2])
            except ValueError as err:
                self.pere << "|err|" + str(err).capitalize() + "|ff|"
            else:
                modele.lier_salle(salle, salle_2, "ouest")
                self.actualiser()

    def opt_ajouter_tribord(self, arguments):
        """Ajoute une salle à tribord.

        Syntaxe :
            /tri <mnémonique>

        """
        modele = self.objet
        try:
            coords, salle = modele.get_salle(arguments)
        except ValueError:
            self.pere << "|err|Ce mnémonique n'existe pas.|ff|"
        else:
            coords = (coords[0] + 1, coords[1], coords[2])
            try:
                salle_2 = modele.ajouter_salle(coords[0], coords[1], coords[2])
            except ValueError as err:
                self.pere << "|err|" + str(err).capitalize() + "|ff|"
            else:
                modele.lier_salle(salle, salle_2, "est")
                self.actualiser()

    def opt_ajouter_avant(self, arguments):
        """Ajoute une salle à l'avant.

        Syntaxe :
            /ava <mnémonique>

        """
        modele = self.objet
        try:
            coords, salle = modele.get_salle(arguments)
        except ValueError:
            self.pere << "|err|Ce mnémonique n'existe pas.|ff|"
        else:
            coords = (coords[0], coords[1] + 1, coords[2])
            try:
                salle_2 = modele.ajouter_salle(coords[0], coords[1], coords[2])
            except ValueError as err:
                self.pere << "|err|" + str(err).capitalize() + "|ff|"
            else:
                modele.lier_salle(salle, salle_2, "nord")
                self.actualiser()

    def opt_ajouter_arriere(self, arguments):
        """Ajoute une salle à l'arrière.

        Syntaxe :
            /tri <mnémonique>

        """
        modele = self.objet
        try:
            coords, salle = modele.get_salle(arguments)
        except ValueError:
            self.pere << "|err|Ce mnémonique n'existe pas.|ff|"
        else:
            coords = (coords[0], coords[1] - 1, coords[2])
            try:
                salle_2 = modele.ajouter_salle(coords[0], coords[1], coords[2])
            except ValueError as err:
                self.pere << "|err|" + str(err).capitalize() + "|ff|"
            else:
                modele.lier_salle(salle, salle_2, "sud")
                self.actualiser()

    def opt_ajouter_bas(self, arguments):
        """Ajoute une salle en bas.

        Syntaxe :
            /bas <mnémonique>

        """
        modele = self.objet
        try:
            coords, salle = modele.get_salle(arguments)
        except ValueError:
            self.pere << "|err|Ce mnémonique n'existe pas.|ff|"
        else:
            coords = (coords[0], coords[1], coords[2] - 1)
            try:
                salle_2 = modele.ajouter_salle(coords[0], coords[1], coords[2])
            except ValueError as err:
                self.pere << "|err|" + str(err).capitalize() + "|ff|"
            else:
                modele.lier_salle(salle, salle_2, "bas")
                self.actualiser()

    def opt_ajouter_haut(self, arguments):
        """Ajoute une salle en haut.

        Syntaxe :
            /hau <mnémonique>

        """
        modele = self.objet
        try:
            coords, salle = modele.get_salle(arguments)
        except ValueError:
            self.pere << "|err|Ce mnémonique n'existe pas.|ff|"
        else:
            coords = (coords[0], coords[1], coords[2] + 1)
            try:
                salle_2 = modele.ajouter_salle(coords[0], coords[1], coords[2])
            except ValueError as err:
                self.pere << "|err|" + str(err).capitalize() + "|ff|"
            else:
                modele.lier_salle(salle, salle_2, "haut")
                self.actualiser()

    def opt_niveau_sup(self, arguments):
        """Passe en niveau supérieur.

        Syntaxe :
            /+

        """
        self.niveau += 1
        self.actualiser()

    def opt_niveau_moins(self, arguments):
        """Passe en niveau inférieur.

        Syntaxe :
            /-

        """
        self.niveau -= 1
        self.actualiser()

    def accueil(self):
        """Affichage de la carte du navire."""
        modele = self.objet
        coordonnees = modele.coordonnees_salles
        msg = " |tit| Carte du modèle de navire {} en niveau {}|ff|" \
                "\n\n".format(modele.cle, self.niveau)
        if coordonnees:
            # On cherche la coordonnée d'extrême ouest / est
            ouest_est = [c[0] for c in coordonnees]
            sud_nord = [c[1] for c in coordonnees]
            bas_haut = [c[2] for c in coordonnees]
            ouest = min(ouest_est)
            est = max(ouest_est)
            sud = min(sud_nord)
            nord = max(sud_nord)
            bas = min(bas_haut)
            haut = max(bas_haut)
            niveau = self.niveau
            for i in range(nord, sud - 1, -1):
                for j in range(ouest, est + 1):
                    t_coords = (j, i, niveau)
                    salle = modele.salles.get(t_coords)
                    if salle:
                        msg += salle.mnemonic.rjust(3)
                    else:
                        msg += "   "
                msg += "\n"
            msg = msg[:-1]
        else:
            msg += "|att|Aucune salle n'est définie pour l'instant.|ff|"

        return msg

    def interpreter(self, msg):
        """Interprétation du message."""
        modele = self.objet
        try:
            coords, salle = modele.get_salle(msg)
        except ValueError:
            self.pere << "|err|Ce mnémonique n'existe pas.|ff|"
        else:
            enveloppe = EnveloppeObjet(EdtSalle, salle)
            enveloppe.parent = self
            contexte = enveloppe.construire(self.pere.joueur)

            self.migrer_contexte(contexte)

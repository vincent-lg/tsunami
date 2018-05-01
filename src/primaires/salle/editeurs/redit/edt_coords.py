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


"""Fichier contenant le contexte éditeur EdtCoords"""

import re

from primaires.interpreteur.editeur.uniligne import Uniligne

# Constantes
COORDS_VALIDE = r"^-?[0-9]+\.-?[0-9]+\.-?[0-9]+$"

class EdtCoords(Uniligne):

    """Classe définissant le contexte éditeur 'coords'.

    Ce contexte permet d'éditer les coordonnées de la salle.

    """

    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Uniligne.__init__(self, pere, objet, attribut)
        self.ajouter_option("s", self.opt_sud)
        self.ajouter_option("so", self.opt_sudouest)
        self.ajouter_option("o", self.opt_ouest)
        self.ajouter_option("no", self.opt_nordouest)
        self.ajouter_option("n", self.opt_nord)
        self.ajouter_option("ne", self.opt_nordest)
        self.ajouter_option("e", self.opt_est)
        self.ajouter_option("se", self.opt_sudest)
        self.ajouter_option("b", self.opt_bas)
        self.ajouter_option("h", self.opt_haut)

    def opt_sud(self, arguments):
        """Change les coordonnées de la salle en la déplaçant vers le sud"""
        self.changer_coordonnees(self.objet.coords.sud.tuple())

    def opt_sudouest(self, arguments):
        """Change les coordonnées de la salle en la déplaçant vers le sud-ouest"""
        self.changer_coordonnees(self.objet.coords.sudouest.tuple())

    def opt_ouest(self, arguments):
        """Change les coordonnées de la salle en la déplaçant vers l'ouest"""
        self.changer_coordonnees(self.objet.coords.ouest.tuple())

    def opt_nordouest(self, arguments):
        """Change les coordonnées de la salle en la déplaçant vers le
        nord-ouest

        """
        self.changer_coordonnees(self.objet.coords.nordouest.tuple())

    def opt_nord(self, arguments):
        """Change les coordonnées de la salle en la déplaçant vers le nord"""
        self.changer_coordonnees(self.objet.coords.nord.tuple())

    def opt_nordest(self, arguments):
        """Change les coordonnées de la salle en la déplaçant vers le
        nord-est

        """
        self.changer_coordonnees(self.objet.coords.nordest.tuple())

    def opt_est(self, arguments):
        """Change les coordonnées de la salle en la déplaçant vers l'est"""
        self.changer_coordonnees(self.objet.coords.est.tuple())

    def opt_sudest(self, arguments):
        """Change les coordonnées de la salle en la déplaçant vers le
        sud-est

        """
        self.changer_coordonnees(self.objet.coords.sudest.tuple())

    def opt_bas(self, arguments):
        """Change les coordonnées de la salle en la déplaçant vers le bas"""
        self.changer_coordonnees(self.objet.coords.bas.tuple())

    def opt_haut(self, arguments):
        """Change les coordonnées de la salle en la déplaçant vers le haut"""
        self.changer_coordonnees(self.objet.coords.haut.tuple())

    def changer_coordonnees(self, tuple):
        """Change les coordonnées de la salle."""
        if tuple in type(self).importeur.salle:
            self.pere.envoyer("|err|Ces coordonnées sont déjà " \
                    "utilisées dans l'univers.|ff|")
        else:
            x, y, z = tuple
            self.objet.coords.x = x
            self.objet.coords.y = y
            self.objet.coords.z = z
            self.objet.coords.valide = True
            self.actualiser()

    def interpreter(self, msg):
        """Interprétation du message"""
        msg = msg.lower()
        if msg == "inv":
            self.objet.coords.valide = False
            self.actualiser()
        elif not re.search(COORDS_VALIDE, msg):
            self.pere.envoyer("|err|Ces coordonnées sont invalides. " \
                    "Veuillez réessayer.|ff|")
        else:
            # On va découper msg
            # Grâce aux regex, on est sûr d'avoir le bon format
            x, y, z = msg.split(".")
            try:
                x, y, z = int(x), int(y), int(z)
            except ValueError:
                self.pere.envoyer("|err|Ces coordonnées sont invalides. " \
                    "Veuillez réessayer.|ff|")
            else:
                self.changer_coordonnees((x, y, z))

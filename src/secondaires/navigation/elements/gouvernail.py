# -*-coding:Utf-8 -*

# Copyright (c) 2010 LE GOFF Vincent
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


"""Fichier contenant la classe Gouvernail, détaillée plus bas."""

from bases.objet.attribut import Attribut
from .base import BaseElement

class Gouvernail(BaseElement):

    """Classe représentant un gouvernail.

    """

    nom_type = "gouvernail"

    def __init__(self, cle=""):
        """Constructeur d'un type"""
        BaseElement.__init__(self, cle)
        # Attributs propres aux gouvernails
        self._attributs = {
            "orientation": Attribut(lambda: 0),
            "tenu": Attribut(lambda: None),
        }

    def get_description_ligne(self, personnage):
        """Retourne la description en une ligne de l'élément."""
        if self.orientation == 0:
            orientation = "parfaitement au centre"
        elif self.orientation < 0:
            orientation = "incliné de {nb}° sur bâbord".format(
                    nb=-self.orientation)
        else:
            orientation = "incliné de {nb}° sur tribord".format(
                    nb=self.orientation)

        return self.nom.capitalize() + " est " + orientation + "."

    def tenir(self, personnage):
        """Méthode demandant au personnage de tenir le gouvernail."""
        self.tenu = personnage
        personnage.etats.ajouter("tenir_gouvernail")
        personnage << "Vous empoignez fermement {}.".format(
                self.nom.lower())
        personnage.salle.envoyer("{{}} empoigne fermement {}.".format(
                self.nom.lower()), personnage)

    def relacher(self, personnage):
        """Méthode demandant au personnage de relâcher le gouvernail."""
        self.tenu = None
        if "tenir_gouvernail" in personnage.etats:
            personnage.etats.retirer("tenir_gouvernail")
        personnage << "Vous relâchez {}.".format(
                self.nom.lower())
        personnage.salle.envoyer("{{}} relâche {}.".format(
                self.nom.lower()), personnage)

    def virer_babord(self, personnage, nombre=1, zero=False):
        """Vire vers bâbord."""
        ancienne = self.orientation
        if zero:
            self.orientation = 0
        self.orientation -= nombre
        if self.orientation < -5:
            self.orientation = -5
        self.afficher_orientation(personnage, ancienne)

    def virer_tribord(self, personnage, nombre=1, zero=False):
        """Vire vers tribord."""
        ancienne = self.orientation
        if zero:
            self.orientation = 0
        self.orientation += nombre
        self.afficher_orientation(personnage, ancienne)

    def centrer(self, personnage):
        """Centre le gouvernail."""
        ancienne = self.orientation
        self.orientation = 0
        if ancienne != 0:
            self.afficher_orientation(personnage, ancienne)

    def afficher_orientation(self, personnage, ancienne=0):
        """Affiche le changement d'orientation."""
        orientation = self.orientation
        diff = (orientation + ancienne) % 5
        if self.orientation < 0:
            diff = 5 - diff

        if diff == 1:
            adverbe = "presque insensiblement"
        elif diff == 2:
            adverbe = "légèrement"
        elif diff == 3:
            adverbe = "assez fortement"
        elif diff == 4:
            adverbe = "fortement"
        else:
            adverbe = "très fortement"
        if orientation == 0:
            msg = "{sujet} redresse{z} le gouvernail."
        elif orientation < 0:
            if orientation < ancienne:
                msg = "{sujet} incline{z} {adverbe} le gouvernail " \
                        "sur bâbord."
            else:
                msg = "{sujet} redresse{z} {adverbe} le gouvernail."
        else:
            if orientation > ancienne:
                msg = "{sujet} incline{z} {adverbe} le gouvernail " \
                        "sur tribord."
            else:
                msg = "{sujet} redresse{z} {adverbe} le gouvernail."

        personnage.envoyer(msg.format(sujet="Vous", z="z", adverbe=adverbe))
        personnage.salle.envoyer(msg.format(sujet="{}", z="",
                adverbe=adverbe), personnage)

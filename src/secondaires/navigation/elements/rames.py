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


"""Fichier contenant la classe Rames, détaillée plus bas."""

from bases.objet.attribut import Attribut
from .base import BaseElement

class Rames(BaseElement):

    """Classe représentant une paire de rames.

    """

    nom_type = "rames"

    def __init__(self, cle=""):
        """Constructeur d'un type"""
        BaseElement.__init__(self, cle)
        # Attributs propres aux ramess
        self._attributs = {
            "vitesse": Attribut(lambda: "immobile"),
            "orientation": Attribut(lambda: 0),
            "tenu": Attribut(lambda: None),
        }

    def get_description_ligne(self, personnage):
        """Retourne la description en une ligne de l'élément."""
        return self.nom.capitalize() + " se trouve là."

    def centrer(self):
        """Centre les rames."""
        ancienne = self.orientation
        self.orientation = 0
        if self.tenu and ancienne != 0:
            personnage = self.tenu
            personnage << "Vous arrêtez de tourner en centrant les rames."
            personnage.salle.envoyer("{} arrête de tourner en centrant " \
                    "les rames", personnage)

    def virer_tribord(self):
        """Vire à tribord."""
        self.orientation = 1
        if self.tenu:
            personnage = self.tenu
            personnage << "Vous commencez de ramez en tournant vers " \
                    "tribord."
            personnage.salle.envoyer("{} commence à ramer vers tribord.",
                    personnage)

    def virer_babord(self):
        """Vire à bâbord."""
        self.orientation = -1
        if self.tenu:
            personnage = self.tenu
            personnage << "Vous commencez de ramez en tournant vers " \
                    "bâbord."
            personnage.salle.envoyer("{} commence à ramer vers bâbord.",
                    personnage)

    def tenir(self, personnage):
        """Empoigne les rames."""
        if self.tenu:
            raise ValueError("Ces rames sont déjà tenues")

        if self.parent is not personnage.salle:
            raise ValueError("Le personnage {} n'est pas en {}".format(
                    personnage, self.parent))

        self.tenu = personnage
        personnage.etats.ajouter("tenir_rames")
        personnage << "Vous empoignez {}.".format(
                self.nom)
        personnage.salle.envoyer("{{}} empoigne {}.".format(
                self.nom), personnage)

    def relacher(self):
        """Relâche les rames."""
        if self.tenu is None:
            raise ValueError("Ces rames ne sont pas tenues")

        personnage = self.tenu
        salle = self.parent
        if self.vitesse != "immobile":
            self.vitesse = "immobile"
            personnage << "Vous arrêtez de ramer."
            salle.envoyer("{} arrête de ramer.", personnage)
        self.centrer()
        self.tenu = None
        personnage.etats.retirer("tenir_rames")

        personnage << "Vous lâchez {}.".format(
                self.nom)
        personnage.salle.envoyer("{{}} lâche {}.".format(
                self.nom), personnage)

    def changer_vitesse(self, n_vitesse):
        """Change la vitesse des rames."""
        if self.tenu is None:
            raise ValueError("Personne ne tient ces rames")

        personnage = self.tenu
        salle = self.parent
        vitesse = self.vitesse
        if vitesse == n_vitesse:
            personnage << "|err|Vous ramez déjà à cette vitesse.|ff|"
            return

        self.vitesse = n_vitesse
        msg = "Vous commencez de ramer {vitesse}."
        msg_autre = "{{personnage}} commence à ramer {vitesse}."
        msg_vit = ""
        if n_vitesse == "arrière":
            msg_vit = "en marche arrière"
        elif n_vitesse == "immobile":
            msg = "Vous arrêtez de ramer."
            msg_autre = "{{personnage}} arrête de ramer."
        elif n_vitesse == "lente":
            msg_vit = "à faible vitesse"
        elif n_vitesse == "moyenne":
            msg_vit = "à vitesse moyenne"
        elif n_vitesse == "rapide":
            msg_vit = "rapidement"
        else:
            raise RuntimeError("vitesse non traitée {}".format(n_vitesse))

        msg = msg.format(vitesse=msg_vit)
        msg_autre = msg_autre.format(vitesse=msg_vit)
        personnage << msg
        salle.envoyer(msg_autre, personnage=personnage)

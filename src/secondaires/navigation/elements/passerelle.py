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


"""Fichier contenant la classe Passerelle, détaillée plus bas."""

from math import sqrt

from bases.objet.attribut import Attribut
from primaires.salle.sorties import NOMS_OPPOSES
from primaires.vehicule.vecteur import Vecteur
from secondaires.navigation.constantes import *
from .base import BaseElement

class Passerelle(BaseElement):

    """Classe représentant une passerelle.

    """

    nom_type = "passerelle"

    def __init__(self, cle=""):
        """Constructeur d'un type"""
        BaseElement.__init__(self, cle)
        # Attributs propres aux passerelles
        self._attributs = {
            "baissee": Attribut(lambda: False),
        }

    @property
    def baissee_vers(self):
        """Retourne la salle vers laquelle la passerelle est dépliée."""
        if not self.baissee:
            return None

        return self.parent.sorties.get_sortie_par_nom(
                "passerelle").salle_dest

    def get_description_ligne(self, personnage):
        """Retourne une description d'une ligne de l'élément."""
        if self.baissee:
            message = "dépliée ici"
        else:
            message = "repliée ici"

        return self.nom.capitalize() + " est " + message + "."

    def deplier(self, personnage=None):
        """Déplie la passerelle (si possible).

        Retourne True si la passerelle a pu être dépliée, False sinon.

        """
        salle = self.parent
        navire = salle.navire
        etendue = navire.etendue
        position = Vecteur(*salle.coords.tuple())
        x, y, z = salle.coords.tuple()
        distance = 10
        dest = None
        # Cherche la salle la plus proche
        for t_salle in etendue.cotes.values():
            if t_salle.coords.z == etendue.altitude and \
                    t_salle.nom_terrain in TERRAINS_QUAI:
                t_x, t_y, t_z = t_salle.coords.tuple()
                t_distance = sqrt((x - t_x) ** 2 + (y - t_y) ** 2)
                if t_distance < distance:
                    dest = t_salle
                    distance = t_distance

        if dest is None or distance > 2.5:
            return False

        try:
            ts_sortie = dest.sorties.get_sortie_par_nom("passerelle")
        except KeyError:
            ts_sortie = None

        if ts_sortie is not None:
            return False

        # On cherche la meilleure sortie
        sorties = ["est", "sud", "ouest", "nord", "sud-est",
                "sud-ouest", "nord-ouest", "nord-est"]

        dir = None
        for nom in sorties:
            oppose = NOMS_OPPOSES[nom]
            if salle.sorties[nom] is None and dest.sorties[oppose] is None:
                dir = nom
                break

        if dir is None:
            return False

        salle.sorties.ajouter_sortie(dir, "passerelle", "la", dest, oppose)
        dest.sorties.ajouter_sortie(oppose, "passerelle", "la", salle, dir)
        self.baissee = True
        if personnage:
            personnage << "Vous déployez {}.".format(self.nom)
        return True

    def replier(self):
        """Replie la passerelle."""
        if self.baissee:
            salle = self.parent
            # On cherche la sortie
            sortie = salle.sorties.get_sortie_par_nom("passerelle")
            dest = sortie.salle_dest
            opp_sortie = None
            for nom, t_sortie in dest.sorties.iter_couple():
                if t_sortie.salle_dest is salle:
                    opp_sortie = t_sortie
                    break

            if opp_sortie:
                dest.sorties.supprimer_sortie(opp_sortie.direction)

            salle.sorties.supprimer_sortie(sortie.direction)
            self.baissee = False

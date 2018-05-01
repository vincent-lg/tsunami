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


"""Package contenant la commande 'point'."""

from primaires.interpreteur.commande.commande import Commande
from primaires.vehicule.vecteur import get_direction
from secondaires.navigation.constantes import get_longitude_latitude

class CmdPoint(Commande):

    """Commande 'point'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "point", "bearing")
        self.nom_categorie = "navire"
        self.aide_courte = "fait le point"
        self.aide_longue = \
            "Cette commande permet de faire le point sur un navire. " \
            "Vous aurez besoin d'avoir un sextant équipé. Faire le " \
            "point prend un peu de temps, nécessite un ciel dégagé de " \
            "nuages et est affecté par la qualité des instruments " \
            "utilisés."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        personnage.agir("fairepoint")
        salle = personnage.salle
        if not hasattr(salle, "navire") or salle.navire is None or \
                salle.navire.etendue is None:
            personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
            return

        navire = salle.navire
        sextant = None
        for objet in personnage.equipement.equipes:
            if objet.est_de_type("sextant"):
                sextant = objet
                break

        if not sextant:
            personnage << "|err|Vous n'avez pas de sextant équipé.|ff|"
            return

        if salle.interieur:
            personnage << "|err|Vous ne pouvez faire le point d'ici.|ff|"
            return
        else:
            perturbation = importeur.meteo.get_perturbation(salle)
            if perturbation is not None and perturbation.est_opaque():
                personnage << "|err|Vous ne voyez pas le ciel.|ff|"
                return

        personnage << "Vous étudiez le ciel en utilisant {}.".format(
                sextant.get_nom())
        personnage.salle.envoyer("{{}} étudie le ciel grâce à {}.".format(
                sextant.get_nom()), personnage)
        personnage.etats.ajouter("faire_point")
        yield sextant.calcul
        if "faire_point" not in personnage.etats:
            return

        personnage.etats.retirer("faire_point")
        x = salle.coords.x
        y = salle.coords.y
        personnage << "Après calcul, vous obtenez " + get_longitude_latitude(
                x, y, sextant.precision) + "."
        personnage.salle.envoyer("{{}} baisse {}".format(sextant.get_nom()),
                personnage)

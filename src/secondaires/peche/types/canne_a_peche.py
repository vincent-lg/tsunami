# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Fichier contenant le type CanneAPeche."""

from primaires.interpreteur.editeur.entier import Entier
from bases.objet.attribut import Attribut
from primaires.objet.types.base import BaseType

class CanneAPeche(BaseType):

    """Type d'objet: canne à pêche.

    """

    nom_type = "canne à pêche"
    empilable_sur = ["vêtement"]

    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        BaseType.__init__(self, cle)
        self.emplacement = "mains"
        self.positions = (1, 2)
        self.tension_max = 10
        self.etendre_editeur("te", "tension maximum", Entier, self,
                "tension_max", 1)

        self._attributs = {
            "appat": Attribut(),
        }

    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes"""
        tension = enveloppes["te"]
        tension.apercu = "{objet.tension_max} Kg"
        tension.prompt = "Tension maximum de la canne (en Kg) : "
        tension.aide_courte = \
            "Entrez la |ent|tension maximum|ff| de la canne ou |cmd|/|ff| " \
            "pour revenir à la fenêtre parente.\n\n" \
            "La tension maximum défini le plus lourd poisson " \
            "pouvant être pêché. Si\n" \
            "un poisson plus lourd se porte sur la canne, celle-ci " \
            "se brisera.\n\n" \
            "Tension actuelle : {objet.tension_max}"

    def objets_contenus(self, conteneur):
        """Retourne les objets contenus."""
        objets = []
        if conteneur.appat:
            objet = conteneur.appat
            objets.append(objet)
            if objet.unique:
                objets.extend(objet.prototype.objets_contenus(objet))

        return objets

    def detruire_objet(self, conteneur):
        """Détruit l'objet passé en paramètre.

        On va détruire tout ce qu'il contient.

        """
        if conteneur.appat:
            objet = conteneur.appat
            if objet.unique and objet.e_existe:
                importeur.objet.essayer_supprimer_objet(objet)

    # Actions sur les objets
    def regarder(self, personnage):
        """Le personnage regarde l'objet"""
        msg = BaseType.regarder(self, personnage)
        msg += "\n\n"
        if getattr(self, "appat", None):
            msg += "La ligne est appâtée avec {}.".format(self.appat.get_nom())
        else:
            msg += "La ligne n'est pas appâtée."

        return msg

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


"""Fichier contenant le masque <observable>."""

import re

from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation
from primaires.format.fonctions import contient, supprimer_accents

# Constantes
RE_NB = re.compile(r"^([0-9]+)\.")

class Observable(Masque):

    """Masque <observable>.

    On attend le fragment d'un nom observable, un joueur, un objet, un
    détail...

    """

    nom = "element_observable"
    nom_complet = "élément observable"

    def init(self):
        """Initialisation des attributs"""
        self.element = ""
        self.nombre = 1

    def repartir(self, personnage, masques, commande):
        """Répartition du masque."""
        lstrip(commande)
        nom = liste_vers_chaine(commande)

        re_nb = RE_NB.search(nom)
        if re_nb:
            nb = re_nb.groups()[0]
            nom = nom[len(nb) + 1:]
            try:
                nb = int(nb)
                assert nb > 0
            except (ValueError, AssertionError):
                    raise ErreurValidation( \
                    "Ce nombre est invalide.", False)
            else:
                self.nombre = nb

        if not nom:
            raise ErreurValidation( \
                "Précisez un élément observable.", False)

        commande[:] = []
        self.a_interpreter = nom
        masques.append(self)
        return True

    def valider(self, personnage, dic_masques):
        """Validation du masque"""
        Masque.valider(self, personnage, dic_masques)
        nom = self.a_interpreter
        nombre = self.nombre
        nb = 0

        salle = personnage.salle
        if not salle.voit_ici(personnage):
            raise ErreurValidation(
                "Il n'y a rien qui ressemble à cela par ici...", True)

        elt = None

        # On cherche dans les personnages
        for perso in salle.personnages:
            if personnage.peut_voir(perso) and \
                    contient(perso.get_nom_pour(personnage), nom):
                nb += 1
                if nb == nombre:
                    elt = perso
                    break

        if elt is None:
            for objet in personnage.equipement.inventaire:
                if contient(objet.get_nom(), nom):
                    nb += 1
                    if nb == nombre:
                        elt = objet
                        break

        if elt is None:
            # On cherche dans les décors
            for decor in salle.decors:
                nom_decor = decor.get_nom()
                if contient(nom_decor, nom):
                    nb += 1
                    if nb == nombre:
                        elt = decor

        if elt is None:
            # On cherche dans les objets
            for objet in salle.objets_sol:
                nom_objet = objet.get_nom()
                if contient(nom_objet, nom):
                    nb += 1
                    if nb == nombre:
                        elt = objet

        if not elt:
            # On cherche dans les autres éléments observables
            elts = salle.get_elements_observables(personnage)
            for t_elt in elts:
                nom_elt = t_elt.get_nom_pour(personnage)
                if contient(nom_elt, nom):
                    nb += 1
                    if nb == nombre:
                        elt = t_elt
                        break

        if not elt:
            nom = supprimer_accents(nom).lower()
            if salle.details.detail_existe(nom, flottants=True):
                detail = salle.details.get_detail(nom, flottants=True)
                nb += 1
                if nb == nombre:
                    elt = detail

        if elt is None:
            raise ErreurValidation(
                "Il n'y a rien qui ressemble à cela par ici...", True)

        self.element = elt
        return True

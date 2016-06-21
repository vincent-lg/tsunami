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


"""Fichier contenant la classe NavireAutomatique, détaillée plus bas."""

from random import choice, randint

from abstraits.obase import BaseObj

class NavireAutomatique(BaseObj):

    """Classe représentant une fiche de navire automatique.

    Un navire automatique est un navire créé par le système et
    manoeuvré par un équipage de PNJ. Cette fiche ne contient que
    les informations de création qui sont par exemple le type de navire
    à créer (modèle), les noms possibles du navire, la constitution
    de son équipage, ses réserves de cale, etc. Après la crréation
    d'un navire automatique, l'équipage PNJ se charge du navire
    (c'est-à-dire le fait d'avancer, attaquer, se défendre...). En
    somme, un navire automatique est un raccourci pour créer rapidement
    un navire contrôlé par des PNJ sans avoir à faire toutes les étapes
    intermédiaires, mais ce que l'équipage d'un navire automatique
    peut faire, un navire contrôlé par un joueur ou par un PNJ peut
    le faire également.

    """

    enregistrer = True

    def __init__(self, cle):
        BaseObj.__init__(self)
        self.cle = cle
        self.modele = None
        self.equipage = {} # {poste: (prototype, salle, nb_min, nb_max)}
        self.noms = []
        self.cale = {} # {cle_objet: (nb_min, nb_max)}
        self.trajets = []
        self.pavillon = None
        self._construire()

    def __getnewargs__(self):
        return ("inconnu", )

    def __repr__(self):
        return "<NavireAutomatique {}>".format(repr(self.cle))

    def __str__(self):
        return self.cle

    def creer(self):
        """Crée un navire automatique en se basant sur le modèle.

        Cette méthode retourne le navire (type Navire) créé. Le nom
        personnalisé, l'équipage, la cale et le trajet sont également
        paramétrés en fonction des informations plus ou moins aléatoires
        de la fiche.

        """
        if self.modele is None:
            raise ValueError("Aucun modèle de navire configuré pour " \
                    "la fiche {}".format(self.cle))

        navire = importeur.navigation.creer_navire(self.modele)

        # On change le nom personnalisé
        if self.noms:
            navire.nom_personnalise = choice(self.noms)

        # Création de l'équipage
        for nom_poste, (cle, coords, nb_min, nb_max) in self.equipage.items():
            fiche = importeur.navigation.fiches.get(cle)
            if fiche is None:
                raise ValueError("Impossible de trouver le prototype " \
                        "de PNJ {} pour le navire automatique {}".format(
                        repr(cle), repr(self.cle)))

            # On cherche la salle où fait apparaître les matelots
            salle = navire.salles.get(coords)
            if salle is None:
                raise ValueError("La salle {} pour faire apparaître " \
                        "{} est introuvable".format(coords, repr(cle)))

            if nb_min != nb_max:
                nb = randint(nb_min, nb_max)
            else:
                nb = nb_min

            if nb > 0:
                pnjs = fiche.creer_PNJ(salle, nb)

                for pnj in pnjs:
                    matelot = navire.equipage.ajouter_matelot(pnj)
                    matelot.nom_poste = nom_poste

        # Ajout d'objets dans la cale
        for cle, (nb_min, nb_max) in self.cale.items():
            prototype = importeur.objet.prototypes.get(cle)
            if prototype is None:
                raise ValueError("Le prototype d'objet {} pour la " \
                        "cale du navire automatique {} ne peut être " \
                        "trouvé".format(repr(cle), repr(self.cle)))

            if not navire.cale.accepte(None, prototype.nom_type):
                raise ValueError("La cale n'accepte pas d'objet de " \
                        "type {}".format(repr(prototype.nom_type)))

            if nb_min != nb_max:
                nb = randint(nb_min, nb_max)
            else:
                nb = nb_min

            if nb > 0:
                navire.cale.ajouter_prototype_objet(prototype, nb)

        # Sélection aléatoire du trajet
        if self.trajets:
            trajet = choice(self.trajets)
            etendue = trajet.etendue
            x, y = trajet.point_depart
            z = etendue.altitude
            navire.etendue = etendue
            navire.position.x = x
            navire.position.y = y
            navire.position.z = z
            navire.maj_salles()
            navire.valider_coordonnees()
            navire.equipage.ajouter_trajet(trajet)

        if self.pavillon:
            navire.pavillon = self.pavillon

        return navire

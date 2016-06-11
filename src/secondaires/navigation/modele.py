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


"""Fichier contenant la classe ModeleNavire, détaillée plus bas."""

from queue import Queue

from abstraits.obase import BaseObj
from primaires.format.description import Description
from .salle import *

class ModeleNavire(BaseObj):

    """Classe représentant un modèle de navire ou une embarcation.

    Les modèles définissent des informations communes à plusieurs navires
    (une barque, par exemple, sera construite sur un seul modèle mais
    plusieurs navires seront formés sur ce modèle).

    """

    enregistrer = True
    def __init__(self, cle):
        """Constructeur du modèle."""
        BaseObj.__init__(self)
        self.cle = cle
        self.nom = "un navire"
        self.vehicules = []
        self.salles = {}
        self.poids_max = 200
        self.tirant_eau = 3
        self.fond_plat = False
        self.graph = {}
        self.m_valeur = 1000
        self.duree_construction = 60
        self.description = Description(parent=self)
        self.description_vente = Description(parent=self)
        self.masculin = True
        self.peut_conquerir = True
        self.niveau = 5
        self.cale_max = 200
        self.facteur_rames = 0.8
        self.facteurs_orientations = {
                "vent debout": -0.3,
                "au près": 0.5,
                "bon plein": 0.8,
                "largue": 1.2,
                "grand largue": 0.9,
                "vent arrière": 0.7,
        }
        self.descriptions_independantes = False
        self._construire()

    def __getnewargs__(self):
        return ("", )

    def __getstate__(self):
        """Enregistrement de l'objet.

        On ne peut pas enregistrer les salles telles qu'elles car
        MongoDB n'aime pas les dictionnaires contenant des tuples en
        clés.

        """
        attrs = BaseObj.__getstate__(self)
        salles = {}
        for cle, salle in attrs["salles"].items():
            salles["|".join([str(c) for c in cle])] = salle

        attrs["salles"] = salles
        return attrs

    def __setstate__(self, attrs):
        """Récupération de l'objet enregistré."""
        salles = {}
        for cle, salle in attrs["salles"].items():
            if isinstance(cle, str):
                x, y, z = cle.split("|")
                cle = int(x), int(y), int(z)
            salles[cle] = salle

        attrs["salles"] = salles
        BaseObj.__setstate__(self, attrs)

    def __repr__(self):
        return self.cle

    @property
    def coordonnees_salles(self):
        """Retourne un tuple des coorodnnées des salles."""
        return tuple(self.salles.keys())

    @property
    def mnemonics_salles(self):
        """Retourne un tuple des mnémoniques des salles."""
        return tuple(s.mnemonic for s in self.salles.values())

    @property
    def a_canot(self):
        """Le modèle de navire a-t-il un canot ?

        Le modèle de navire a un canot si il existe un objet de
        même clé que le modèle.

        """
        return self.cle in importeur.objet.prototypes

    @property
    def prototype_canot(self):
        """Retourne le prototype d'objet du canot ou None."""
        return importeur.objet.prototypes.get(self.cle)

    def get_max_distance_au_centre(self):
        """Retourne la distance maximum par rapport au centre du navire."""
        distances = []
        for x, y, z in self.salles.keys():
            distances.append(sqrt(x ** 2 + y ** 2 + z ** 2))

        return max(distances)

    def get_salle(self, mnemonic):
        """Retourne la salle ayant le mnémonique indiqué.

        Lève une exception ValueError si la salle n'est pas trouvée.

        """
        for coords, salle in self.salles.items():
            if salle.mnemonic == mnemonic:
                return coords, salle

        raise ValueError("la salle {} est introuvable".format(mnemonic))

    def ajouter_salle(self, r_x, r_y, r_z, mnemonic=None):
        """Ajoute une nouvelle salle.

        r_x, r_y et r_z sont les coordonnées relatives par rapport
        au milieu du navire.
        Si mnemonic est None (par défaut), cherche un mnémonique disponible.

        """
        r_coords = (r_x, r_y, r_z)
        if r_coords in self.salles.keys():
            raise ValueError("les coordonnées {}.{}.{} sont déjà " \
                    "occupées".format(*r_coords))

        if mnemonic is None:
            # On cherche le plus petit mnémonique non utilisé
            mnemonics = sorted(self.mnemonics_salles)
            for i in range(1, int(max(mnemonics, key=int)) + 2):
                if str(i) not in mnemonics:
                    mnemonic = str(i)
                    break

        salle = SalleNavire(self.cle, mnemonic, r_x, r_y, r_z, self)
        self.salles[r_coords] = salle
        return salle

    def lier_salle(self, salle_1, salle_2, direction):
        """Lie la salle salle_1 avec salle_2."""
        if isinstance(salle_1, str):
            c, salle_1 = self.get_salle(salle_1)
        if isinstance(salle_2, str):
            c, salle_2 = self.get_salle(salle_2)

        try:
            nom = NOMS_SORTIES[direction]
            article = ARTICLES[nom]
            contraire = NOMS_CONTRAIRES[direction]
            nom_contraire = NOMS_SORTIES[contraire]
            article_contraire = ARTICLES[nom_contraire]
        except KeyError:
            raise ValueError("cette direction est invalide")
        else:
            salle_1.sorties.ajouter_sortie(direction, nom, article, salle_2,
                    contraire)
            salle_2.sorties.ajouter_sortie(contraire, nom_contraire,
                    article_contraire, salle_1, direction)

    def supprimer_salle(self, mnemonic):
        """Supprime la salle précisée."""
        c, salle = self.get_salle(mnemonic)

        # On supprime les sorties menant à la salle
        for autre in self.salles.values():
            for sortie in list(autre.sorties):
                if sortie.salle_dest is salle:
                    autre.sorties.supprimer_sortie(sortie.direction)

        # Supprime la salle
        self.salles.pop(c).detruire()

    def generer_graph(self):
        """Génère le graph des sorties.

        Le graph est un dictionnaire comprenant en clé un tuple
        (origine, destination) et en valeur la liste des sorties
        nécessaires pour s'y rendre.

        L'algorithme Dijkstra est utilisé.

        """
        graph = {}
        aretes = {}
        sorties = {}

        # On remplit le chemin avec toutes les liaisons
        for salle in self.salles.values():
            origine = salle.mnemonic
            aretes[origine] = []
            for sortie in salle.sorties:
                destination = sortie.salle_dest.mnemonic
                aretes[origine].append(destination)
                sorties[origine, destination] = sortie.nom

        # Population des chemins dans le graph
        for origine in range(1, len(self.salles) + 1):
            origine = str(origine)
            for destination in range(1, len(self.salles) + 1):
                destination = str(destination)
                if origine == destination:
                    continue

                frontier = Queue()
                frontier.put(origine)
                origines = {origine: None}
                while not frontier.empty():
                    actuel = frontier.get()
                    if actuel == destination:
                        break

                    for fils in aretes[actuel]:
                        if fils not in origines:
                            frontier.put(fils)
                            origines[fils] = actuel


                # Recherche la liste des sorties
                parent = Queue()
                parent.put(destination)
                chemin = []
                while not parent.empty():
                    actuel = parent.get()
                    precedent = origines[actuel]
                    sortie = sorties[precedent, actuel]
                    chemin.insert(0, sortie)
                    if precedent != origine:
                        parent.put(precedent)

                graph[origine, destination] = chemin

        self.graph = graph

    def detruire(self):
        """Se détruit, ainsi que les véhicules créés sur ce modèle."""
        for vehicule in list(self.vehicules):
            vehicule.detruire()

        BaseObj.detruire(self)

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


"""Fichier contenant la classe ModeleNavire, détaillée plus bas."""

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
        self.graph = {}
        self.m_valeur = 1000
        self.duree_construction = 60
        self.description_vente = Description(parent=self)
        self.masculin = True

    def __getnewargs__(self):
        return ("", )

    @property
    def coordonnees_salles(self):
        """Retourne un tuple des coorodnnées des salles."""
        return tuple(self.salles.keys())

    @property
    def mnemonics_salles(self):
        """Retourne un tuple des mnémonics des salles."""
        return tuple(s.mnemonic for s in self.salles.values())

    def get_max_distance_au_centre(self):
        """Retourne la distance maximum par rapport au centre du navire."""
        distances = []
        for x, y, z in self.salles.keys():
            distances.append(sqrt(x ** 2 + y ** 2 + z ** 2))

        return max(distances)

    def get_salle(self, mnemonic):
        """Retourne la salle ayant le mnémonic indiqué.

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
        Si mnemonic est None (par défaut), cherche un mnémonic disponible.

        """
        r_coords = (r_x, r_y, r_z)
        if r_coords in self.salles.keys():
            raise ValueError("les coordonnées {}.{}.{} sont déjà " \
                    "occupées".format(*r_coords))

        if mnemonic is None:
            # On cherche le plus petit mnémonic non utilisé
            mnemonics = sorted(self.mnemonics_salles)
            for i in range(1, int(max(mnemonics, key=int)) + 2):
                if str(i) not in mnemonics:
                    mnemonic = str(i)

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

    def generer_graph(self):
        """Génère le graph des sorties.

        Le graph est un dictionnaire comprenant en clé un tuple
        (origine, destination) et en valeur la liste des sorties
        nécessaires pour s'y rendre.

        """
        def ajouter_paire(graph, origine, destination, sorties):
            """Ajoute une paire unique au graph."""

            o_mnemo = origine if isinstance(origine, str) else origine.mnemonic
            d_mnemo = destination if isinstance(destination, str) else \
                    destination.mnemonic
            if o_mnemo == d_mnemo:
                return False

            chemin = graph.get((o_mnemo, d_mnemo))
            if chemin is None or len(sorties) < len(chemin):
                graph[(o_mnemo, d_mnemo)] = sorties
                return True

            return False

        def enrichir_graph(graph, origine, destination, sorties):
            """Enrichit le graph."""
            court = ajouter_paire(graph, origine, destination, sorties)
            if court:
                for (o_mnemo, d_mnemo), chemin in tuple(graph.items()):
                    if o_mnemo == destination.mnemonic:
                        n_chemin = list(sorties) + list(chemin)
                        ajouter_paire(graph, origine, d_mnemo, n_chemin)

                for sortie in destination.sorties:
                    if sortie.salle_dest:
                        enrichir_graph(graph, destination, sortie.salle_dest,
                                [sortie.nom])

                for (o_mnemo, d_mnemo), chemin in tuple(graph.items()):
                    if o_mnemo == destination.mnemonic:
                        n_chemin = list(sorties) + list(chemin)
                        ajouter_paire(graph, origine, d_mnemo, n_chemin)

        graph = {}
        origine = self.salles.get((0, 0, 0))
        if origine:
            for sortie in origine.sorties:
                if sortie and sortie.salle_dest:
                    enrichir_graph(graph, origine, sortie.salle_dest,
                            [sortie.nom])

        self.graph = graph

    def detruire(self):
        """Se détruit, ainsi que les véhicules créés sur ce modèle."""
        for vehicule in list(self.vehicules):
            vehicule.detruire()

        BaseObj.detruire(self)

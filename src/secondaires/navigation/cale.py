# -*-coding:Utf-8 -*

# Copyright (c) 2013 LE GOFF Vincent
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


"""Fichier contenant la classe Cale, détaillée plus bas."""

from abstraits.obase import BaseObj

CONTENEURS = [
        "boulets",
        "écopes",
        "sacs de poudre",
        "tonneaux de poix",
        "vivres",
]

TYPES = {
        "boulet de canon": "boulets",
        "sac de poudre": "sacs de poudre",
        "écope": "écopes",
        "calfeutrage": "tonneaux de poix",
        "nourriture": "vivres",
        "poisson": "vivres",
        "viande": "vivres",
        "légume": "vivres",
        "fruit": "vivres",
        "gâteau": "vivres",
}

class Cale(BaseObj):

    """Classe représentant la cale d'un navire.

    La cale peut contenir plusieurs marchandises en grande quantité.
    Avoir un objet à part permet d'avoir plus facilement des règles
    concernant ce qui peut être mis en cale, à quel endroit dans le
    navire et comment le récupérer.

    Les boulets de canon, la poudre, les vivres, la plupart des
    instruments et les marchandises sont conservés sous la forme de
    prototype: nombre. Quand un joueur ou membre d'équipage demande
    l'objet en question, il est matérialisé (et lui ai donné directement).

    """

    def __init__(self, navire):
        """Constructeur du matelot."""
        BaseObj.__init__(self)
        self.navire = navire
        self.boulets = {}
        self.sacs_poudre = {}
        self.ecopes = {}
        self.tonneaux_poix = {}
        self.vivres = {}

        self._construire()

    def __getnewargs__(self):
        return (None, )

    def __repr__(self):
        navire = self.navire and self.navire.cle or "aucun"
        return "<Cale du navire {}>".format(repr(navire))

    @property
    def poids(self):
        """Retourne le poids de la cale (somme des contenus)."""
        poids = 0
        for conteneur in self.conteneurs.values():
            for cle, qtt in conteneur.items():
                try:
                    prototype = importeur.objet.prototypes[cle]
                except KeyError:
                    continue

                poids += prototype.poids_unitaire * qtt

        return poids

    @property
    def poids_max(self):
        """Retourne le poids maximum défini dans le modèle."""
        return self.navire.modele.cale_max

    @property
    def conteneurs(self):
        """Retourne les conteneurs de la cale."""
        return {
                "boulets": self.boulets,
                "sacs de poudre": self.sacs_poudre,
                "écopes": self.ecopes,
                "tonneaux de poix": self.tonneaux_poix,
                "vivres": self.vivres,
        }

    @property
    def types(self):
        """Retourne la correspondance nom_type: conteneur."""
        return {
                "boulet de canon": self.boulets,
                "sac de poudre": self.sacs_poudre,
                "écope": self.ecopes,
                "calfeutrage": self.tonneaux_poix,
                "nourriture": self.vivres,
                "poisson": self.vivres,
                "viande": self.vivres,
                "légume": self.vivres,
                "fruit": self.vivres,
                "gâteau": self.vivres,
        }

    def accepte(self, salle, nom_type):
        """Vérifie si la salle en paramtère accepte le nom type."""
        conteneur = TYPES.get(nom_type)
        if conteneur is None:
            return False

        return conteneur in salle.cales

    def ajouter_objets(self, objets):
        """Ajoute les objets précisés dans la cale, si possible."""
        nombre = 0
        poids = self.poids
        poids_max = self.poids_max
        for objet in list(objets):
            nom_type = objet.nom_type
            if nom_type in self.types:
                conteneur = self.types[nom_type]
                if nom_type == "sac de poudre":
                    if objet.onces_contenu < objet.onces_max_contenu:
                        raise ValueError("{} n'est pas complètement " \
                                "rempli et ne peut être mis en cale " \
                                "tel quel.".format(
                                objet.get_nom().capitalize()))
                elif nom_type == "calfeutrage":
                    if objet.onces_contenu < objet.onces_max_contenu:
                        raise ValueError("{} n'est pas complètement " \
                                "rempli et ne peut être mis en cale " \
                                "tel quel.".format(
                                objet.get_nom().capitalize()))
            elif poids + objet.prototype.poids_unitaire > poids_max:
                raise ValueError("Vous ne pouvez remplir la cale davantage.")
            else:
                raise ValueError("{} ne peut être mis en " \
                        "cale.".format(objet.get_nom().capitalize()))

            nb = conteneur.get(objet.prototype.cle, 0)
            nb += 1
            conteneur[objet.prototype.cle] = nb
            poids += objet.prototype.poids_unitaire
            importeur.objet.supprimer_objet(objet.identifiant)
            nombre += 1

        return nombre

    def recuperer(self, personnage, cle, nb=1, donner=True):
        """Récupère une quantité d'objets depuis la cale."""
        prototype = importeur.objet.prototypes[cle]
        nom_type = prototype.nom_type
        if nom_type in self.types:
            conteneur = self.types[nom_type]
        else:
            personnage << "|err|{} ne se conserve pas en cale.|ff|".format(
                    prototype.nom_singulier.capitalize())
            return

        if cle not in conteneur:
            personnage << "|err|{} est introuvable dans cette " \
                    "cale.|ff|".format(prototype.nom_singulier.capitalize())
            return

        quantite = conteneur[cle]
        if quantite < nb:
            nb = quantite

        conteneur[cle] -= nb
        if conteneur[cle] == 0:
            del conteneur[cle]

        personnage << "Vous récupérez {} depuis la cale.".format(
                prototype.get_nom(nb))
        objet = None
        for i in range(nb):
            objet = importeur.objet.creer_objet(prototype)
            if donner:
                personnage.ramasser_ou_poser(objet)

        return objet

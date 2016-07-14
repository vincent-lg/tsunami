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


"""Fichier contenant la classe Cale, détaillée plus bas."""

from abstraits.obase import BaseObj
from primaires.objet.conteneur import ConteneurObjet

CONTENEURS = [
        "boulets",
        "écopes",
        "sacs de poudre",
        "tonneaux de poix",
        "vivres",
        "armes",
        "pavillons",
        "marchandises",
        "outils",
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
        "tonneau d'eau": "vivres",
        "arme de jet": "armes",
        "épée": "armes",
        "hache": "armes",
        "lance": "armes",
        "masse": "armes",
        "projectile": "armes",
        "pavillon": "pavillons",
        "sac de matériau": "marchandises",
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
        self.eau_douce = 0
        self.conteneur = ConteneurObjet(self)
        self.boulets = {}
        self.sacs_poudre = {}
        self.ecopes = {}
        self.tonneaux_poix = {}
        self.vivres = {}
        self.armes = {}
        self.pavillons = {}
        self.marchandises = {}
        self.outils = {}

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


        # Parcourt des objets uniques
        for objet, quantite in self.conteneur.iter_nombres():
            poids += objet.poids * quantite

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
                "armes": self.armes,
                "pavillons": self.pavillons,
                "marchandises": self.marchandises,
                "outils": self.outils,
        }

    @property
    def types(self):
        """Retourne la correspondance nom_type: conteneur."""
        marchandises = importeur.objet.get_types_herites("matériau")
        outils = importeur.objet.get_types_herites("outil")
        types = {
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
                "tonneau d'eau": self.vivres,
                "arme de jet": self.armes,
                "épée": self.armes,
                "hache": self.armes,
                "lance": self.armes,
                "masse": self.armes,
                "projectile": self.armes,
                "pavillon": self.pavillons,
                "sac de matériau": self.marchandises,
        }

        # Marchandises
        for nom_type in marchandises:
            types[nom_type] = self.marchandises

        # Outils
        for nom_type in outils:
            types[nom_type] = self.outils

        return types

    def get_noms(self, nom):
        """Retourne les noms d'objet contenus dans la portion de la cale."""
        objets = {}
        liste = list(self.conteneurs[nom].items())
        liste += list(self.conteneur.iter_nombres())
        for objet, quantite in liste:
            if isinstance(objet, str):
                try:
                    objet = importeur.objet.prototypes[objet]
                except KeyError:
                    continue

            nom_type = objet.nom_type
            conteneur = TYPES[nom_type]
            if conteneur == nom:
                singulier = objet.get_nom(1)
                if singulier not in objets:
                    objets[singulier] = (objet, quantite)
                else:
                    quantite += objets[singulier][1]
                    objets[singulier] = (objet, quantite)

        noms = []
        for nom, (objet, quantite) in sorted(objets.items()):
            nom = objet.get_nom(quantite)
            noms.append(nom)

        return noms

    def accepte(self, salle, nom_type):
        """Vérifie si la salle en paramtère accepte le nom type."""
        conteneur = TYPES.get(nom_type)
        if conteneur is None:
            return False

        if salle is None:
            return True

        return conteneur in salle.cales

    def ajouter_prototype_objet(self, prototype, nombre=1):
        """Ajoute les objets spécifiés en cale."""
        nom_type = prototype.nom_type
        if nom_type in self.types:
            conteneur = self.types[nom_type]
        else:
            raise ValueError("{} ne peut être mis en " \
                    "cale.".format(prototype.cle))

        nb = conteneur.get(prototype.cle, 0)
        nb += nombre
        conteneur[prototype.cle] = nb

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
                elif nom_type == "tonneau d'eau":
                    self.eau_douce += objet.gorgees_contenu
            elif poids + objet.prototype.poids_unitaire > poids_max:
                raise ValueError("Vous ne pouvez remplir la cale davantage.")
            else:
                raise ValueError("{} ne peut être mis en " \
                        "cale.".format(objet.get_nom().capitalize()))

            if objet.nom_singulier == objet.prototype.nom_singulier and \
                    not objet.est_de_type("sac de matériau"):
                # C'est un objet non unique
                nb = conteneur.get(objet.prototype.cle, 0)
                nb += 1
                conteneur[objet.prototype.cle] = nb
                importeur.objet.supprimer_objet(objet.identifiant)
            else:
                # C'est un objet unique, on le conserve à part
                objet.contenu.retirer(objet)
                self.conteneur.ajouter(objet)

            poids += objet.prototype.poids_unitaire
            nombre += 1

        return nombre

    def recuperer(self, personnage, cle, nb=1, donner=True):
        """Récupère une quantité d'objets depuis la cale.

        cle peut être une liste d'objets.

        """
        if isinstance(cle, list):
            objets = cle
            prototype = objets[0].prototype
            cle = prototype.cle
        else:
            objets = []
            prototype = importeur.objet.prototypes[cle]

        nom_type = prototype.nom_type
        if nom_type in self.types:
            conteneur = self.types[nom_type]
        else:
            personnage << "|err|{} ne se conserve pas en cale.|ff|".format(
                    prototype.nom_singulier.capitalize())
            return

        # Cet objet se trouve-t-il dans le conteneur
        if objets:
            objet = objets[0]
            personnage << "Vous récupérez {} depuis la cale.".format(
                    objet.get_nom(nb))
            for objet in objets:
                self.conteneur.retirer(objet)
                if objet.est_de_type("tonneau d'eau"):
                    nb_max = objet.gorgees_max_contenu
                    if nb_max > self.eau_douce:
                        objet.gorgees_contenu = self.eau_douce
                    self.eau_douce -= objet.gorgees_contenu

                if donner:
                    personnage.ramasser_ou_poser(objet)

            return objet

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
            if prototype.est_de_type("tonneau d'eau"):
                nb_max = prototype.gorgees_max_contenu
                if nb_max > self.eau_douce:
                    objet.gorgees_contenu = self.eau_douce
                self.eau_douce -= objet.gorgees_contenu

            if donner:
                personnage.ramasser_ou_poser(objet)

        return objet

    def boire(self):
        """Boit une gorgée, retire un tonneau d'eau si nécessaire."""
        total = 0
        plus_petit = None
        for cle, nb in self.vivres.items():
            prototype = importeur.objet.prototypes[cle]
            if prototype.est_de_type("tonneau d'eau"):
                total += prototype.gorgees_max_contenu * nb
                if plus_petit is None or plus_petit.gorgees_max_contenu > \
                        prototype.gorgees_max_contenu:
                    plus_petit = prototype

        if self.eau_douce == 0:
            raise ValueError("Il n'y a plus d'eau douce dans la cale.")

        self.eau_douce -= 1
        if total - plus_petit.gorgees_max_contenu >= self.eau_douce:
            # On retire le plus petit
            self.vivres[prototype.cle] -= 1
            if self.vivres[prototype.cle] <= 0:
                del self.vivres[prototype.cle]

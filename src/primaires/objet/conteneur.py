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


"""Ce fichier contient la classe ConteneurObjet, détaillée plus bas."""

from bases.exceptions.base import ExceptionMUD
from collections import OrderedDict
from datetime import datetime

from abstraits.obase import BaseObj
from .objet_non_unique import ObjetNonUnique

class ConteneurObjet(BaseObj):

    """Conteneur standard d'objet.

    Cette classe peut être héritée (le sol d'une salle par exemple est un
    conteneur d'objet hérité) ou utilisée telle qu'elle.

    Un objet conteneur contient lui-même d'autres objets.
    Note : le conteneur d'objet utilise deux listes en fonction de
    l'unicité ou nom des objets.

    Les objets uniques, la majorité, sont représentés par une instance
    pour chaque objet. Les objets non uniques, comme la monnaie, sont des
    objets représentés par leur prototype et le nombre d'objets présents.

    """

    def __init__(self, parent=None):
        """Constructeur du conteneur"""
        BaseObj.__init__(self)
        self._objets = []
        self._non_uniques = []
        self.parent = parent
        self._construire()

    def __getnewargs__(self):
        return ()

    def __iter__(self):
        """Itérateur"""
        liste = list(self._objets) + list(self._non_uniques)
        return iter(liste)

    def __repr__(self):
        parent = repr(self.parent) if self.parent else "sans parent"
        return parent

    def __str__(self):
        parent = repr(self.parent) if self.parent else "sans parent"
        return parent + " " + str(self._objets) + " " + str(self._non_uniques)

    def __contains__(self, objet):
        return objet in self._objets

    @property
    def grand_parent(self):
        if hasattr(self.parent, "grand_parent"):
            return self.parent.grand_parent
        else:
            return self.parent

    def iter_nombres(self):
        """Parcourt les objets et quantités du conteneur."""
        for objet in self._objets:
            yield (objet, 1)
        for objet in self._non_uniques:
            yield (objet.prototype, objet.nombre)

    def get_objets_cle(self, cle, limite=None):
        """Retourne une liste des objets de clé indiquée."""
        objets = []
        for objet, quantite in self.iter_nombres():
            if objet.cle == cle:
                objets.append(objet)

        return objets[:limite]

    def get_objets_par_nom(self):
        """Retourne une liste de couples (objet, nombre).

        ATTENTION : pour les objets non uniques, on retourne le
        prototype mais le comportement devrait être identique la
        plupart du temps.

        """
        objets = OrderedDict()
        nombres = {}
        for objet in self._objets:
            if not objet.visible:
                continue

            nom = objet.get_nom()
            objets[nom] = objet
            nb = nombres.get(nom, 0)
            nombres[nom] = nb + 1

        ret = []
        for objet in self._non_uniques:
            ret.append((objet.prototype, objet.nombre))

        for nom, objet in objets.items():
            nombre = nombres[nom]
            ret.append((objet, nombre))

        return tuple(ret)

    def ajouter(self, objet, nombre=1):
        """On ajoute l'objet dans le conteneur.

        On peut très bien ajouter un prototype si l'objet est dit non unique.

        """
        prototype = hasattr(objet, "prototype") and objet.prototype or objet
        self._enregistrer()
        if prototype.unique:
            self.supporter_poids_sup(objet.poids)
            objet.contenu = self
            objet.ajoute_a = datetime.now()
            if objet not in self._objets:
                self._objets.append(objet)
            else:
                raise ValueError("le conteneur {} contient déjà l'objet " \
                        "{}".format(repr(self), objet))
        else:
            qtt = nombre
            # On cherche l'objet non unique correspondant au prototype
            non_unique = None
            for objet in self._non_uniques:
                if objet.prototype == prototype:
                    non_unique = objet
                    qtt -= objet.nombre
                    break

            self.supporter_poids_sup(prototype.poids_unitaire * nombre)
            if non_unique:
                non_unique.nombre += nombre
            else:
                non_unique = ObjetNonUnique(prototype, nombre)
                self._non_uniques.append(non_unique)

    def retirer(self, objet, nombre=1, accepte_non_trouve = False):
        """On retire l'objet du conteneur"""
        prototype = hasattr(objet, "prototype") and objet.prototype or objet
        self._enregistrer()
        if prototype.unique:
            if objet in self._objets:
                self._objets.remove(objet)
            else:
                if accepte_non_trouve:
                    return nombre
                raise ValueError("le conteneur {} ne contient pas l'objet " \
                        "{}".format(repr(self), objet))
            return nombre - 1
        else:
            non_unique = None
            for objet in self._non_uniques:
                if objet.prototype is prototype:
                    non_unique = objet
                    break

            if non_unique:
                nombre_retirable = min(nombre, non_unique.nombre)
                non_unique.nombre -= nombre_retirable
                self.nettoyer_non_uniques()
                nombre_a_retirer = nombre - nombre_retirable
                # S'il en reste à retirer, retrait récursif parmi les enfants
                if nombre_a_retirer > 0:
                    sous_conteneurs = [o for o in self._objets \
                                       if o.est_de_type("conteneur")]
                    for sc in sous_conteneurs:
                        nombre_a_retirer = sc.conteneur.retirer(objet,
                                nombre_a_retirer, True)
                        if nombre_a_retirer == 0:
                            break
                return nombre_a_retirer
            else:
                if accepte_non_trouve:
                    return nombre
                raise ValueError("le conteneur {} ne contient pas l'objet " \
                        "{} (qtt={})".format(repr(self), objet, nombre))

    def nettoyer_non_uniques(self):
        """Nettoie les objets non uniques présents en quantité négative."""
        self._non_uniques = [o for o in self._non_uniques if o.nombre > 0]

    def supporter_poids_sup(self, poids, recursif=True):
        """Méthode vérifiant que le conteneur peut contenir le poids.

        Le poids indiqué est le poids supplémentaire.

        Si recursif est à True, on vérifie que les conteneurs
        qui contiennent l'objet peuvent également supporter ce nouveau poids.

        Si une erreur survient (dans cet objet ou l'un de ses pères)
        on lève l'exception SurPoids.

        """
        if not self.parent:
            return True

        poids_actuel = self.parent.poids
        poids_max = self.parent.poids_max
        if poids_actuel + poids > poids_max:
            raise SurPoids("{} ne peut contenir davantage.".format(
                    self.parent.nom_singulier.capitalize()))

        if recursif:
            parent = self.parent
            contenu = hasattr(parent, "contenu") and parent.contenu or parent
            if hasattr(contenu, "supporter_poids_sup"):
                contenu.supporter_poids_sup(poids, recursif)


class SurPoids(ExceptionMUD):

    """Exception levée en cas de surpoids."""

    pass

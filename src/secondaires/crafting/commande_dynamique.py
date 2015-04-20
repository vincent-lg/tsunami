# -*-coding:Utf-8 -*

# Copyright (c) 2015 LE GOFF Vincent
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


"""Fichier contenant la classe CommandeDynamique détaillée plus bas."""

from abstraits.obase import BaseObj
from primaires.format.description import Description
from primaires.interpreteur.commande.commande import Commande
from primaires.interpreteur.masque.parametre import Parametre

class CommandeDynamique(BaseObj):

    """Classe décrivant les commandes dynamiques du crafting.

    Il existe deux types de ocmmandes dynamiques : celles définies
    dans le scripting, qui font systématiquement référence à
    des éléments observables, et celles définies dans le crafting,
    qui sont plus configurables et permettent presque autant de
    liberté que les commandes standard.

    Ces dernières sont intégralement scriptables et permettent
    de configurer un véritable schéma, ce qui rend leur puissance
    encore plus importante. Le schéma est généralement convertit
    en paramètres scripting, ce qui permet une plus grande
    flexibilité.

    """

    def __init__(self, parent, nom_francais, nom_anglais):
        """Constructeur d'une commande dynamique."""
        BaseObj.__init__(self)
        self.parent = parent
        self.nom_francais = nom_francais
        self.nom_anglais = nom_anglais
        self.commande = None # commande statique liée
        self._utilisable = False
        self._nom_categorie = "divers"
        self._aide_courte = "à renseigner..."
        self.aide_longue = Description(parent=self, scriptable=False,
                callback="maj")
        self._construire()

    def __getnewargs__(self):
        return ("", "", "")

    def __repr__(self):
        parent = "{}:".format(self.parent) if self.parent else ""
        return "<CommandeDynamique '{}{}/{}'>".format(
                parent, self.nom_francais, self.nom_anglais)

    def __str__(self):
        parent = "{}:".format(self.parent) if self.parent else ""
        return parent + self.nom_francais + "/" + self.nom_anglais

    def __getstate__(self):
        dico_attr = self.__dict__.copy()
        if "commande" in dico_attr:
            del dico_attr["commande"]

        return dico_attr

    @property
    def nom_complet(self):
        """Retourne le nom complet (<parent>:)<fr>/<an>."""
        parent = "{}:".format(self.parent) if self.parent else ""
        return parent + self.nom_francais + "/" + self.nom_anglais

    def _get_aide_courte(self):
        return self._aide_courte
    def _set_aide_courte(self, aide):
        if len(aide) > 70:
            aide = aide[:70]
        self._aide_courte = aide
        self.maj()
    aide_courte = property(_get_aide_courte, _set_aide_courte)

    def _get_nom_categorie(self):
        return self._nom_categorie
    def _set_nom_categorie(self, categorie):
        self._nom_categorie = nom_categorie
        self.maj()
    nom_categorie = property(_get_nom_categorie, _set_nom_categorie)

    def _get_utilisable(self):
        return self._utilisable
    def _set_utilisable(self, utilisable):
        self._utilisable = utilisable
        if utilisable and self.commande is None:
            self.ajouter()
    utilisable = property(_get_utilisable, _set_utilisable)

    def ajouter(self):
        """Ajoute la commande dans l'interpréteur.

        Il est préférable de faire cela après l'insertion des commandes
        statiques dans l'interpréteur, c'est-à-dire durant la phase de
        préparation du module.

        Si la commande a un parent, on va créer à la place son
        paramètre.

        """
        parent = None
        if self.parent:
            parent = importeur.interpreteur.trouver_commande(self.parent)
            commande = Parametre(self.nom_francais, self.nom_anglais)
        else:
            commande = Commande(self.nom_francais, self.nom_anglais)

        commande.nom_categorie = self.nom_categorie
        commande.aide_courte = self.aide_courte
        commande.aide_longue = str(self.aide_longue)
        commande.interpreter = self.interpreter
        if parent:
            parent.ajouter_parametre(commande)
        else:
            importeur.interpreteur.ajouter_commande(commande)

        self.commande = commande
        return commande

    def interpreter(self, personnage, dic_masques):
        """Méthode outre-passant l'interprétation de la commande statique.

        """
        personnage << "Bien joué !"

    def maj(self):
        """Mise à jour de la commande dynamique."""
        if self.commande:
            self.commande.nom_categorie = self.nom_categorie
            self.commande.aide_courte = self._aide_courte
            self.commande.aide_longue = str(self.aide_longue)


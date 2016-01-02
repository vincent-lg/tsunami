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


"""Fichier définissant la classe NoeudMasque détaillée plus bas;"""

import re

from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.masque.noeuds.base_noeud import BaseNoeud
from primaires.interpreteur.masque.noeuds.embranchement import Embranchement
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation

# Constantes
RE_MASQUE = re.compile(r"^(<?)((.*):)?([^ >]*)(>?)$")
RE_MOT_CLE = re.compile(r"^[A-Za-z]*/[A-Za-z]*$")

class NoeudMasque(BaseNoeud):

    """Noeud masque, noeud contenant un masque.
    Sa validation dépend de la validation de ses masques.
    De par son statut, s'il possède un noeud suivant, deux possibilités :
    -   soit c'est un noeud optionnel et le noeud masque que contient ce
        noeud fils est optionnel ;
    -   soit c'est un noeud masque également et le masque contenu dans ce fils
        est obligatoire.

    """

    def __init__(self, parente, commande):
        """Constructeur du noeud masque"""
        BaseNoeud.__init__(self)
        self.nom = ""
        self.parente = parente # commande parente
        self.commande = commande
        self.masques = []  # une liste vide de masques
        self.defaut = None  # valeur par défaut

    def construire_depuis_schema(self, lst_schema):
        """Construit le masque depuis le schéma."""
        # On convertit la liste en chaîne
        schema = liste_vers_chaine(lst_schema)
        delimiteurs = ('>', ' ', ')')
        fins = [schema.index(dl) for dl in delimiteurs if dl in schema]
        pos_fin = min(fins)
        fin = schema[pos_fin]
        schema = schema[:pos_fin]
        lst_schema[:] = lst_schema[pos_fin + 1:]

        # On extrait le type du schéma
        # Si c'est un mot-clé d'abord
        res = RE_MOT_CLE.search(schema)
        if res:
            self.construire_mot_cle(schema)
            return

        if fin in ('>', ):
            schema += fin

        res = RE_MASQUE.search(schema)
        if not res:
            raise ValueError("le schéma {} n'a pas pu être interprété".format(
                    schema))

        groupes = res.groups()
        # Nos groupes sont un tuple constitué de :
        # 1.  le signe < si présent (sinon None)
        # 2.  le nom avec le signe ':' (on ne l'utilise pas)
        # 3.  le nom sans le signe ':' si présent, sinon None
        # 4.  le type du masque
        # 5.  le signe > si présent (sinon None)
        inf, none, nom, liste_types_masques, sup = groupes
        liste_types_masques = liste_types_masques.split("|")

        # Nettoyage des inf et sup
        if not inf: inf = ""
        if not sup: sup = ""

        # On cherche le type de masque dans l'interpréteur
        # on remplace dans liste_types_masques chaque str par son instance
        # de masque.
        # Note: si chevrons est à False, on ne cherche pas dans l'interpréteur
        # mais dans la commande.
        # Si le masque n'existe pas, une exception est levée.
        for i, str_type_masque in enumerate(liste_types_masques):
            proprietes = ""
            if str_type_masque.count("{"):
                proprietes = "{" + "{".join(str_type_masque.split("{")[1:])
                str_type_masque = str_type_masque.split("{")[0]

            type_masque = type(self).importeur.interpreteur.get_masque(
                    str_type_masque)
            type_masque.construire(str_type_masque + proprietes)

            liste_types_masques[i] = type_masque

        # Si le nom du masque n'est pas défini, on le déduit du premier
        # type de masque
        if not nom:
            nom = liste_types_masques[0].nom

        self.nom = nom

        self.masques = liste_types_masques
        for masque in self.masques:
            masque.nom = self.nom

    def construire_mot_cle(self, schema):
        """Construit le mot-clé depuis le schéma.

        Un mot-clé a une forme assez simple :
            francais/anglais

        Exemple : depuis/from

        """
        francais, anglais = schema.split("/")
        self.masques = [type(self).importeur.interpreteur.creer_mot_cle(
                francais, anglais)]

    @property
    def masque(self):
        """Retourne le premier masque."""
        return self.masques[0]

    def est_parametre(self):
        """Retourne True si le premier masque est un paramètre."""
        return self.masque.est_parametre()

    def __str__(self):
        """Méthode d'affichage"""
        msg = "msg "
        msg += self.nom + "["
        msg += ", ".join([str(masque) for masque in self.masques])
        msg += "]"
        if self.suivant:
            msg += " : " + str(self.suivant)

        return msg

    def get_masque(self, nom_masque):
        """Retourne le masque du nom 'nom_masque'"""
        if self.nom == nom_masque:
            return self.masque
        elif self.suivant:
            return self.suivant.get_masque(nom_masque)
        else:
            return None

    def repartir(self, personnage, masques, commande, tester_fils=True):
        """Répartit dans le masque si possible."""
        lstrip(commande)
        for masque in self.masques:
            masque.init()
            valide = masque.repartir(personnage, masques, commande)
            if valide:
                break

        if valide and self.suivant:
            valide = self.suivant.repartir(personnage, masques, commande)

        return valide

    def valider(self, personnage, dic_masques, tester_fils=True):
        """Validation d'un noeud masque.

        On va essayer de valider successivement chaque masque possible. Si
        aucun masque ne marche, on s'arrête ici.

        """
        valide = False
        premiere_erreur = None
        for masque in self.masques:
            try:
                valide = masque.valider(personnage, dic_masques)
            except ErreurValidation as err:
                if not premiere_erreur:
                    premiere_erreur = err
                valide = False

        if not valide:
            if premiere_erreur:
                raise premiere_erreur
        elif self.suivant and tester_fils:
            valide = self.suivant.valider(personnage, dic_masques)

        return valide

    def afficher(self, personnage=None):
        """Retourne un affichage du masque pour les joueurs."""
        noms_masques = []
        for masque in self.masques:
            noms_masques.append(masque.nom_complet_pour(personnage))

        msg = ""
        if self.masque.est_mot_cle():
            msg += " / ".join(noms_masques)
        else:
            msg += "<" + " / ".join(noms_masques) + ">"

        if self.suivant:
            msg += " " + self.suivant.afficher(personnage)

        return msg

    def extraire_masques(self, masques=None):
        """Extraction des masques de la commande."""
        for masque in self.masques:
            masques[masque.nom] = masque

        for fils in self.fils:
            if fils:
                fils.extraire_masques(masques)

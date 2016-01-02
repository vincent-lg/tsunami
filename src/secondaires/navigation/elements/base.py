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


"""Fichier contenant la classe BaseElement, détaillée plus bas."""

from abstraits.obase import BaseObj
from corps.fonctions import valider_cle
from primaires.format.description import Description
from . import MetaElt

class BaseElement(BaseObj, metaclass=MetaElt):

    """Classe abstraite représentant le type de base d'un élément.

    Si des données doivent être communes à tous les types d'éléments
    c'est dans cette classe qu'elles apparaissent.

    """

    enregistrer = True
    nom_type = "" # à redéfinir
    def __init__(self, cle=""):
        """Constructeur d'un type"""
        if cle:
            valider_cle(cle)

        BaseObj.__init__(self)
        self.cle = cle

        self._attributs = {}
        self.nom = "un élément inconnu"
        self.description = Description(parent=self)

        # Editeur
        self._extensions_editeur = []

    def __getnewargs__(self):
        return ()

    def __str__(self):
        return self.cle

    def __getstate__(self):
        """Retourne le dictionnaire à enregistrer."""
        attrs = self.__dict__.copy()
        if "_extensions_editeur" in attrs:
            del attrs["_extensions_editeur"]
        if "_attributs" in attrs:
            del attrs["_attributs"]
        return attrs

    def etendre_editeur(self, raccourci, ligne, editeur, objet, attribut, *sup):
        """Permet d'étendre l'éditeur d'éléments en fonction du type.

        Paramètres à entrer :
        -   raccourci   le raccourci permettant d'accéder à la ligne
        -   ligne       la ligne de l'éditeur (exemple 'Description')
        -   editeur     le contexte-éditeur (exemple Uniligne)
        -   objet       l'objet à éditer
        -   attribut    l'attribut à éditer

        Cette méthode est appelée lors de la création de l'éditeur
        d'éléments.

        """
        self._extensions_editeur.append(
            (raccourci, ligne, editeur, objet, attribut, sup))

    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes.

        On récupère un dictionnaire représentant la présentation avec en
        clé les raccourcis et en valeur les enveloppes.

        Cela peut permettre de travailler sur les enveloppes ajoutées par
        'etendre_editeur'.

        """
        pass

    def get_description_ligne(self, personnage):
        """Retourne une description d'une ligne de l'élément."""
        return self.nom.capitalize() + " est là"

    def construire(self, parent):
        """Construit l'élément basé sur le parent."""
        pass

    def get_nom_pour(self, personnage):
        """Retourne le nom de l'élément."""
        return self.nom

    def regarder(self, personnage):
        """personnage regarde self."""
        msg = "Vous regardez {} :".format(self.nom) + "\n\n"
        msg += self.description.regarder(personnage, self)
        return msg

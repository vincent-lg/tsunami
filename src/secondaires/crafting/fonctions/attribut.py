# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
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


"""Fichier contenant la fonction attribut."""

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Retourne l'attribut crafting d'un objet."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.attribut, "Objet", "str")
        cls.ajouter_types(cls.attribut_prototype, "PrototypeObjet", "str")
        cls.ajouter_types(cls.attribut_cle, "str", "str")

    @staticmethod
    def attribut(objet, nom_attribut):
        """Retourne l'attribut spécifié 'un objet.

        L'attribut est un ajout de crafting, modifiable dans
        l'éditeur 'oedit'. Il s'applique à un objet ou à son
        prototype, si l'attribut n'est pas trouvé dans l'objet-même.

        Paramètres à préciser :

          * objet : l'objet dont on veut récupérer l'attribut
          * nom_attribut : le nom de l'attribut (une chaîne)

        """
        attributs = importeur.crafting.configuration[objet].attributs
        if attributs and nom_attribut in attributs:
            return attributs[nom_attribut]

        attributs = importeur.crafting.configuration[objet.prototype].attributs
        if attributs and nom_attribut in attributs:
            return attributs[nom_attribut]

        return None

    @staticmethod
    def attribut_prototype(prototype, nom_attribut):
        """Retourne l'attribut spécifique à un prototype d'objet.

        L'attribut est un ajout de crafting, modifiable dans
        l'éditeur 'oedit'. Il s'applique à un objet ou à son
        prototype. Dans ce cas précis, on cherche l'attribut dans
        le prototype, c'est-à-dire celui modifié directement dans
        l'éditeur.

        Paramètres à préciser :

          * prototype : le prototype d'objet à utiliser ;
          * nom_attribut : le nom de l'attribut (une chaîne)

        """
        attributs = importeur.crafting.configuration[prototype].attributs
        if attributs and nom_attribut in attributs:
            return attributs[nom_attribut]

        return None

    @staticmethod
    def attribut_cle(cle_prototype, nom_attribut):
        """Retourne l'attribut spécifique à un prototype d'objet.

        L'attribut est un ajout de crafting, modifiable dans
        l'éditeur 'oedit'. Il s'applique à un objet ou à son
        prototype. Dans ce cas précis, on cherche l'attribut dans
        le prototype, c'est-à-dire celui modifié directement dans
        l'éditeur.

        Paramètres à préciser :

          * cle_prototype : la clé du prototype d'objet (une chaîne) ;
          * nom_attribut : le nom de l'attribut (une chaîne)

        """
        try:
            prototype = importeur.objet.prototypes[cle_prototype]
        except KeyError:
            raise ErreurExecution("prototype d'objet {} inconnu".format(
                    repr(cle_prototype)))

        attributs = importeur.crafting.configuration[prototype].attributs
        if attributs and nom_attribut in attributs:
            return attributs[nom_attribut]

        return None

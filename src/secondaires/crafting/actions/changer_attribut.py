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


"""Fichier contenant l'action changer_attribut."""

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Change l'attribut crafting d'un objet."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.changer_attribut, "Objet", "str", "str")

    @staticmethod
    def changer_attribut(objet, nom_attribut, valeur):
        """Change l'attribut d'un objet.

        Paramètres à renseigner :

          * objet : l'objet dont on doit modifier l'attribut
          * nom_attribut : le nom de l'attribut à modifier
          * valeur : la valeur de l'attribut (forcément une chaîne)

        Notez bien qu'il existe plusieurs différences entre
        les attributs et extensiosn. Bien que les deux
        fonctionnalités soient ajoutées par le crafting, ils ont
        des buts distincts :

          * Les extensions modifient un éditeur ;
          * Les extensions peuvent s'appliquer à des salles, PNJ ou objets
          * Les attributs ne s'appliquent qu'aux objets
          * Les configurations d'extension peuvent être de types variables
          * Les valeurs des attributs sont toujours des chaînes
          * Une configuration d'extension s'applique au prototype
          * Un attribut s'applique à un objet précis, pas un prototype
          * Les attributs sont directement consultables dans la description.

        En somme, les attributs permettent une configuration plus
        rapide et pouvant s'appliquer à un objet précis. Le concept
        d'attributs est très utile pour les recettes, où un objet
        fabriqué récupère les attributs des ingrédients de la
        recette.
        Si par exemple vous voulez créer une épée formée d'un
        métal, le métal en question peut avoir l'attribut 'couleu'.
        L'attribut sera automatiquement répercuté sur l'objet epee
        qui aura aussi l'attribut 'couleur'. L'action scripting
        permet de forcer un attribut à changer de valeur (c'est
        parfois utile si vous voulez régler le conflit entre
        plusieurs attributs du même nom).

        """
        attributs = importeur.crafting.configuration[objet].attributs
        if attributs is None:
            attributs = {}
            importeur.crafting.configuration[objet].attributs = attributs

        attributs[nom_attribut] = valeur

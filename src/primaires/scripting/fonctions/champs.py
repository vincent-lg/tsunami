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


"""Fichier contenant la fonction champs."""

import re

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Retourne les champs de la structure indiquée."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.champs, "Structure")
        cls.ajouter_types(cls.champs, "Structure", "str")

    @staticmethod
    def champs(structure, filtres=""):
        """Retourne les champs de la structure indiquée.

        Paramètres à préciser :

          * structure : la structure dont on veut récupérer les champs.
          * filtres (optionnel) : une suite de filtres séparés par un espace.

        Cette fonction retourne tous les champs d'une structure. Pour
        les structures enregistrées, cela inclut le champ "structure"
        (contenant le nom du groupe de la structure) et "id" (contenant
        l'ID de la structure). Cette fonction retourne une liste de
        couples (clé du champ, valeur du champ) que vous pouvez parcourir
        (voir les exemples ci-dessous).

        Vous pouvez également préciser une liste de filtres séparés par
        un espace. Les filtres sont des expressions régulières (ce peut
        être, simplement, le nom du champ). Si le filtre commence par
        un tiret (-), les champs correspondants sont supprimés. Là encore,
        consultez les exemples pour voir leur utilisation.

        Exemples d'utilisation :

          # Ces exemples utiliseront la même structure que l'on crée ici
          structure = creer_structure()
          ecrire structure "auteur" joueur("Kredh")
          ecrire structure "creation" temps()
          ecrire structure "titre" "sans titre"
          ecrire structure "valide" 1
          # Retourne et parcourt la liste de champs
          pour chaque couple dans champs(structure):
              cle = recuperer(couple, 1)
              valeur = recuperer(couple, 2)
              dire personnage "Le champ $cle vaut $valeur."
          fait
          # Ce code envoie au personnage
          #     Le champ auteur vaut Kredh.
          #     Le champ creation vaut <TempsVariable ...>
          #     Le champ titre vaut sans titre.
          #     Le champ valide vaut 1.
          # (notez que la fonction peut retourner les champs dans un
          # ordre différent.)
          # Exemple de filtrage
          champs = champs(structure, "titre auteur")
          # Ne récupère que les champs 'titre' et 'auteur'
          champs = champs(structure, "-creation")
          # Récupère tous les champs sauf 'creation'
          champs = champs(structure, ".*e")
          # Récupère tous les champs dont la clé finit par 'e'.

        """
        # On commence par récupérer tous les champs sans filtrer
        champs = structure.donnees.copy()

        # Constitue une expression régulière pour les filtres indiqués
        expression = "^(?!e_existe$"
        contraires = []
        correspond = []

        for filtre in filtres.split(" "):
            if not filtre:
                continue

            if filtre.startswith("-"):
                contraires.append(filtre[1:] + "$")
            else:
                correspond.append(filtre + "$")

        if contraires:
            expression += "|" + "|".join(contraires)

        expression += ")(" + "|".join(correspond) + ")"
        print("travaille avec", expression)

        for champ, valeur in list(champs.items()):
            if not re.search(expression, champ, re.I):
                del champs[champ]

        # On convertit la liste des champs en liste
        liste = []
        for champ, valeur in champs.items():
            liste.append([champ, valeur])

        return liste

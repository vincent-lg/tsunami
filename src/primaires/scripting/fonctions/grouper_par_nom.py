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


"""Fichier contenant la fonction grouper_par_nom."""

from collections import OrderedDict
from fractions import Fraction

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Groupe les objets par nom."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.grouper_objets, "list")

    @staticmethod
    def grouper_objets(objets):
        """Groupe les objets par nom.

        Cette fonction travaille depuis une liste d'objets, et
        retourne une liste de listes sous la forme liste(liste(objet1,
        quantite1), liste(objet2, quantite2), ...)

        Paramètres à entrer :

          * objets : la liste des objets

        Exemple d'utilisation :

          # objets contient une liste d'objets
          groupe = grouper_par_nom(objets)
          pour chaque couple dans groupe:
              objet = recuperer(liste, 1)
              quantite = recuperer(liste, 2)
              nom = nom_objet(objet, quantite)
          fait

        """
        noms = OrderedDict()
        liens = {}

        for objet in objets:
            nom = objet.get_nom()
            if nom not in noms:
                noms[nom] = 0
                liens[nom] = objet
            noms[nom] += 1

        groupe = []
        for nom, qtt in noms.items():
            objet = liens[nom]
            groupe.append([objet, Fraction(qtt)])

        return groupe

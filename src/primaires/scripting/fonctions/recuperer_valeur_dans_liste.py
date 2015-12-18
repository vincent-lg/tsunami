# -*-coding:Utf-8 -*

# Copyright (c) 2014 LE GOFF Vincent
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


"""Fichier contenant la fonction recuperer_valeur_dans_liste."""

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Renvoie la valeur spécifiée d'une liste."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.recuperer_valeur_dans_liste, "list", "Fraction")

    @staticmethod
    def recuperer_valeur_dans_liste(liste, indice):
        """Retourne l'élément spécifié dans la liste.

        Paramètres à préciser :

          * liste : la liste d'éléments
          * indice : l'indice représentant la case de la liste

        Voir les exemples d'utilisation pour voir comment marche cette fonction.

        *NOTE* : les fonctions 'recuperer' et 'recupere_valeur_dans_liste'
        font strictement la même chose. La seconde est conservée pour
        des raisons de compatibilité. Préférez utiliser la première
        ('recuperer') dans vos scripts.

        Exemples d'utilisation :

          lettres = liste("a", "b", "c", "d", "e", "f")
          valeur = recuperer(liste, 3)
          # valeur contient maintenant "c", le troisième élément dans la liste
          # L'indice peut également être négatif
          valeur = recuperer(liste, -1)
          # valeur contient à présent "f", la dernière lettre

        """
        if int(indice) != indice: # nombre flottant
            raise ErreurException("le nombre flottant {} a été précisé " \
                    "comme indice de liste. Seuls des nombres entiers " \
                    "(1, 2, 3, ...) sont acceptés".format(indice))

        if indice == 1:
            raise ErreurExecution("l'indice précisé doit être positif ou " \
                    "négatif".format(indice))

        if indice < 0:
            indice = int(indice)
        else:
            indice = int(indice) - 1

        try:
            return liste[indice]
        except IndexError:
            raise ErreurExecution("l'indice spécifié ({}) est invalide " \
                    "dans cette liste de taille {}".format(indice,
                    len(liste)))

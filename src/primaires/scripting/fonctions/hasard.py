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


"""Fichier contenant la fonction hasard."""

from random import random, choice

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Retourne vrai ou faux aléatoirement.

    Cette fonction peut être utilisée associée à une condition."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.hasard, "Fraction")
        cls.ajouter_types(cls.choix_chaine, "str")
        cls.ajouter_types(cls.choix_liste, "list")
        cls.ajouter_types(cls.choix_probable, "list", "Fraction")
        cls.ajouter_types(cls.choix_probable, "list", "Fraction", "str")

    @staticmethod
    def hasard(probabilite):
        """Retourne vrai ou faux en fonction de la probabilité.

        La probabilité entrée doit être un entier entre 1 et 100.
        Un test avec une probabilité de 100 sera toujours vrai.
        Un test avec une probabilité de 50 aura 1/2 chances d'être vrai.
        Un test avec une probabilité de 0 sera toujours faux.

        """
        probabilite /= 100
        probabilite = float(probabilite)
        chance = random()
        return chance < probabilite

    @staticmethod
    def choix_chaine(chaine):
        """Choisit un des éléments de la chaîne séparé par |.

        La chaîne est sous la forme de plusieurs éléments séparés
        par |. Par exemple:

            cle = choisir("branche|tronc|racine|tige")

        Dans la variable 'cle' se trouvera soit "branche", soit
        "tronc", soit "racine", soit "tige".

        """
        if not chaine:
            raise ErreurExecution("la chaîne précisée est vide")

        chaines = chaine.split("_b_")
        return choice(chaines)

    @staticmethod
    def choix_liste(liste):
        """Retourne un élément aléatoire d'une liste.

        Paramètres :

          * liste : la liste dans laquelle l'élément sera sélectionné.

        Exemple d'utilisation :

          liste = liste("chat", "chien", "renard", "poule")
          element = hasard(liste)
          # element contiendra peut-être "chien"

        """
        return choice(liste)

    @staticmethod
    def choix_probable(liste, colonne, moyen="pourcent"):
        """Retourne un choix probable dans la liste indiquée.

        La liste passée en paramètre doit être une liste de listes.
        L'un des éléments de cette seconde liste doit contenir la
        probabilité. Cette fonction peut sembler assez complexe,
        consultez les exemples ci-dessous pour avoir une meilleure
        idée de son fonctionnement.

        Paramètres à entrer :

          * liste : la liste de listes
          * colonne : le numéro de la colonne contenant la probabilité
          * moyen : le moyen de calculer la probabilité

        Moyens disponibles :

          * "pourcent" : les probabilités sont en pourcent
          * "total" : les probabilités font référence à leur somme totale

        Cette fonction peut retourner une variable vide si aucune
        probabilité n'est trouvée.

        Plusieurs exemples d'utilisation :

          # Choix simple
          objets = liste()
          ajouter liste("pomme_rouge", 5) objets
          ajouter liste("pomme_verte", 8) objets
          ajouter liste("pomme_rose", 1) objets
          # La variable 'objets' contient donc une liste de listes.
          # Chaque liste de second niveau contient un couple :
          # une clé d'objet en premier paramètre et une probabilité
          # en second (colonne 2).
          choix = hasard(objets, 2)
          # 'choix' va contenir aléatoirement :
          # * "pomme_rouge" (5% de chance)
          # * "pomme_verte" (8% de chance)
          # * "pomme_rose" (1% de chance)
          # * Une variable vide (86% de chance)

          # Dans ce contexte, la somme de toute les probabilités ne
          # fait pas 100, il y a donc une chance que la fonction
          # 'hasard' ne retourne qu'une variable vide.
          # Vous pouvez aussi demander à cette variable de se baser
          # sur le total des probabilités.
          choix = hasard(objets, 2, "total")
          # choix va contenir aléatoirement :
          # * "pomme_rouge" (5 chance sur 14)
          # * "pomme_verte" (8 chances sur 14)
          # * "pomme_rose" (1 chances sur 14)

          # Dans ce cas, la variable retournée ne peut jamais être vide.

          # Si votre liste de second niveau contient plus de deux
          # éléments, la fonction 'hasard' retourne toute la liste.
          objets = liste()
          ajouter liste("pomme_rouge", 5, "une pomme rouge") objets
          ajouter liste("pomme_verte", 8, "une pomme verte") objets
          ajouter liste("pomme_rose", 1, "une pomme rose ?") objets
          # Ici 'objets' contient une liste de listes de trois
          # éléments (la clé, la probabilité toujours en colonne 2
          # et un nom associé). Appeler 'hasard' va retourner la
          # liste sélectionnée, car le système ne sait pas quel
          # élément il doit retourner, donc les retourne tous.
          # Vous devrez ensuite les extraire.
          choix = hasard(objets, 2)
          # 'choix' contient aléatoirement :
          # * Une variable vide
          # * liste("pomme_rouge", 5, "une pomme rouge")
          # * liste("pomme_verte", 8, "une pomme verte")
          # * liste("pomme_rose", 1, "une pomme rose ?")

        """
        colonne = int(colonne - 1)
        poids = [float(element[colonne]) for element in liste]
        total = 100
        if moyen == "total":
            total = sum(poids)

        rnd = random() * total
        for element in liste:
            element = list(element)
            probabilite = float(element[colonne])
            rnd -= probabilite
            if rnd < 0:
                if len(element) == 2:
                    del element[colonne]
                    return element[0]
                else:
                    return element

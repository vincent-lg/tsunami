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


"""Fichier contenant la fonction traite."""

from corps.fonctions import lisser
from primaires.format.fonctions import supprimer_accents
from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Effectue des traitements de mise en forme sur une chaîne."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.traite, "str", "str")

    @staticmethod
    def traite(chaine, operations):
        """Traite une chaîne de caractères selon plusieurs opérations.

        Cette fonction scripting permet de mettre en forme une chaîne
        de caractères (la mettre en majuscule, minuscule, retirer
        les accents...). Plusieurs opérations peuvent être précisées
        en même temps (voir les exemples ci-dessous).

        Paramètres à préciser :

          * chaine : la chaîne d'origine (à transformer)
          * operations : la chaîne contenant les flags de transformation

        Les flags d'opération sont à préciser dans une chaîne avec
        chaque nom de flag séparé par un espace. Voir les exemples
        pour plus d'informations. Les flags disponibles sont :

          * minuscule : met la chaîne en minuscule
          * majuscule : met la chaîne en majuscule
          * capital : met chaque première lettre de chaque mot en majuscule
          * titre : la première lettre de la chaîne est mise en majuscules
          * sans_accents : retire les accents.
          * lisser : change "de un" en "d'un", "le un" en "l'un"...
          * rogner : rogne les espaces au début et à la fin de la chaaîne

        Exemples d'utilisation :

          chaine = "BONNE JOURNÉE"
          # Met la chaîne en minuscule
          chaine = traite(chaine, "minuscule")
          # chaine contient à présent "bonne journée"
          chaine = "BONNE JOURNÉE"
          # Met la chaîne en capital sans accents
          chaine = traite(chaine, "capital sans_accents")
          # chaine contient à présent "Bonne Journee"
          # Puis met chaine en majuscule
          chaine = traite(chaine, "majuscule")
          # chaine contient à présent "BONNE JOURNEE"
          chaine = "C'est une porte de acier."
          chaine = traite(chaine, "lisser")
          # chaine contient "C'est une porte d'acier."

        """
        operations = operations.lower()
        if not operations:
            raise ErreurExecution("Précisez au moins une opération")

        operations = operations.split(" ")
        for operation in operations:
            if operation == "minuscule":
                chaine = chaine.lower()
            elif operation == "majuscule":
                chaine = chaine.upper()
            elif operation == "titre":
                chaine = chaine[0].upper() + chaine[1:]
            elif operation == "capital":
                chaine = chaine.title()
            elif operation == "rogner":
                chaine = chaine.strip(" ")
            elif operation == "sans_accents":
                chaine = supprimer_accents(chaine)
            elif operation == "lisser":
                chaine = lisser(chaine)
            else:
                raise ErreurExecution("Opération {} inconnue.".format(
                        repr(operation)))

        return chaine

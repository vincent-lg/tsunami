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


"""Fichier contenant la fonction joindre."""

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Convertit une liste en chaîne pour un affichage agréable."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.joindre, "list", "str")
        cls.ajouter_types(cls.joindre, "list", "str", "str")

    @staticmethod
    def joindre(liste, lien, dernier=""):
        """Retourne une chaîne repre'sentant la liste jointe.

        Les exemples plus bas sont assez explicites. L'idée est de convertir une liste de valeurs en une chaîne, souvent plus agréable à regarder.

        Paramètres à préciser :

          * liste : la liste à joindre ;
          * lien : la valeur à mettre entre chaque élément de liste ;
          * dernier (optionnel) : la valeur à mettre entre en dernier.

        La liste peut contenir tout et n'importe quoi, mais il est
        utile d'avoir une liste de chaînes, car on n'a pas de risques
        d'aléas d'affichage dans ce cas. Si par exemple vous voulez
        afficher une liste de joueurs, regrouper le nom des joueurs
        dans une liste que vous pourrez joindre ainsi. Ce n'est pas
        une obligation, mais cela évite des confusions. Consultez
        les exemples ci-dessous pour voir le fonctionnement de base
        de cette fonction.

        Exemples d'utilisation :

          liste = liste("abricot", "poire", "pomme", "banane")
          fruits = joindre(liste, " et ")
          # " et " sera placé entre chaque élément de la liste :
          # chaine contient donc :
          # "abricot et poire et pomme et banane"
          fruits = joindre(liste, ", ", " et ")
          # Ici, on veut mettre ", " entre chaque élément, excepté
          # le dernier lien. chaine contient donc :
          # "abricot, poire, pomme et banane"
          # Ce qui est d'autant plus agréable.
          participants = liste("Kredh", "Anael", "Eridan")
          trier participants
          participants = joindre(participants, " ")
          # participants contient : "Anael Eridan Kredh"

        """
        if not liste:
            return ""

        dernier = dernier or lien
        liste = [str(e) for e in liste]
        chaine = lien.join(liste[:-1])
        if len(liste) > 1:
            chaine += dernier

        chaine += liste[-1]
        return chaine

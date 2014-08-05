# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Fichier contenant la fonction contient."""

from primaires.scripting.fonction import Fonction
from primaires.format.fonctions import contient

class ClasseFonction(Fonction):

    """Teste si une chaîne contient une autre chaîne."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.contient_element, "object", "list")
        cls.ajouter_types(cls.contient, "str", "str")

    @staticmethod
    def contient(chaine_complete, expression):
        """Retourne vrai si la chaine_complete contient expression.

        Le test ne tient ni compte des majuscules ni des accents.
        Une expression est contenue dans une chaîne si l'expression
        est le début d'un des mots de la chaîne complète.
        Par exemple :
            "chien" est contenue dans "un chien de ferme"
        Ou :
            "po" est contenue dans "une pomme rouge"
        Mais :
            "table" n'est pas contenue dans "une étable"
        Car "table" n'est pas le début d'un des mots de "une étable".

        """
        return contient(chaine_complete, expression)

    @staticmethod
    def contient_element(element, liste):
        """Retourne vrai si la liste contient l'élément.

        Paramètres à préciser :

          * element : un élément de n'importe quel type
          * liste : la liste d'éléments

        Exemples d'utilisation :

          nombres = liste(1, 2, 3, 4, 5)
          si contient(5, nombres): # returnera vrai
              ...
          si contient(12, nombres): # retournera faux
              ...
          mots = liste("chat", "chien", "cheval")
          si contient("chat", mots): # retournera vrai
              ...
          si contient("canard", mots): # retournera faux
              ...

        Bien entendu, votre liste peut aussi contenir des types plus
        complexes, comme des joueurs, des objets, des salles ou autre.
        Cette fonction scripting pourra être utilisée dans tous les cas.
        Elle pourra être utilisée sans problème si la liste contient
        des doublons ou des données de différents types. Notez cependant
        que :

          varies = liste(1, 2.8, "chouette", "8")
          si contient(8, varies): # retournera faux

        Ce résultat peut-être inattendu est dû au fait que dans la liste,
        le dernier élément ("8") est une chaîne de caractères, alors
        que la fonction contient teste la présence d'un nombre. Ainsi,
        pour le système, la liste ne contiendra pas 8 alors qu'elle
        contiendra "8". Faire attention aux types de données.

        """
        return element in liste

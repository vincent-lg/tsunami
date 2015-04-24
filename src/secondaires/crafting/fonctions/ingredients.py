# -*-coding:Utf-8 -*

# Copyright (c) 2015 LE GOFF Vincent
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


"""Fichier contenant la fonction ingredients."""

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Retourne les ingrédient (objets) d'une liste d'objets.

    La recherche peut se faire par type ou clé de prototype.

    """

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.ingredients, "list", "str")

    @staticmethod
    def ingredients(objets, type_ou_prototype):
        """Retourne les ingrédients d'une liste d'objets.

        Cette fonction est très utile pour extraire les ingrédients
        d'une liste d'objets. C'est notamment très pratique quand
        il s'agit de scripter les recettes, qui peuvent ainsi
        récupréer les objets précis qui ont permis à la créer.

        Paramètres à préciser :

          * objets : la liste d'objets
          * type_ou_prototype : le nom du type ou prototype d'objet

        Exemple d'utilisation :

          # Admettons que 'objets' est une variable contenant :
          # * une pomme rouge (type fruit)
          # * une banane (type fruit)
          # * une carotte (type légume)
          fruits = ingredients(objets, "+fruit")
          # 'fruits' contient une pomme rouge et une banane
          legumes = ingredients(objets, "+légume")
          # legumes' contient une carotte crue
          armes = ingredients(objets, "+arme")
          # 'armes' contient une liste vide
          pommes = ingredients(objets, "pomme_rouge")
          # 'pommes' contient une pomme rouge
          bananes = ingredients(objets, "banane")
          # 'bananes' contient une liste vide

        Vous pouvez faire une recherche sur un type d'objet en
        préfixant son nom du signe + ("+type"). Dans tous les
        cas, le système retourne une liste : vide si rien n'est
        trouvé, contenant un ou plusieurs objets dans le cas
        contraire.

        """
        if type_ou_prototype.startswith("+"):
            type_ou_prototype = type_ou_prototype[1:]
            type_objet = importeur.objet.get_type(type_ou_prototype)
            return [o for o in objets if o.est_de_type(type_ou_prototype)]

        prototype = importeur.objet.prototypes[type_ou_prototype]
        return [o for o in objets if isinstance(o, prototype)]

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


"""Fichier contenant la fonction nom_objet."""

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Retourne le nom singulier ou pluriel d'un objet."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.nom_objet, "str", "Fraction")
        cls.ajouter_types(cls.nom_objet, "str", "Fraction", "str")
        cls.ajouter_types(cls.nom_objet2, "Objet", "Fraction")
        cls.ajouter_types(cls.nom_objet2, "Objet", "Fraction", "str")

    @staticmethod
    def nom_objet(cle_prototype, nombre, flags=""):
        """Retourne le nom singulier ou pluriel de l'objet précisé.

        Paramètres :

          * cle_prototype : la clé du prototype d'objet, sous la forme d'une chaîne
          * nombre : la quantité de l'objet
          * flags (optionnel) : les flags sous la forme d'une chaîne

        Flags disponibles :

          * "ra" : retire l'article du nom (le premier mot)

        Exemple d'utilisation :

          nom = nom_objet("carotte_crue", 8)
          # nom devrait contenir quelque chose comme "8 carottes crues"
          nom = nom_objet("carotte_crue", 8, "ra")
          # Cette fois, nom devrait contenir "carottes crues"

        """
        try:
            prototype = importeur.objet.prototypes[cle_prototype]
        except KeyError:
            raise ErreurExecution("prototype d'objet introuvable : {}".format(
                    repr(cle_prototype)))

        nom = prototype.get_nom(int(nombre), pluriels=False)
        flags = flags.lower().split(" ")
        for flag in flags:
            if flag == "ra":
                nom = " ".join(nom.split(" ")[1:])

        return nom

    @staticmethod
    def nom_objet2(objet, nombre, flags=""):
        """Retourne le nom singulier ou pluriel de l'objet précisé.

        Paramètres à préciser :

          * objet : l'objet concerné
          * nombre : la quantité de l'objet
          * flags (optionnel : les flags de transformation à appliquer

        Liste des flags :

          * "ra" : retire l'article (le premier mot) du nom

        Exemple d'utilisation :

          nom = nom_objet(objet, 8)
          # nom devrait contenir quelque chose comme "8 carottes crues"
          nom = nom_objet(objet, 8, "ra")
          # Cette fois, 'nom' contient "carottes crues"

        """
        nom = objet.get_nom(int(nombre), pluriels=False)
        flags = flags.lower().split(" ")
        for flag in flags:
            if flag == "ra":
                nom = " ".join(nom.split(" ")[1:])

        return nom

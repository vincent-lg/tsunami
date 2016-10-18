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


"""Fichier contenant la fonction a_tag."""

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Retourne vrai si a le tag spécifié."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.a_tag_salle, "Salle", "str")
        cls.ajouter_types(cls.a_tag_personnage, "Personnage", "str")
        cls.ajouter_types(cls.a_tag_objet, "Objet", "str")

    @staticmethod
    def a_tag_salle(salle, tags):
        """Retourne vrai si la salle a le tag, faux sinon.

        Paramètres à préciser :

          * salle : la salle qu'on veut tester ;
          * tags : un ou plusieurs tags (une chaîne).

        On peut tester plusieurs tags en les séparant par une barre
        verticale (|). Dans ce cas, la fonction retournera vrai si
        la salle a au moins un des tags précisés.

        Exemple d'utilisation :

          si a_tag(salle, "exploration"):
              ...
          finsi
          si a_tag(salle, "tag1|tag2"):
              ...
          finsi

        """
        o_tags = importeur.tags.configuration[salle].tags
        return any(tag.lower() in o_tags for tag in tags.split("_b_"))

    @staticmethod
    def a_tag_personnage(pnj, tags):
        """Retourne vrai si le PNJ a le tag, faux sinon.

        Paramètres à préciser :

          * pnj : le PNJ qu'on veut tester ;
          * tags : un ou plusieurs tags (une chaîne).

        On peut tester plusieurs tags en les séparant par une barre
        verticale (|). Dans ce cas, la fonction retournera vrai si
        le PNJ a au moins un des tags précisés.

        Exemple d'utilisation :

          si a_tag(pnj, "marchand"):
              ...
          finsi
          si a_tag(pnj, "tag1|tag2"):
              ...
          finsi

        """
        pnj = getattr(pnj, "prototype", pnj)
        o_tags = importeur.tags.configuration[pnj].tags
        return any(tag.lower() in o_tags for tag in tags.split("_b_"))

    @staticmethod
    def a_tag_objet(objet, tags):
        """Retourne vrai si l'objet a le tag, faux sinon.

        Paramètres à préciser :

          * objet : l'objet qu'on veut tester ;
          * tags : un ou plusieurs tags (une chaîne).

        On peut tester plusieurs tags en les séparant par une barre
        verticale (|). Dans ce cas, la fonction retournera vrai si
        l'objet a au moins un des tags précisés.

        Exemple d'utilisation :

          si a_tag(objet, "unique"):
              ...
          finsi
          si a_tag(objet, "tag1|tag2"):
              ...
          finsi

        """
        o_tags = importeur.tags.configuration[objet.prototype].tags
        return any(tag.lower() in o_tags for tag in tags.split("_b_"))

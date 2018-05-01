# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
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


"""Fichier contenant l'action ajouter_chapitre"""

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Ajoute un chapitre à un livre."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.ajouter_chapitre, "str", "str", "str")
        cls.ajouter_types(cls.ajouter_chapitre_prototype, "PrototypeObjet",
                "str", "str")

    @staticmethod
    def ajouter_chapitre(cle_livre, titre, texte):
        """Ajoute un chapitre au livre précisé en paramètre.

        Paramètres à préciser :

          * cle_livre : la clé identifiant le prototype d'objet de type livre ;
          * titre : une chaîne de caractères contenant le titre du chapitre ;
          * texte : une chaîne de caractères contenant le texte du chapitre.

        Cette action modifie les chapitres du prototype d'objet. Tous
        les objets créés sur ce prototype sont donc affectés.

        Exemple d'utilisation :

          ajouter_chapitre "chants_noel" "Jingle bells" "Dashin' through the snow"

        """
        cle_livre = cle_livre.lower()
        try:
            livre = importeur.objet.prototypes[cle_livre]
        except KeyError:
            raise ErreurExecution("le prototype d'objet {} est " \
                    "introuvable".format(repr(cle_livre)))

        if not livre.est_de_type("livre"):
            raise ErreurExecution("le prototype d'objet {} n'est pas " \
                    "de type livre".format(repr(cle_livre)))

        chapitre = livre.ajouter_chapitre(titre)
        texte = texte.replace("_b_nl_b_", "\n")
        chapitre.description.paragraphes[:] = texte.split("\n")

    @staticmethod
    def ajouter_chapitre_prototype(livre, titre, texte):
        """Ajoute un chapitre au livre précisé en paramètre.

        Paramètres à préciser :

          * livre : le prototype d'objet de type livre à modifier ;
          * titre : une chaîne de caractères contenant le titre du chapitre ;
          * texte : une chaîne de caractères contenant le texte du chapitre.

        Cette action modifie les chapitres du prototype d'objet. Tous
        les objets créés sur ce prototype sont donc affectés.

        Exemple d'utilisation :

          ajouter_chapitre "chants_noel" "Jingle bells" "Dashin' through the snow"

        """
        if not livre.est_de_type("livre"):
            raise ErreurExecution("le prototype d'objet {} n'est pas " \
                    "de type livre".format(repr(cle_livre)))

        chapitre = livre.ajouter_chapitre(titre)
        texte = texte.replace("_b_", "|")
        texte = texte.replace("|nl|", "\n")
        chapitre.description.paragraphes[:] = texte.split("\n")

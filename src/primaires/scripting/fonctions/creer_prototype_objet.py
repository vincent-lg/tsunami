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


"""Fichier contenant la fonction creer_prototype_objet."""

from corps.fonctions import valider_cle
from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Crée un prototype d'objet."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.creer_prototype_objet, "str", "str")

    @staticmethod
    def creer_prototype_objet(prototype, type):
        """Crée un prototype d'objet du type précisé.

        Cette fonction permet de créer un prototype d'objet du type
        indiqué. Le prototype d'objet est retourné et peut être
        manipulé pour d'avantage de configuration (voire les exemples
        ci-dessous). La clé précisée est utilisée telle quelle. Si
        un prototype d'objet de cette clé existe déjà, cependant, le
        système va essayer de créer la clé ${cle}_2, ${cle}_3 et ainsi
        de suite, jusqu'à en trouver une libre.

        Si la clé de prototype précisée finit par "_X", (le signe
        souligné suivi de la lettre X), le système cherchera le prototype
        correspondant en remplaçant X par un nombre (ce qui est souvent
        un comportement plus logique quand on veut créer des
        prototypes en série).

        Paramètres à préciser :

          * prototype : la clé du prototype à créer (une chaîne de caractères) ;
          * type : le nom du type (une chaîne de caractères).

        Exemples d'utilisation :

          prototype = creer_prototype_objet("pomme_rouge", "fruit")
          # Si un prototype d'objet de la clé 'pomme_rouge' existe
          # déjà, le système créra le prototype 'pomme_rouge_2'
          journal = creer_prototype_objet("journal_X", "livre")
          # Le système cherchera à créer le prototype d'objet 'journal_1'.
          # Si la clé existe, alors 'journal_2', 'journal_3' et ainsi
          # de suite.
          changer_nom journal "un journal" "journaux"
          changer_etat journal "est posé là" "sont posés là"
          changer_description journal "C'est un journal."
          changer_poids journal 0.2
          changer_prix journal 50
          ajouter_chapitre journal "Chapitre 1" "C'est le chapitre 1."
          ...

        """
        type = importeur.objet.get_type(type).nom_type
        cles = tuple(importeur.objet.prototypes.keys())
        prototype = prototype.lower()
        nb = 1
        cle = prototype
        if prototype.endswith("_x"):
            prototype = prototype[:-2]
            cle = prototype + "_1"

        valider_cle(prototype)
        while cle in cles:
            nb += 1
            cle = "{}_{}".format(prototype, nb)

        return importeur.objet.creer_prototype(cle, type)

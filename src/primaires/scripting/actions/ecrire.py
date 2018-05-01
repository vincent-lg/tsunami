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


"""Fichier contenant l'action ecrire."""

from corps.fonctions import valider_cle
from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """écrit une information dans une structure."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.ecrire, "Structure", "str", "object")

    @staticmethod
    def ecrire(structure, cle, valeur):
        """Écrit l'information dans la structure indiquée.

        Paramètres à préciser :

          * structure : la structure à modifier
          * cle : la clé de la case à modifier
          * valeur : la valeur de la case à écrire (tous types acceptés)

        Exemple d'utilisation :

          ecrire structure "nom" "Quelque chose"
          ecrire structure "numero" 5
          ecrire structure "elements" liste(1, 2, 3, 8)
          ecrire structure "coupable" joueur("Kredh")

        **ATTENTION** : la clé de case doit être une clé (sans
        majuscules ni accents, ne comprenant que des lettres et
        des chiffres, ainsi que le signe souligné _, si il n'est
        pas en début de mot). Les noms suivants sont par ailleurs interdits :

          "e_existe", "get_nom_pour", "id", "structure"

        """
        valider_cle(cle)

        if cle.startswith("_"):
            raise ErreurExecution("la clé précisée {} commence par " \
                    "un signe souligné".format(repr(cle)))

        interdits = ("e_existe", "get_nom_pour", "id", "structure")
        if cle in interdits:
            raise ErreurExecution("Ce nom de clé est interdit. Clés " \
                    "interdites : {}.".format(repr(interdits)))

        setattr(structure, cle, valeur)

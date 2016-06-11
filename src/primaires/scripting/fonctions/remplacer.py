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


"""Fichier contenant la fonction remplacer."""

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Remplace un morceau de chaîne par une autre."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.remplacer, "str", "str", "str")

    @staticmethod
    def remplacer(origine, recherche, remplacement):
        """Remplace une partie de la chaîne indiquée.

        Paramètres à préciser :

          * origine : la chaîne d'origine, celle qui sera modifiée
          * recherche : la chaîne à rechercher
          * remplacement : la chaîne qui doit remplacer la recherche

        Exemple d'utilisation :

          chaine = "C'est une phrase contenant le mot pigeon."
          chaine = remplacer(chaine, "pigeon", "carad")
          # 'chaine' contient à présent
          # "C'est une phrase contenant le mot canard."

        La partie à remplacer peut se trouver n'importe où dans la
        chaîne, au début, milieu ou à la fin. Elle peut se trouver
        plusieurs fois. La recherche est sensible aux majuscules
        et accents.

        """
        return origine.replace(recherche, remplacement)

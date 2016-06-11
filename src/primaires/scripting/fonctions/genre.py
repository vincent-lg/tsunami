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


"""Fichier contenant la fonction genre."""

from primaires.format.fonctions import supprimer_accents
from primaires.scripting.fonction import Fonction

class ClasseFonction(Fonction):

    """Retourne le genre d'un personnage."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.genre, "Personnage")

    @staticmethod
    def genre(personnage):
        """Retourne le nom du genre du personnage.

        Paramètres à préciser :

          * personnage : le personnage dont on veut avoir le genre

        Le genre retourné est une chaîne, soit "aucun" (aucun genre), soit
        "feminin" (sans accent, genre féminin), soit "masculin".

        Exemples d'utilisation :

          genre = genre(personnage)
          # genre est maintenant une chaîne
          si genre = "aucun":
              # aucun genre
          sinon si genre = "feminin":
              # notez le "feminin" (sans accent)
          sinon si genre = "masculin":
              # masculin

          # On peut bien évidemment aussi faire :
          si genre(personnage) = "feminin":
              # Genre féminin
          sinon:
              # Genre masculin ou aucun

        """
        return supprimer_accents(personnage.genre)

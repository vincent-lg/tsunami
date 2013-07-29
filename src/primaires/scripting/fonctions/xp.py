# -*-coding:Utf-8 -*

# Copyright (c) 2013 LE GOFF Vincent
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


"""Fichier contenant la fonction xp."""

from fractions import Fraction

from primaires.scripting.fonction import Fonction

class ClasseFonction(Fonction):

    """Retourne l'XP d'un PNJ passé en paramètre."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.xp, "Personnage")

    @staticmethod
    def xp(pnj):
        """Retourne le gain d'XP absolu que le bénéficiaire doit récupérer.

        Les paramètres à entrer sont :

          * pnj : le PNJ (la victime)

        ATTENTION : cette fonction ne donne pas de l'XP, elle retourne
        simplement l'XP sous la forme d'un nombre absolu.

        Voici un exemple d'utilisation :

          xp = xp(pnj)
          donner_xp personnage "combat" xp

        """
        if pnj.gain_xp:
            xp = importeur.perso.gen_niveaux.grille_xp[pnj.niveau][1]
            xp = xp * pnj.gain_xp / 100
            return Fraction(xp)

        raise ErreurExecution("{} n'a pas de gain d'XP, est-ce bien un " \
                "PNJ ?".format(pnj))

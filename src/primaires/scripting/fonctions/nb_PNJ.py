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


"""Fichier contenant la fonction nb_PNJ."""

from fractions import Fraction

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Retourne le nombre de PNJ."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.PNJ_proto, "str")
        cls.ajouter_types(cls.PNJ_salle, "Salle", "str")

    @staticmethod
    def PNJ_proto(cle_prototype):
        """Retourne le nombre de PNJ modelés sur ce prototype.

        Le paramètre à entrer est la clé du prototype sous la forme
        d'une chaîne.

        Par exemple :

            nb_PNJ("rat_picte")

        Si le prototype de PNJ est introuvable, crée une alerte.

        """
        try:
            prototype = importeur.pnj.prototypes[cle_prototype]
        except KeyError:
            raise ErreurExecution("prototype inconnu {}".format(
                    repr(cle_prototype)))

        return Fraction(len(prototype.pnj))

    @staticmethod
    def PNJ_salle(salle, cle_prototype):
        """Retourne le nombre de PNJ présents dans la salle.

        Paramètres à préciser :

          * salle : la salle dans laquelle chercher le ou les PNJ
          * cle_prototype : la clé du prototype de PNJ.

        Par exemple, si vous faites apparaître un prototype
        'lapin' dans la salle :

          nb = nb_PNJ(salle, "lapin")
          # nb baut 1

        """
        try:
            prototype = importeur.pnj.prototypes[cle_prototype]
        except KeyError:
            raise ErreurExecution("prototype inconnu {}".format(
                    repr(cle_prototype)))

        pnjs = [p for p in prototype.pnj if p.salle is salle]
        return Fraction(len(pnjs))

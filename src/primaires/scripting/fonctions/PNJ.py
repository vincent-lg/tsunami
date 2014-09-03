# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Fichier contenant la fonction PNJ."""

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Retourne tous les PNJ présents."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.PNJ_salle, "Salle")
        cls.ajouter_types(cls.tous_PNJ, "str")

    @staticmethod
    def PNJ_salle(salle):
        """Retourne tous les PNJ présents dans la salle.

        Cette fonction retourne les PNJ présents (pas les joueurs).

        """
        return salle.PNJ

    @staticmethod
    def tous_PNJ(cle_prototype):
        """Retourne tous les PNJ d'un prototype.

        Paramètres à préciser :

          * cle_prototype : la clé du prototype de PNJ

        Vous devez préciser la clé du prototype sous la
        forme d'une chaîne. Une liste contenant tous les
        PNJ du prototype, peu importe l'endroit où ils
        se trouvent, sera retournée. La liste sera
        vide si le prototype n'a aucun PNJ créé
        actuellement. Vous pouvez partir du principe que
        tous les PNJ retournés sont vivants (ceux morts
        sont automatiquement supprimés).

        Utilisez la fonction 'salle' pour connaître la
        salle dans laquelle un PNJ se trouve.

        Exemple d'utilisation :

          pour chaque pnj dans PNJ("marchand_myr"):
              salle = salle(pnj)
              # salle contient la salle du PNJ parcouru

        """
        try:
            prototype = importeur.pnj.prototypes[cle_prototype.lower()]
        except KeyError:
            raise ErreurExecution("prototype inconnu {}".format(
                    repr(cle_prototype)))

        return list(prototype.pnj)

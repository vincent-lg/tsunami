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


"""Fichier contenant la fonction quetes."""

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Permet d'interroger les niveaux de quête d'un personnage."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.quetes_personnage, "Personnage", "str", "str")

    @staticmethod
    def quetes_personnage(personnage, cle_de_quete, niveau):
        """Retourne vrai si le personnage a fait la quête, faux sinon.

        Les paramètres à entrer sont :
          * Le personnage à tester
          * La clé de la quête
          * Le niveau testé (sous la forme d'une chaîne, comme "1.2")
        Vous pouvez préciser plusieurs niveaux sous à l'aide du pipe |
        (par exemple "1|2|3.1|3.2").

        """
        niveau = niveau.split("_b_")
        try:
            niveau = [tuple(int(v) for v in n.split(".")) for n in niveau]
        except ValueError:
            raise ErreurExecution("niveau spécifié invalide {}".format(
                    niveau))
        faits = []
        if personnage.quetes[cle_de_quete].niveaux != [(0, )]:
            faits = personnage.quetes[cle_de_quete].niveaux
        if all(n in faits for n in niveau):
            return True
        return False

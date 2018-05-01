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


"""Fichier contenant la fonction peut_faire."""

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Teste si un personnage peut faire la quête."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.quetes_personnage, "Personnage", "str", "str")

    @staticmethod
    def quetes_personnage(personnage, cle_de_quete, niveau):
        """Retourne vrai si le personnage peut faire la quête, faux sinon.

        Les paramètres à entrer sont :

          * Le personnage à tester
          * La clé de la quête
          * Le niveau testé (sous la forme d'une chaîne, comme "1.2")

        """
        try:
            t_niveau = tuple(int(v) for v in niveau.split("."))
        except ValueError:
            raise ErreurExecution("niveau spécifié invalide {}".format(
                    niveau))

        quete = personnage.quetes[cle_de_quete]
        template = importeur.scripting.quetes[cle_de_quete].etapes.get(niveau)
        if template is None:
            return False
        elif template.parent:
            template = template.parent

        return quete.peut_faire(template, t_niveau)

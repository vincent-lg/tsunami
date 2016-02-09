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


"""Fichier contenant la fonction oui_ou_non."""

from primaires.format.fonctions import oui_ou_non
from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Retourne la chaîne "oui" ou "non"."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.oui_ou_non, "object")

    @staticmethod
    def oui_ou_non(valeur):
        """Retourne "oui" si la valeur est vraie, "non" sinon.

        0 est toujours faux. 1 ou n'importe quel nombre est toujours
        vrai. Une valeur nulle est fausse. Une liste vide est fausse.
        Une information quelconque est toujours vraie (voir les
        exemples ci-dessous).

        Paramètres à préciser :

          * valeur : la valeur, sous la forme d'un nombre ou autre.

        Exemples d'utilisation :

          retour = oui_ou_non(1)
          # retour contient "oui"
          retour = oui_ou_non(0)
          # retour contient "non"
          retour = oui_ou_non(liste())
          # retour contient "non"

        """
        return oui_ou_non(bool(valeur))

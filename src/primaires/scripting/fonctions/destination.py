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


"""Fichier contenant la fonction destination."""

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Retourne la destination d'une sortie."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.destination, "Salle", "str")

    @staticmethod
    def destination(salle, nom_sortie):
        """Retourne la destination de la sortie indiquée.

        Paramètres à préciser :

          * salle : la salle dans laquelle on doit trouver la sortie
          * nom_sortie : le nom de la sortie

        Si trouvé, retourne la salle de destination de la sortie. Si la
        sortie n'existe pas, une alerte est créée. Vérifiez donc que la
        sortie existe :

          si sortie_existe(salle, "porte"):
              destination = destination(salle, "porte")

        """
        try:
            sortie = salle.sorties.get_sortie_par_nom_ou_direction(nom_sortie)
            assert sortie is not None
            assert sortie.salle_dest is not None
        except (KeyError, AssertionError):
            raise ErreurExecution("la sortie {} dans la salle {} ne " \
                    "peut être trouvée.".format(repr(nom_sortie), salle))

        return sortie.salle_dest

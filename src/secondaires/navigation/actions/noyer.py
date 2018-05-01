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


"""Fichier contenant l'action noyer."""

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Essaye de noyer une salle de navire."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.noyer, "Salle", "Fraction")

    @staticmethod
    def noyer(salle, degats):
        """Noie une salle de navire.

        Les dégâts précisés sont sous la forme de kilos : si vous
        entrez des dégâts de 50 et que la salle est noyable, la
        salle indiquée aura une brèche qui laissera entrer 50 kilos
        (plus ou moins 50 litres) d'eau. Si la salle n'est pas
        noyable, rien ne se passe. Si la salle n'est pas une salle
        de navire, une alerte est créée.

        Paramètres à renseigner :

          * salle : la salle de navire à noyer
          * degats : les dégâts sous la forme d'un nombre

        Exemple d'utilisation :

          noyer salle 30

        """
        if not hasattr(salle, "noyer"):
            raise ErreurExecution("La salle {} n'est pas une salle " \
                    "de navire".format(salle))

        salle.noyer(int(degats))

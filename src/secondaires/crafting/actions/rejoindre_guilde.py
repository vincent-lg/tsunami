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


"""Fichier contenant l'action rejoindre_guilde."""

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Fait rejoindre une guilde à un personnage."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.rejoindre_guilde, "Personnage", "str")

    @staticmethod
    def rejoindre_guilde(personnage, cle_guilde):
        """Fait rejoindre la guilde au personnage.

        Cette action crée une alerte si le personnage ne peut
        rejoindre la guilde (si il n'a pas assez de points de guilde,
        par exemple). Si l'action réussit, le personnage se retrouve
        dans le premier rang de la guilde à 0% d'avancement.

        Paramètres à renseigner :

          * personnage : le personnage (futur membre)
          * cle_guilde : la clé de la guilde (une chaîne)

        Exemple d'utilisation :

          rejoindre_guilde personnage "forgerons"

        """
        cle_guilde = cle_guilde.lower()
        if cle_guilde not in importeur.crafting.guildes:
            raise ErreurExecution("La guilde {} n'existe pas".format(
                    repr(cle_guilde)))

        guilde = importeur.crafting.guildes[cle_guilde]
        guilde.rejoindre(personnage)

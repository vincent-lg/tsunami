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


"""Fichier contenant l'action planter."""

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Plante un végétal dans une salle."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.planter, "Salle", "str")
        cls.ajouter_types(cls.planter, "Salle", "str", "Fraction")

    @staticmethod
    def planter(salle, cle_plante, nombre=1):
        """Plante un végétal dans la salle.

        Paramètres à préciser :

          * salle : la salle dans laquelle planter
          * cle_plante : la clé du végétal à planter
          * nombre (optionnel) : le nombre de plantes à planter (1 par défaut)

        Exemples d'utilisation :

          # Plante un pommier sauvage dans la salle
          planter salle "pommier_sauvage"
          # Plante 3 pommiers sauvages dans la salle
          planter salle "pommier_sauvage" 3

        """
        prototype = importeur.botanique.prototypes.get(cle_plante.lower())
        if prototype is None:
            raise ErreurExecution("le végétal {} n'existe pas".format(
                    repr(cle_plante)))

        nombre = int(nombre)
        nombre = 1 if nombre <= 0 else nombre
        for i in range(nombre):
            plante = importeur.botanique.creer_plante(prototype, salle)
            plante.ajuster()

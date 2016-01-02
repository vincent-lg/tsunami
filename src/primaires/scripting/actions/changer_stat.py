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


"""Fichier contenant l'action changer_stat."""

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Change la stat d'un personnage."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.changer_stat, "Personnage", "str", "Fraction")

    @staticmethod
    def changer_stat(personnage, nom_stat, valeur):
        """Modifie la stat d'un personnage.

        Cette action doit être de préférence utilisée pour augmenter
        les stats d'un personnage. Pour consommer des stats particulières
        (comme la vitalité ou l'endurance), utilisez l'action
        'consommer'.

        Paramètres à préciser :

          * personnage : le personnage dont on veut modifier la stat
          * nom_stat : le nom de la stat
          * valeur : la valeur de la nouvelle stat

        Exemples d'utilisation :

          changer_stat personnage "force" 90
          changer_stat personnage "vitalite_max" 2000
          changer_stat "mana" 80

        Note : n'utilisez pas cette action pour tuer un personnage
        (utilisez l'action 'tuer' pour ce faire).
        Si vous voulez modifier la stat max d'un personnage, utilisez
        "stat_max" (par exemple "vitalite_max"). Notez que les noms
        des stats sont en minuscule et sans accent.

        """
        valeur = int(valeur)
        if valeur <= 0:
            valeur = 1

        if nom_stat not in personnage.stats:
            raise ErreurExecution("stat {} inconnue".format(repr(nom_stat)))

        setattr(personnage.stats, nom_stat, valeur)

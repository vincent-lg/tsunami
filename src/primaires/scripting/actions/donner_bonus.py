# -*-coding:Utf-8 -*

# Copyright (c) 2013 LE GOFF Vincent
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


"""Fichier contenant l'action donner_bonus."""

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution
from primaires.format.fonctions import supprimer_accents

class ClasseAction(Action):

    """Donne ou retire des bonus temporaires à un personnage.

    Cette action permet de donner ou retirer des bonus à un personnage
    dans une stat précise (par exemple, augmenter son agilité pendant
    10 minutes).

    """

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.donner_bonus, "Personnage", "str",
                "Fraction")

    @staticmethod
    def donner_bonus(personnage, nom_stat, points):
        """Donne ou retire un bonus dans la stat indiquée.

        Les paramètres à préciser sont :

          * personnage : le personnage ciblé par le bonus
          * nom_stat : le nom de la stat (par exemple "force")
          * points : le nombre de points à ajouter ou retirer.

        NOTE IMPORTANTE : cette action modifie la partie variable
        de la stat du personnage. Concrètement, cela signifie que vous
        devez l'appeler deux fois : une fois pour donner le bonus, une
        fois pour le retirer. Retirer le bonus se fait en spécifiant un
        nombre négatif de points. Par exemple, si vous voulez faire
        une affection qui donne 10 points de force, vous devrez faire
        comme ceci :

            donner_bonus personnage "force" 10

        Et quand l'affection se détruit:

            donner_bonus personnage "force" -10

        Dans le cas contraire le bonus sera maintenu éternellement.

        """
        nom_stat = supprimer_accents(nom_stat)
        points = int(points)
        variable = personnage.stats[nom_stat].variable
        personnage.stats[nom_stat].variable = variable + points

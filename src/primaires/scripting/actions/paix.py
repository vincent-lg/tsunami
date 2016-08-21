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
# LIABLE FOR ANY paixCT, INpaixCT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant l'action paix."""

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Termine le combat ou retire un combattant."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.paix_salle, "Salle")
        cls.ajouter_types(cls.paix_personnage, "Personnage")

    @staticmethod
    def paix_salle(salle):
        """Termine le combat dans la salle.

        Cette action est identique à la commande paix/peace. Elle
        interrompt le combat dans la salle précisée en paramètre. Tous
        les personnages sont libérés du combat et peuvent se déplacer
        normalement.
        Si il n'y a pas de combat dans la salle, aucune alerte n'est créée.

        Paramètres à préciser :

          * salle : La salle dans laquelle on veut interrompre le combat.

        Exemple d'utilisation :

          paix salle

        """
        if salle.ident in importeur.combat.combats:
            importeur.combat.supprimer_combat(salle.ident)

    @staticmethod
    def paix_personnage(personnage):
        """Retire le personnage précisé du combat dans sa salle.

        Cette action permet de retirer un combattant du combat en
        cours dans cette salle. Cette action peut avoir pour conséquence
        d'interrompre le combat pour d'autres personnages. Si par
        exemple, un combat a lieu entre A et B, et qu'on interrompt le
        combat pour B, alors A n'a plus d'adversaire et arrête de
        combattre.
        Si il n'y a aucun combat dans cette salle, ou bien que le
        personnage précisé ne combat pas, aucune alerte n'est créée.

        Paramètres à préciser :

          * personnage : le personnage à retirer du combat.

        Exemple d'utilisation :

          paix personnage

        """
        salle = personnage.salle
        if salle is None:
            return

        combat = importeur.combat.combats.get(salle.ident)
        if combat is None:
            return

        combat.supprimer_combattant(personnage)

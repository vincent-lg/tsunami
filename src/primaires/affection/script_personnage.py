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


"""Fichier contenant la classe ScriptAffectionPersonnage détaillée plus bas."""

from primaires.affection.script import ScriptAffection

class ScriptAffectionPersonnage(ScriptAffection):

    """Script et évènements propre aux affections personnage.

    C'est dans cette classe que sont construits les évènements du scripting
    des affections de personnage. Elle hérite de ScriptAffection et
    propose les mêmes scripts de base mais aussi quelques évènements
    en plus.

    """

    def init(self):
        """Initialisation du script"""
        ScriptAffection.init(self)

        # Évènement sort
        evt_sort = self.creer_evenement("sort")
        evt_sort.aide_courte = "avant que le personnage ne quitte la salle"
        evt_sort.aide_longue = \
            "Cet évènement est appelé quand le personnage affecté " \
            "quitte une salle. L'affection peut ainsi être détruite si " \
            "le personnage bouge, ou au contraire la renforcer. Cet " \
            "évènement est appelé avant que le personnage ne quitte " \
            "la salle, donc il peut être empêché de bouger si nécessaire."
        var_salle = evt_sort.ajouter_variable("salle", "Salle")
        var_salle.aide = "la salle que quitte le personnage"

        # Ajout de la variable personnage
        for evt in self.evenements.values():
            var_perso = evt.ajouter_variable("personnage", "Personnage")
            var_perso.aide = "le personnage subissant l'affection"

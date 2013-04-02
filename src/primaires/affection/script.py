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


"""Fichier contenant la classe ScriptAffection détaillée plus bas."""

from primaires.scripting.script import Script

class ScriptAffection(Script):

    """Script et évènements propre aux affections.

    C'est dans cette classe que sont construits les évènements du scripting
    des affections. C'est la classe commune aux différents types
    d'affections (personnage et salle). Il existe une affection de
    sous-type pour chacun des types d'affections ce qui permet d'ajouter
    des évènements propres à certains types d'affections uniquement.

    """

    def init(self):
        """Initialisation du script"""
        # Évènement détruit
        evt_detruit = self.creer_evenement("détruit")
        evt_detruit.aide_courte = "l'affection se détruit"
        evt_detruit.aide_longue = \
            "Cet évènement est appelé quand l'affection doit se " \
            "détruire, généralement parce que sa durée est descendue " \
            "à 0. Il est aussi appelé quand on demande à l'affection " \
            "de se détruire par script."

        # Évènement tick
        evt_tick = self.creer_evenement("tick")
        evt_tick.aide_courte = "chaque tick de l'affection"
        evt_tick.aide_longue = \
            "Cet évènement est appelé à chaque tick de l'affection " \
            "tant qu'elle existe. Les ticks peuvent être d'une minute " \
            "(60 secondes) mais peuvent être plus courts. Cet évènement " \
            "n'est donc pas strictement appelé toutes les minutes " \
            "(clla dépend de la configuration de l'affection)."

        # Évènement valide
        evt_valide = self.creer_evenement("valide")
        evt_valide.aide_courte = "vérifie que l'affection est valide"
        evt_valide.aide_longue = \
            "Cet évènement est appelé toutes les minutes tant que " \
            "l'affection existe. Il permet de vérifier la validité de " \
            "l'affection (éventuellement varier sa force ou sa durée si " \
            "nécessaire). Attention cependant, cet avènement ne doit " \
            "pas être utilisé pour des traitements répétés sur " \
            "l'affection : notez que chaque affection a un temps de tick " \
            "(en secondes) et que c'est dans ce tick que les actions " \
            "ponctuelles (comme afficher des messages, diminuer certaines " \
            "statistiques ou autre) doivent être faites."

        # Configuration des variables communes aux évènements
        for evt in self.evenements.values():
            var_force = evt.ajouter_variable("force", "Fraction")
            var_force.aide = "la force de l'affection"
            var_duree = evt.ajouter_variable("duree", "Fraction")
            var_duree.aide = "la durée de l'affection"

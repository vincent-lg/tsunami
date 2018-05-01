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


"""Fichier contenant la classe ScriptFiche détaillée plus bas."""

from primaires.scripting.script import Script

class ScriptFiche(Script):

    """Script et évènements propre aux fiches de familier."""

    def init(self):
        """Initialisation du script"""
        # Evénement apprivoiser
        evt_appr = self.creer_evenement("apprivoiser")
        evt_appr_avant = evt_appr.creer_evenement("avant")
        evt_appr_reus = evt_appr.creer_evenement("réussir")
        evt_appr_echoue = evt_appr.creer_evenement("échoue")
        evt_appr_avant.aide_courte = "avant que le personnage ne tente d'apprivoiser le pnj"
        evt_appr.aide_courte = "un personnage apprivoise le familier"
        evt_appr_reus.aide_courte = "l'apprivoisement réussi"
        evt_appr_echoue.aide_courte = "l'apprivoisement échoue"
        evt_appr.aide_longue = \
            "Cet évènement est appelé quand un personnage, joueur ou PNJ, " \
            "apprivoise un familier. Deux sous-évènements différents " \
            "sont appelés si il réussi ou échoue l'apprivoisement."
        evt_appr_avant.aide_longue = \
        "Cet évènement est appelé avant que le personnage " \
        " ne tente d'apprivoiser le pnj."
        evt_appr_reus.aide_longue = \
            "Cet évènement est appelé quand le personnage réussi à " \
            "apprivoiser le familier."
        evt_appr_echoue.aide_longue = \
            "Cet évènement est appelé quand le personnage n'arrive pas à " \
            "apprivoiser le familier."

        # Configuration des variables de l'évènement apprivoiser
        var_perso = evt_appr.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage qui apprivoise"
        var_pnj = evt_appr.ajouter_variable("familier", "PNJ")
        var_pnj.aide = "le familier, un PNJ"

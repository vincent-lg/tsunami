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


"""Module contenant la classe PromptMonture, détaillée plus bas."""

from collections import namedtuple

from primaires.perso.prompt import Prompt

# Stats vides
Stats = namedtuple("stats",
        ["vitalite", "vitalite_max", "mana", "mana_max",
        "endurance", "endurance_max"])

class PromptMonture(Prompt):

    """Classe représentant le prompt affiché en chevauchant."""

    nom = "monture"
    nom_anglais = "mount"
    defaut = "Vit   {stats.vitalite}     Man   {stats.mana} " \
            "    End   {stats.endurance}{sl}{{{monture}}}   Vit   " \
            "{mstats.vitalite}     Man   {mstats.mana}     End   " \
            "{mstats.endurance}"

    aide_courte = "prompt de monture"
    aide_longue = "Ce prompt est affiché quand vous chevauchez une monture"
    symboles_sup = """
                %o          Nom de la monture chevauchée
                %ov         Vitalité de la monture chevauchée
                %ovx        Vitalité maximum de la monture chevauchée
                %om         Mana de la monture chevauchée
                %omx        Mana maximum de la monture chevauchée
                %oe         Endurance de la monture chevauchée
                %oex        Endurance maximum de la monture chevauchée
    """.strip("\n")

    symboles = Prompt.symboles.copy()
    symboles["o"] = "monture"
    symboles["ov"] = "mstats.vitalite"
    symboles["ovx"] = "mstats.vitalite_max"
    symboles["om"] = "mstats.mana"
    symboles["omx"] = "mstats.mana_max"
    symboles["oe"] = "mstats.endurance"
    symboles["oex"] = "mstats.endurance_max"

    @classmethod
    def calculer(cls, personnage, prompt):
        """Calcul et retourne le prompt calculé."""
        prompt = prompt if prompt is not None else cls.defaut
        nom_monture = "|att|inconnue|ff|"
        mstats = Stats('?', '?', '?', '?', '?', '?')
        etat = personnage.etats.get("chevauche")
        if etat and etat.monture:
            nom_monture = etat.monture.nom
            mstats = etat.monture.pnj.stats

        return prompt.format(
                stats=personnage.stats,
                sl="\n",
                monture=nom_monture,
                mstats=mstats,
            )

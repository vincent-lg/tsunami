# -*-coding:Utf-8 -*

# Copyright (c) 2015 LE GOFF Vincent
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


"""Module contenant la classe PromptCombat, détaillée plus bas."""

from primaires.perso.prompt import Prompt

class PromptCombat(Prompt):

    """Classe représentant le prompt affiché en combat."""

    nom = "combat"
    nom_anglais = "fighting"
    defaut = "[{pct_adv}] Vit   {stats.vitalite}     Man   {stats.mana} " \
            "    End   {stats.endurance}"
    aide_courte = "prompt de combat"
    aide_longue = "Ce prompt est affiché quand votre personnage est " \
            "en combat"
    symboles_sup = """
                    %p          Pourcentage de vitalité de l'adversaire
    """.strip("\n")

    symboles = Prompt.symboles.copy()
    symboles["p"] = "pct_adv"

    @classmethod
    def calculer(cls, personnage, prompt):
        """Calcul et retourne le prompt calculé."""
        prompt = prompt if prompt else cls.defaut
        pct_adv = "???%"
        salle = personnage.salle
        if salle:
            try:
                combat = importeur.combat.get_combat_depuis_salle(salle)
            except KeyError:
                personnage.deselectionner_prompt("combat")
            else:
                adversaire = combat.combattus.get(personnage)
                if adversaire:
                    pct_adv = round(adversaire.stats.vitalite / \
                            adversaire.stats.vitalite_max * 20) * 5
                    pct_adv = str(pct_adv).rjust(3) + "%"

        return prompt.format(stats=personnage.stats, pct_adv=pct_adv)

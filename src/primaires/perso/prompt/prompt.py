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


"""Module contenant la classe Prompt, détaillée plus bas."""

class Prompt:

    """Classe représentant un prompt abstrait.

    Créer une classe héritant de Prompt pour créer un nouveau prompt.
    Un prompt est une ou plusieurs lignes de texte qui apparaissent
    régulièrement (à pratiquement chaque entrée de commande ou chaque
    action de l'univers). Ce prompt donne généralement des informations
    par défaut sur l'état du joueur (comme sa vitalité actuelle). Ce
    prompt (dit prompt par défaut) peut être complété par d'autres
    prompts qui ne sont invoqués que dans des situations particulières.
    Par exemple, on pourrait avoir un prompt spécial combat.

    """

    nom = ""
    nom_anglais = ""
    defaut = "" # Prompt par défaut si le prompt n'a pas été changé
    aide_courte = ""
    aide_longue = ""
    symboles_sup = ""
    symboles = {
        "vx": "stats.vitalite_max",
        "mx": "stats.mana_max",
        "ex": "stats.endurance_max",
        "v": "stats.vitalite",
        "m": "stats.mana",
        "e": "stats.endurance",
        "f": "stats.force",
        "a": "stats.agilite",
        "r": "stats.robustesse",
        "i": "stats.intelligence",
        "c": "stats.charisme",
        "s": "stats.sensibilite",
    }

    @classmethod
    def calculer(cls, personnage, prompt):
        """Calcul et retourne le prompt calculé."""
        raise NotImplementedError

# -*-coding:Utf-8 -*

# Copyright (c) 2014 LE GOFF Vincent
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


"""Module contenant la classe MontrerScore, détiallée plus bas."""

# Chaîne représentant le score
chn_score = r"""
/----------------------------------------------\
| {nom: <15}      {nom_race:>12} ({genre:<8}) |
|                                              |
|    Vitalité   |     Mana    |   Endurance    |
|   {v: >5}/{vm: <5} | {m: >5}/{mm: <5} | {e: >5}/{em: <5}    |
|                                              |
|      For - Agi - Rob - Int - Cha - Sen       |
|      {f: >3} | {a: >3} | {r: >3} | {i: >3} | {c: >3} | {s: >3}       |
|                                              |
| Poids porté : {poids:>3} / {poids_max:>3} ({poids_pc:>3}%)               |
|                                              |
| Points d'apprentissage : {p_app:>4} / {p_app_max:>4}         |
|                                              |
| Points d'entraînement : {p_en:>4}                 |
|                                              |
| Points de tribut : {p_tr:>2}                        |
|                                              |
\----------------------------------------------/
"""

class MontrerScore:

    """Classe envelope d'affichage d'un score."""

    @staticmethod
    def montrer(personnage, **kwargs):
        """Retourne le score formatté du personnage spécifié."""
        nom_race = personnage.race and personnage.race.nom or "inconnue"
        poids = int(personnage.poids)
        poids_max = int(personnage.poids_max)
        poids_pc = int(poids / poids_max * 100)

        informations = {
            "nom": personnage.nom,
            "nom_race": nom_race,
            "genre": personnage.genre,
            "v": personnage.vitalite,
            "vm": personnage.vitalite_max,
            "m": personnage.mana,
            "mm": personnage.mana_max,
            "e": personnage.endurance,
            "em": personnage.endurance_max,
            "f": personnage.force,
            "a": personnage.agilite,
            "r": personnage.robustesse,
            "i": personnage.intelligence,
            "c": personnage.charisme,
            "s": personnage.sensibilite,
            "poids": poids,
            "poids_max": poids_max,
            "poids_pc": poids_pc,
            "p_app": personnage.points_apprentissage,
            "p_app_max": personnage.points_apprentissage_max,
            "p_en": personnage.points_entrainement,
            "p_tr": personnage.points_tribut,
        }

        informations.update(kwargs)
        return chn_score.format(**informations).strip()

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


"""Module contenant la classe PromptDefaut, détaillée plus bas."""

from primaires.perso.prompt import Prompt

class PromptDefaut(Prompt):

    """Classe représentant le prompt par défaut.

    Ce prompt est appelé dans les cas où il n'y a pas d'autre
    prompt actif.

    """

    nom = "défaut"
    nom_anglais = "default"
    defaut = "Vit   {stats.vitalite}     Man   {stats.mana}     End   " \
            "{stats.endurance}"
    aide_courte = "prompt par défaut"
    aide_longue = "Ce prompt est affiché si aucun autre prompt " \
            "n'est sélectionné"
    symboles = Prompt.symboles.copy()

    @classmethod
    def calculer(cls, personnage, prompt):
        """Calcul et retourne le prompt calculé."""
        prompt = prompt if prompt is not None else cls.defaut
        return prompt.format(stats=personnage.stats, sl="\n")

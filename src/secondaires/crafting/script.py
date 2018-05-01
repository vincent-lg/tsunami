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


"""Fichier contenant la classe ScriptGuilde détaillée plus bas."""

from primaires.scripting.script import Script

class ScriptGuilde(Script):

    """Script et évènements propre aux guildes.

    Il s'agit surtout d'une occasion de regrouper les blocs d'une
    certaine guilde dans un endroit plutôt que d'avoir beaucoup
    de scripts éparpillés.

    """

    def init(self):
        """Initialisation du script"""
        # Événement recette
        evt_recette = self.creer_evenement("recette")
        evt_recette.aide_courte = "évènement des recettes de guilde"
        evt_recette.aide_longue = \
            "Cet évènement regroupe les sous-évènement propres aux " \
            "recettes de la guilde."

        # Événement valide
        evt_valide = evt_recette.creer_evenement("valide")
        evt_valide.aide_courte = "la recette est-elle valide ?"
        evt_valide.aide_longue = \
            "Cet évènement permet de configurer génériquement le " \
            "statut valide ou invalide des recettes de la guilde. Si " \
            "cet évènement existe (et contient des instructions), il " \
            "est appelé pour chaque recette (la clé de la recette " \
            "est précisée en argument). Si ce n'est pas le cas, " \
            "l'évènement 'valide' de chaque recette est appelé. Dans " \
            "tous les cas, ces évènements doivent renseigner une " \
            "variable 'valide', vallant soit |ent|1|ff| (la recette est " \
            "valide), soit |ent|0|ff|."

        # Configuration des variables de l'évènement valide
        var_perso = evt_valide.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage fabriquant la recette"
        var_ingredients = evt_valide.ajouter_variable("ingredients", "list")
        var_ingredients.aide = "la liste des ingrédients (liste d'objets)"
        var_recette = evt_valide.ajouter_variable("recette", "str")
        var_recette.aide = "la clé de la recette valide ou non (une chaîne)"

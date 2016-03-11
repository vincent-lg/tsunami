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


"""Fichier contenant l'action copier_attributs."""

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Copie les attributs d'un objet vers un autre."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.copier_attributs, "Objet", "Objet")

    @staticmethod
    def copier_attributs(objet_origine, objet_final):
        """Copie les attributs d'un objet vers un autre.

        Paramètres à renseigner :

          * objet_origine : l'objet d'origine
          * objet_final : l'objet final, qui prend les attributs.

        Exemple de syntaxe :

          # Si 'objet1' et 'objet2' contiennent des objets
          copier_attributs objet1 objet2

        """
        attributs = importeur.crafting.configuration[objet_origine].attributs
        if attributs is None:
            attributs = {}

        if importeur.crafting.configuration[objet_final].attributs is None:
            importeur.crafting.configuration[objet_final].attributs = {}

        importeur.crafting.configuration[objet_final].attributs.update(
                attributs)

        for attribut, valeur in attributs.items():
            print(objet_final, "replace", attribut, valeur)
            objet_final.nom_singulier = objet_final.nom_singulier.replace(
                    "${}".format(attribut), valeur)
            objet_final.nom_pluriel = objet_final.nom_pluriel.replace(
                    "${}".format(attribut), valeur)

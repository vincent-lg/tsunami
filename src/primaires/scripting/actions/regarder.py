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


"""Fichier contenant l'action regarder."""

from primaires.scripting.action import Action

class ClasseAction(Action):

    """Regarde un élément de l'univers.

    Cette action est utilisée pour forcer un personnage à regarder
    un élément (la description de la salle où il se trouve, par exemple).

    """

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.regarder_salle, "Salle", "Personnage")

    @staticmethod
    def regarder_salle(salle, personnage):
        """Force le personnage spécifié à regarder la salle spécifiée.

        Les paramètres à entrer sont :

          * salle : la salle que le personnage doit regarder
          * personnage : le personnage regardant la salle

        Cette action ne vérifie pas que le personnage se trouve bel et
        bien dans la salle indiquée avant d'envoyer le titre, la
        description, les sorties et autres informations. Si cette
        vérification doit être faite, elle doit l'être dans le script
        qui utilise cette action.

        """
        personnage << salle.regarder(personnage)

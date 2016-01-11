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


"""Fichier contenant l'action changer_description."""

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Change la description de plusieurs choses."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.description_salle, "Salle", "str")
        cls.ajouter_types(cls.description_personnage, "Personnage", "str")
        cls.ajouter_types(cls.description_objet, "Objet", "str")
        cls.ajouter_types(cls.description_objet, "PrototypeObjet", "str")

    @staticmethod
    def description_salle(salle, description):
        """Change la description de la salle.

        Paramètres à entrer :

          * salle : la salle dont on veut changer la description ;
          * description : la nouvelle description (une chaîne).

        Cette action modifie la description d'une salle.
        Si la description est partagée par plusieurs salles (les
        descriptions de navire, par exemple, le sont souvent), toutes
        les salles partageant cette description sont modifiées.

        Exemple d'utilisation :

          changer_description salle "Vous êtes ici."

        """
        description = description.replace("_b_nl_b_", "\n")
        salle.description.paragraphes[:] = description.split("\n")

    @staticmethod
    def description_personnage(personnage, description):
        """Change la description du personnage.

        Paramètres à entrer :

          * personnage : le personnage dont on veut changer la description ;
          * description : la nouvelle description (une chaîne).

        Cette action modifie la description d'un personnage.

        Exemple d'utilisation :

          changer_description personnage "C'est une pomme."

        """
        description = description.replace("_b_nl_b_", "\n")
        personnage.description.paragraphes[:] = description.split("\n")

    @staticmethod
    def description_objet(prototype_ou_objet, description):
        """Change la description de l'objet ou de son prototype.

        Paramètres à entrer :

          * prototype_ou_objet : l'objet dont on veut changer la description ;
          * description : la nouvelle description (une chaîne).

        Cette action modifie la description d'un objet.
        Le prototype d'objet est modifié, ce qui modifie la description de
        tous les objets créés sur le même prototype, que l'on
        précise en premier paramètre un objet ou un prototype d'objet.

        Exemple d'utilisation :

          changer_description objet "C'est une pomme."

        """
        description = description.replace("_b_", "|")
        description = description.replace("|nl|", "\n")
        prototype_ou_objet.description.paragraphes[:] = description.split("\n")

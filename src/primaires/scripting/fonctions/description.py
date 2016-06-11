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


"""Fichier contenant la fonction description."""

from corps.fonctions import valider_cle
from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Retourne la description de plusieurs choses."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.description_salle, "Salle", "Personnage")
        cls.ajouter_types(cls.description_personnage, "Personnage",
                "Personnage")
        cls.ajouter_types(cls.description_objet, "Objet", "Personnage")

    @staticmethod
    def description_salle(salle, personnage):
        """Retourne la description de la salle telle que vue par le personnage.

        Paramètres à entrer :

          * salle : la salle dont on veut récupérer la description ;
          * personnage : le personnage regardant la description.

        Cette fonction retourne la description d'un salle.
        Le second paramère est utile, car cette fonction retourne la
        description perçue : les descriptions de la salle étant en partie
        scriptables, la description peut varier en fonction de
        certains critères. Cette fonction retourne le texte de la
        description telle que vue par le personnage, sous la forme
        d'une chaîne de caractères, avec les remplacements de flottantes
        et éléments dynamiques.

        Exemple d'utilisation :

          description = description(salle, personnage)
          # On a la description telle que vue par le personnage

        """
        return salle.description.regarder(personnage, salle)

    @staticmethod
    def description_personnage(personnage, autre):
        """Retourne la description du personnage telle que vue par un autre.

        Paramètres à entrer :

          * personnage : le personnage dont on veut récupérer la description ;
          * autre : le personnage regardant la description.

        Cette fonction retourne la description d'un personnage.
        Le second paramère est utile, car cette fonction retourne la
        description perçue : les descriptions du personnage étant parfois
        scriptables, la description peut varier en fonction de
        certains critères. Cette fonction retourne le texte de la
        description telle que vue par le personnage, sous la forme
        d'une chaîne de caractères, avec les remplacements de flottantes
        et éléments dynamiques.

        Exemple d'utilisation :

          description = description(personnage, joueur)
          # On a la description telle que vue par le joueur

        """
        return personnage.description.regarder(autre, personnage)

    @staticmethod
    def description_objet(objet, personnage):
        """Retourne la description de l'objet telle que vue par le personnage.

        Paramètres à entrer :

          * objet : l'objet dont on veut récupérer la description ;
          * personnage : le personnage regardant la description.

        Cette fonction retourne la description d'un objet.
        Le second paramètre est utile, car cette fonction retourne la
        description perçue : les descriptions d'objet étant en partie
        scriptables, la description peut varier en fonction de
        certains critères. Cette fonction retourne le texte de la
        description telle que vue par le personnage, sous la forme
        d'une chaîne de caractères, avec les remplacements de flottantes
        et éléments dynamiques.

        Exemple d'utilisation :

          description = description(objet, personnage)
          # On a la description telle que vue par le personnage

        """
        return objet.description.regarder(personnage, objet)

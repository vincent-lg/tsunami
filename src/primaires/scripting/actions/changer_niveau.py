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


"""Fichier contenant l'action changer_niveau."""

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Change le niveau d'un personnage."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.changer_niveau_principal, "Personnage",
                "Fraction")
        cls.ajouter_types(cls.changer_niveau_secondaire, "Personnage",
                "str", "Fraction")

    @staticmethod
    def changer_niveau_principal(personnage, niveau):
        """Change le niveau principal d'un personnage.

        Paramètres à préciser :

          * personnage : le personnage dont on veut modifier le niveau
          * niveau : le nouveau niveau (entre 1 et 100).

        Si le niveau spécifié est inférieur à 1, il est ramené à
        1. Si il est supérieur à 100, il est ramené à 100.

        """
        niveau = int(niveau)
        if niveau < 1:
            niveau = 1
        elif niveau > 100:
            niveau = 100

        personnage.niveau = niveau

    @staticmethod
    def changer_niveau_secondaire(personnage, nom_niveau, niveau):
        """Change le niveau secondaire d'un personnage.

        Paramètres à préciser :

          * personnage : le personnage dont on veut modifier le niveau
          * nom_niveau : le nom du niveau secondaire à modifier
          * niveau : le nouveau niveau (entre 1 et 100).

        Si le niveau spécifié est inférieur à 1, il est ramené à
        1. Si il est supérieur à 100, il est ramené à 100.

        NOTE : le nom du niveau doit être précisé en entier :

          changer_niveau personnage "art du pisteur" 5

        """
        niveau = int(niveau)
        if niveau < 1:
            niveau = 1
        elif niveau > 100:
            niveau = 100

        try:
            template = importeur.perso.get_niveau_par_nom(nom_niveau)
        except ValueError:
            raise ErreurExecution("niveau secondaire {} inconnu".format(
                    repr(nom_niveau)))

        cle = template.cle
        personnage.niveaux[cle] = niveau
        if cle not in personnage.xps:
            personnage.xps[cle] = 0

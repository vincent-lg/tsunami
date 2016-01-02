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


"""Fichier contenant l'action donner_tresor."""

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Donne un montant à une zone à ajouter ou retirer de son trésor."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.donner_tresor, "str", "Fraction")

    @staticmethod
    def donner_tresor(nom_zone, montant):
        """Modifie le trésor de la zone spécifiée.

        Paramètres à préciser :

          * nom_zone : le nom de la zone sous la forme d'une chaîne
          * montant : le montant à ajouter ou retirer du trésor

        Précisez un montant négatif pour retirer l'argent de la zone.
        Notez qu'il ne se produira aucune erreur si le trésor de la
        zone passe dans le négatif.

        Exemples d'utilisation :

          # Donne 500 pièces de bronze dans le trésor de la zone 'picte'
          donner_tresor "picte" 500
          # Retire 200 pièces de la même zone
          donner_tresor "picte" -200

        """
        try:
            zone = importeur.salle.zones[nom_zone.lower()]
        except KeyError:
            raise ErreurExecution("zone {} inconnue".format(repr(nom_zone)))

        zone.argent_total += int(montant)

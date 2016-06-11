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


"""Fichier contenant l'action consommer."""

from primaires.scripting.action import Action
from primaires.scripting.exceptions import InterrompreCommande
from primaires.perso.exceptions.stat import DepassementStat
from primaires.format.fonctions import supprimer_accents

class ClasseAction(Action):

    """Consomme la stat d'un personnage.

    Cette action permet de consommer une stat (vitalité, mana ou endurance)
    d'un personnage. Si la consommation ne marche simplement pas
    (parce que le personnage n'a pas assez de cette stat), un message
    est envoyé au personnage et le script est interrompu.

    """

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.consommer_defaut, "Personnage", "str",
                "Fraction")
        cls.ajouter_types(cls.consommer_perso, "Personnage", "str",
                "Fraction", "str")

    @staticmethod
    def consommer_stat(personnage, stat, points, message=None):
        """Consomme la stat indiquée."""
        msg_defauts = {
            "endurance": "Vous êtes trop fatigué.",
            "mana": "Vous épuisez votre énergie magique en vain.",
            "vitalite": "Vous êtes mort",
        }
        stat = supprimer_accents(stat)
        points = int(points)
        if points <= 0:
            return

        if message is None:
            message = msg_defauts[stat]

        courante = personnage.stats[stat].courante
        try:
            personnage.stats[stat].courante = courante - points
        except DepassementStat:
            if message:
                personnage << message

            raise InterrompreCommande

    @staticmethod
    def consommer_defaut(personnage, stat, points):
        """Consomme la stat passée en paramètre.

        Le message envoyé au joueur sera choisi par défaut en fonction de la stat.

        Les paramtres à préciser sont :

          * personnage : le personnage (joueur ou PNJ)
          * stat : le nom de la stat (exemple "mana")
          * points : le nombre de points à retirer à la stat

        Note : si vous souhaitez blesser le personnage (consommer sa
        vitalité), utilisez l'action blesser de préférence.

        """
        ClasseAction.consommer_stat(personnage, stat, points)

    @staticmethod
    def consommer_perso(personnage, stat, points, message):
        """Consomme la stat précisée en paramètre.

        Les paramètres attendus sont :

          * personnage : le personnage (joueur ou PNJ)
          * stat : le nom de la stat (par exemple "mana")
          * points : le nombre de points à retirer
          * message : le message à envoyer au joueur si la stat est trop faible.

        Si vous ne souhaitez pas notifier le personnage que sa stat
        est trop faible, précisez une chaîne vide ("") en quatrième paramètre.

        Note : si vous souhaitez blesser le personnage (consommer sa
        vitalité), utilisez l'action blesser de préférence.

        """
        ClasseAction.consommer_stat(personnage, stat, points, message)

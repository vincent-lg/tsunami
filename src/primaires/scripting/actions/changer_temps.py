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


"""Fichier contenant l'action changer_temps."""

import re

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

# Constantes
MODIFICATION = re.compile(r"^(r|m)(-?[0-9]+)([mhjoa])$")
UNITES = {
        "m": "minute",
        "h": "heure",
        "j": "jour",
        "o": "mois",
        "a": "annee",
}

class ClasseAction(Action):

    """Change le temps précisé."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.changer_temps, "TempsVariable", "str")

    @staticmethod
    def changer_temps(temps, changement):
        """Change le temps précisé.

        Cette action permet de modifier le temps précisé en paramètre,
        l'avancer ou le reculer selon plusieurs critères. Le paramètre
        'changement' est une chaîne contenant trois informations :
        une lettre pour indiquer le type de temps modifié, un ou
        plusieurs chiffres de modification et une lettre représentant
        l'unité de modification. Voir les exemples ci-dessous.

        Paramètres à préciser :

          * temps : le temps à modifier ;
          * changement : une chaîne représentant la modification à effectuer.

        La chaîne de changement doit contenir :

          * Une lettre (r pour modification réelle, m pour modification IG) ;
          * Un ou plusieurs chiffres ;
          * Une lettre représentant l'unité.

        Unités disponibles :

          * "m" : ajoute ou retire des minutes au temps indiqué ;
          * "h" : ajoute ou retire des heures au temps indiqué ;
          * "j" : ajoute ou retire des jours au temps indiqué ;
          * "o" : ajoute ou retire des mois au temps indiqué ;
          * "a" : ajoute ou retire des années au temps indiqué.

        Exemples d'utilisation :

          # Cherche le temps dans 2 mois IRL
          temps = temps()
          changer_temps temps "r2o"
          # 'r' pour modification IRL ;
          # '2' pour modification de deux unités ;
          # 'o' pour spécifier l'unité de mois.
          # Ainsi 'changer_temps temps "i2o" veut dire :
          # Avancer le temps de deux mois IRL.
          # Retire 30 minutes
          temps = temps()
          changer_temps temps "r-30m"
          # Ajoute 20 jours IG
          temps = temps()
          changer_temps temps "m20j"
          # Ajoute deux ans IG
          temps = temps()
          changer_temps temps "m2a"

        """
        changement = changement.lower()
        modification = MODIFICATION.search(changement)
        if modification is None:
            raise ErreurExecution("Format de modification de temps " \
                    "invalide : {}".format(repr(changement)))

        cnv, nombre, unite = modification.groups()
        unite = UNITES[unite]
        if cnv == "r":
            date = temps.reelle
            parametres = {
                    "annee": date.year,
                    "mois": date.month,
                    "jour": date.day,
                    "heure": date.hour,
                    "minute": date.minute,
            }

            parametres[unite] += int(nombre)
            temps.changer_IRL(**parametres)
        else:
            parametres = {
                    "annee": temps.annee,
                    "mois": temps.mois,
                    "jour": temps.jour,
                    "heure": temps.heure,
                    "minute": temps.minute,
            }

            parametres[unite] += int(nombre)
            temps.changer_IG(**parametres)

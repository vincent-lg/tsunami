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


"""Fichier contenant la fonction afficher_temps."""

from primaires.format.fonctions import supprimer_accents
from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Affiche le temps IG ou IRL précisé."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.afficher_temps, "TempsVariable", "str")

    @staticmethod
    def afficher_temps(temps, flags):
        """Retourne la chaîne contenant le temps converti.

        Paramètres à préciser :

          * temps : le temps (tel que retourné par la fonction 'temps()')
          * flags : les flags d'affichage.

        Liste des flags possibles :

          * "ig" : retourne le temps en format IG (in game)
          * "irl" : retourne le temps en format IRL ;
          * "numig" : retourne le temps IG en format numérique ;
          * "numirl" : retourne le temps IRL en format numérique ;
          * "dig" : retourne la date IG ;
          * "hig" : retourne l'heure IG ;
          * "sa" : retourne le temps sans article.

        Exemples d'utilisation :

          # Récupère le temps actuel
          actuel = temps()
          # Affiche le temps IG
          ig = afficher_temps(temps, "ig")
          dire personnage ig
          # Affiche le temps réel correspondant
          irl = afficher_temps(temps, "irl")
          dire personnage irl
          # Retire l'article du temps
          ig = afficher_temps(temps, "ig sa")
          irl = afficher_temps(temps, "irl sa")
          # Retourne le temps en format numérique
          irl = afficher(temps(temps, "numirl")
          # irl contient quelque chose comme : 2016-11-10 11:18"

        """
        flags = flags.lower().split(" ")
        if "ig" in flags:
            retour = "le {} à {}".format(temps.date_formatee,
                    temps.heure_formatee)
        elif "dig" in flags:
            retour = "le {}".format(temps.date_formatee)
        elif "hig" in flags:
            retour = "à {}".format(temps.heure_formatee)
        elif "irl" in flags:
            retour = temps.aff_reelle
        elif "numig" in flags:
            annee = temps.annee
            mois = temps.mois + 1
            jour = temps.jour + 1
            heure = temps.heure
            minute = temps.minute
            retour = "{}-{:>02}-{:>02} {:>02}:{:>02}".format(
                    annee, mois, jour, heure, minute)
        elif "numirl" in flags:
            date = temps.reelle
            annee = date.year
            mois = date.month
            jour = date.day
            heure = date.hour
            minute = date.minute
            retour = "{}-{:>02}-{:>02} {:>02}:{:>02}".format(
                    annee, mois, jour, heure, minute)
        else:
            raise ErreurExecution("Il vous faut préciser au moins \"ig\" " \
                    "ou \"irl\" en flag d'affichage")

        for flag in flags:
            if flag == "sa":
                retour = " ".join(retour.split(" ")[1:])

        return retour

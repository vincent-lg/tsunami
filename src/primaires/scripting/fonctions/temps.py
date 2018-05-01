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


"""Fichier contenant la fonction temps."""

import re
from datetime import datetime

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

# Constantes
RE_TEMPS = re.compile(
        r"^(r|m)([x0-9]{1,4})\-([x0-9]{2})\-([x0-9]{2}) " \
        "([x0-9]{2})\:([x0-9]{2})$", re.I)

class ClasseFonction(Fonction):

    """Retourne le temps indiqué.

    Sans paramètre, cette fonciton retourne le temps actuel. Ce
    temps retourné peut être affiché soit en format IG (in-game),
    soit en format réel (comme "le vendredi 15 avril 2016 à 03:00".
    Le temps retourné peut être également comparé à d'autres temps.
    Il est également possible de retourner un temps spécifique, soit
    à un temps IRL, soit à un temps IG.

    """

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.temps)
        cls.ajouter_types(cls.temps_param, "str")

    @staticmethod
    def temps():
        """Retourne le temps actuel.

        Le temps courant est retourné, c'est-à-dire le temps IRL ou IG correpsondant au moment ou la fonction s'exécute. Vous pouvez conserver ce temps (dans une mémoire ou dans une structure, par exemple). Pour l'afficher, vous aurez besoin de la fonction 'afficher_temps()'.

        Paramètres à entrer :

          Aucun

        Exemple d'utilisation :

          # Récupère le temps actuel
          temps = temps()
          # L'affiche en format IG
          ig = afficher_temps(temps, "ig")
          dire personnage "Le temps IG est ${ig}."
          # Affiche maintenant le temps réel
          irl = afficher_temps(temps, "irl")
          dire personnage "Le temps IRL est ${irl}."
          # Compare des temps entre eux
          premier = temps()
          attendre 3
          second = temps()
          si premier < second:
              # Oui, second a au moins 3 secondes de plus que premier
          finsi

        """
        return importeur.temps.variable

    @staticmethod
    def temps_param(chaine):
        """Retourne le temps modifié par la chaîne.

        La chaîne peut préciser un modificateur de temps IG ou IRL. Le format est précisé ci-dessous.

        Paramètre :

          * chaine : la chaîne indiquant le modificateur de temps

        La première lettre de la chaîne doit être "m" ou "r" pour indiquer le type de format. "m" indique que le format de temps qui suit est précisé en temps IG, "r" que le temps qui suit est exprimé en format réel.

        Après cette lettre doivent se trouver les informations suivantes :

          * 1 à 4 chiffres représentant l'année ;
          * Un signe tiret (-) ;
          * Deux chiffres représentant le mois ;
          * Un signe tiret (-) ;
          * Deux chiffres représentant le jour ;
          * Un espace ( ) ;
          * Deux chiffres représentant l'heure ;
          * Un signe deux points (:) ;
          * Deux chiffres représentant les minutes.

        Vous pouvez remplacer une information par des X à la place
        des chiffres pour indiquer que le temps actuel doit être
        utilisé. Par exemple, "rxxxx-01-01 00:00" veut dire "cette
        année réelle, le premier janvier à minuit."

        Exemples possibles :

          # On veut avoir le temps du 1 janvier 2017 à minuit
          nouvel_an = temps("r2017-01-01 00:00")
          # Que l'on peut convertir ensuite
          ig = afficher_temps(nouvel_an, "ig")
          # ... ou dans l'autre sens
          # Le temps du jour 1 du mois 1 de l'année 50 à minuit
          nouvel_an = temps("m50-01-01 00:00")
          # Et pour récupérer le format en temps IRL
          irl = afficher_temps(nouvel_an, "irl")

        """
        temps = importeur.temps.variable
        format = RE_TEMPS.search(chaine.lower())
        if format is None:
            raise ErreurExecution("Format de temps {} incorrect.".format(
                    repr(chaine)))
        cnv, annee, mois, jour, heure, minute = format.groups()
        mtn = datetime.now()
        r_annee = mtn.year
        r_mois = mtn.month
        r_jour = mtn.day
        r_heure = mtn.hour
        r_minute = mtn.minute
        m_annee = temps.annee
        m_mois = temps.mois + 1
        m_jour = temps.jour + 1
        m_heure = temps.heure
        m_minute = temps.minute

        # On remplit les format par défaut
        if cnv == "m":
            annee = int(annee) if "x" not in annee else m_annee
            mois = int(mois) if "x" not in mois else m_mois
            jour = int(jour) if "x" not in jour else m_jour
            heure = int(heure) if "x" not in heure else m_heure
            minute = int(minute) if "x" not in minute else m_minute
            mois -= 1
            jour -= 1
            temps.changer_IG(annee, mois, jour, heure, minute)
        else:
            annee = int(annee) if "x" not in annee else r_annee
            mois = int(mois) if "x" not in mois else r_mois
            jour = int(jour) if "x" not in jour else r_jour
            heure = int(heure) if "x" not in heure else r_heure
            minute = int(minute) if "x" not in minute else r_minute
            temps.changer_IRL(annee, mois, jour, heure, minute)

        return temps

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


"""Fichier contenant la classe TempsVariable, détaillée plus bas."""

from datetime import datetime, timedelta
from time import time

from abstraits.obase import BaseObj
from primaires.format.date import get_date
from .constantes import *

class TempsVariable(BaseObj):

    """Classe contenant un mécanisme de temps virtuel variable.

    À la différence de la classe Temps (module 'temps'), cette classe
    contient un temps variable qui n'est pas destiné à être enregistré,
    mais propose plusieurs calculs simplifiants l'obtention d'informations
    temporelles quand les temps IRL et IG sont synchronisés.

    Créer un temps virtuel revient à demander le temps virtuel actuel.
    On peut cependant ajouter ou retirer diverses unitées de ce temps,
    le convertir en temps réel ou bien trouver le temps IG correspondant
    à un temps réel.

    """

    def __init__(self, configurer=True):
        BaseObj.__init__(self)
        self.annee = 0
        self.mois = 0
        self.jour = 0
        self.heure = 0
        self.minute = 0

        if configurer:
            temps = importeur.temps.temps
            self.annee = temps.annee
            self.mois = temps.mois
            self.jour = temps.jour
            self.heure = temps.heure
            self.minute = temps.minute

        self.timestamp = time()
        self._construire()

    def __getnewargs__(self):
        return (False, )

    def __repr__(self):
        return "<TempsVariable pour {}>".format(self.reelle)

    @property
    def no_j(self):
        return "{:02}".format(self.jour + 1)

    @property
    def nm_j(self):
        return importeur.temps.temps.noms_jours[self.jour]

    @property
    def no_m(self):
        return "{:02}".format(self.mois + 1)

    @property
    def nm_m(self):
        return importeur.temps.temps.noms_mois[self.mois]

    @property
    def nm_s(self):
        return importeur.temps.temps.mois_saisons[self.nm_m]

    @property
    def no_a(self):
        return "{}".format(self.annee)

    @property
    def no_h(self):
        return "{:02}".format(self.heure)

    @property
    def no_m(self):
        return "{:02}".format(self.minute)

    @property
    def nom_quart(self):
        """Retourne l'heure sous la forme d'un nom de quart.

        par exemple :
            une heure moins le quart du matin

        """
        heure = self.heure
        minute = self.minute
        quart = round(minute / 15)
        if quart >= 4:
            quart = 3

        minutes = ""
        masc_minutes = ""
        if quart == 1:
            masc_minutes = minutes = "et quart"
        elif quart == 2:
            minutes = "et demie"
            masc_minutes = "et demi"
        elif quart == 3:
            heure += 1
            heure = heure % 24
            masc_minutes = minutes = "moins le quart"

        moment = "du matin"
        if heure >= 13:
            if heure < 17:
                moment = "de l'après-midi"
            else:
                moment = "du soir"
            heure = heure % 12

        nom_heure = NOMS_HEURES[heure]
        nom_heure = nom_heure.format(minutes=minutes,
                masc_minutes=masc_minutes, moment=moment)
        nom_heure = nom_heure.replace("  ", " ")
        return nom_heure.rstrip()

    @property
    def date_formatee(self):
        """Retourne la date formatée"""
        return importeur.temps.temps.formatage_date.format(no_j=self.no_j,
                nm_j=self.nm_j, no_m=self.no_m, nm_m=self.nm_m,
                nm_s=self.nm_s, no_a=self.no_a)

    @property
    def heure_formatee(self):
        """Retourne l'heure formatée"""
        return importeur.temps.temps.formatage_heure.format(no_h=self.no_h,
                no_m=self.no_m, nm_q=self.nom_quart)

    @property
    def reelle(self):
        """Retourne le temps réel associé."""
        return datetime.fromtimestamp(self.timestamp)

    @property
    def aff_reelle(self):
        """Affichage de la date réelle."""
        return get_date(self.reelle)

    def __eq__(self, autre):
        return int(self.timestamp) == int(autre.timestamp)

    def __ne__(self, autre):
        return int(self.timestamp) != int(autre.timestamp)

    def __le__(self, autre):
        return int(self.timestamp) <= int(autre.timestamp)

    def __lt__(self, autre):
        return int(self.timestamp) < int(autre.timestamp)

    def __ge__(self, autre):
        return int(self.timestamp) >= int(autre.timestamp)

    def __gt__(self, autre):
        return int(self.timestamp) > int(autre.timestamp)

    def changer_IG(self, annee=None, mois=None, jour=None, heure=None,
            minute=None):
        """Change le temps in game spécifié."""
        annee = annee if annee is not None else self.annee
        mois = mois if mois is not None else self.mois
        jour = jour if jour is not None else self.jour
        heure = heure if heure is not None else self.heure
        minute = minute if minute is not None else self.minute

        m_annee = self.annee
        m_mois = self.mois
        m_jour = self.jour
        m_heure = self.heure
        m_minute = self.minute
        nb_jours = len(importeur.temps.temps.noms_jours)
        nb_mois = len(importeur.temps.temps.noms_mois)

        # Changement du temps
        self.minute = minute
        self.heure = heure
        self.jour = jour
        self.mois = mois
        self.annee = annee

        # On module les minutes
        self.heure += self.minute // 60
        self.minute %= 60

        # On module l'heure
        self.jour += self.heure // 24
        self.heure %= 24

        # On module les jours
        self.mois += self.jour // nb_jours
        self.jour %= nb_jours

        # On module le mois
        self.annee += self.mois // nb_mois
        self.mois %= nb_mois

        if self.annee < 1:
            raise ValueError("Changement IG d'année < 1")

        # On fait évoluer le timestamp
        secondes = (annee - m_annee) * 31104000
        secondes += (mois - m_mois) * 2592000
        secondes += (jour - m_jour) * 86400
        secondes += (heure - m_heure) * 3600
        secondes += (minute - m_minute) * 60
        secondes = int(secondes * importeur.temps.temps.vitesse_ecoulement)
        self.timestamp += secondes

    def changer_IRL(self, annee=None, mois=None, jour=None, heure=None,
            minute=None):
        """Change le temps IRL, impactant le temps IG."""
        mtn = datetime.now()
        annee = annee or mtn.year
        mois = mois or mtn.month
        jour = jour or mtn.day
        heure = heure if heure is not None else mtn.hour
        minute = minute if minute is not None else mtn.minute

        date = datetime(year=annee, month=mois, day=jour, hour=heure,
                minute=minute)
        t1 = self.timestamp
        t2 = date.timestamp()

        # Entre t2 et t1 se trouvent le nombre de secondes devant
        # faire varier la date
        secondes = (int(t2 - t1) / importeur.temps.temps.vitesse_ecoulement)
        self.changer_IG(minute=self.minute + (secondes // 60))

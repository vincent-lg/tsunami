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


"""Fichier contenant la classe Temps, détaillée plus bas."""

from fractions import Fraction
from time import time
from random import choice

from abstraits.obase import BaseObj
from .constantes import *

class Temps(BaseObj):

    """Classe contenant les informations d'un temps, enregistrée en fichier.

    Cette classe est créée en lui passant en paramètre la configuration du
    module temps.

    Si la configuration du module est modifiée, il est nécessaire de supprimer
    le temps enregistré.

    """

    enregistrer = True
    def __init__(self, config):
        """Constructeur de l'objet"""
        BaseObj.__init__(self)
        self.timestamp = time()
        self._construire()
        if not config:
            return

        reglage_init = config.reglage_initial
        self.annee = reglage_init[0]
        self.mois = reglage_init[1] - 1
        self.jour = reglage_init[2] - 1
        self.heure = reglage_init[3]
        self.minute = reglage_init[4]
        self.seconde = Fraction()

        # Différents noms
        self.saisons = config.saisons
        self.mois_saisons = dict(config.mois)
        self.noms_mois = [nom for nom, saison in config.mois]
        if config.noms_jours:
            self.noms_jours = config.noms_jours
        else:
            self.noms_jours = [str(i) for i in range(1,
                    config.nombre_jours + 1)]

        # On vérifie que le réglage initial est conforme aux noms
        try:
            nom_mois = self.noms_mois[self.mois]
        except IndexError:
            raise ValueError("erreur lors du réglage de l'heure initiale : " \
                    "le mois {} est invalide".format(self.mois))
        try:
            nom_jour = self.noms_jours[self.jour]
        except IndexError:
            raise ValueError("erreur lors du réglage de l'heure initiale : " \
                    "le jour {} est invalide".format(self.jour))

        self.vitesse_ecoulement = Fraction(config.vitesse_ecoulement)

        self.formatage_date = config.formatage_date
        self.formatage_heure = config.formatage_heure

    def __getnewargs__(self):
        return (None, )

    @property
    def no_j(self):
        return "{:02}".format(self.jour + 1)

    @property
    def nm_j(self):
        return self.noms_jours[self.jour]

    @property
    def no_m(self):
        return "{:02}".format(self.mois + 1)

    @property
    def nm_m(self):
        return self.noms_mois[self.mois]

    @property
    def nm_s(self):
        return self.mois_saisons[self.nm_m]

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
        return self.formatage_date.format(no_j=self.no_j,
                nm_j=self.nm_j, no_m=self.no_m, nm_m=self.nm_m,
                nm_s=self.nm_s, no_a=self.no_a)

    @property
    def heure_formatee(self):
        """Retourne l'heure formatée"""
        return self.formatage_heure.format(no_h=self.no_h, no_m=self.no_m,
                nm_q=self.nom_quart)

    @property
    def h_lever(self):
        """Retourne l'heure du lever de soleil"""
        for ligne in type(self).importeur.temps.cfg.alternance_jn:
            if ligne[0] == self.nm_s:
                return ligne[1]

    @property
    def h_coucher(self):
        """Retourne l'heure du coucher de soleil"""
        for ligne in type(self).importeur.temps.cfg.alternance_jn:
            if ligne[0] == self.nm_s:
                return ligne[2]

    @property
    def il_fait_jour(self):
        """Retourne True s'il fait jour, False sinon"""
        return self.heure >= self.h_lever and self.heure < self.h_coucher

    @property
    def il_fait_nuit(self):
        """Retourne True s'il fait nuit, False sinon"""
        return not self.il_fait_jour

    @property
    def ciel_actuel(self):
        """Retourne le message correspondant au ciel actuel selon l'heure"""
        config = type(self).importeur.temps.cfg
        h_now = self.heure
        if h_now == self.h_lever -  1:
            return config.pre_lever
        elif h_now == self.h_lever:
            return config.post_lever
        elif h_now > self.h_lever and h_now < 12:
            return config.matinee
        elif h_now == 12:
            return config.midi
        elif h_now > 12 and h_now < self.h_coucher - 1:
            return config.apres_midi
        elif h_now == self.h_coucher - 1:
            return config.pre_coucher
        elif h_now == self.h_coucher:
            return config.post_coucher
        elif h_now > self.h_coucher or h_now < self.h_lever - 1:
            return config.nuit

    @property
    def heure_minute(self):
        """Retourne un tuple heure, minute."""
        heure = self.heure
        minute = self.minute
        if minute >= 60:
            minute %= 60
            heure += 1
        return (heure, minute)

    def inc(self):
        """Incrémente de 1 seconde réelle"""
        avt_fait_jour = self.il_fait_jour
        self.seconde += 1 / self.vitesse_ecoulement
        minute = heure = jour = mois = annee = False

        if self.seconde >= 60:
            self.seconde = Fraction()
            self.minute += 1
            minute = True
        if self.minute >= 60:
            self.minute -= 60
            self.heure += 1
            heure = True
        if self.heure >= 24:
            self.heure -= 24
            self.jour += 1
            jour = True
        if self.jour >= len(self.noms_jours):
            self.jour -= len(self.noms_jours)
            self.mois += 1
            mois = True
        if self.mois >= len(self.noms_mois):
            self.mois -= len(self.noms_mois)
            self.annee += 1
            annee = True

        apr_fait_jour = self.il_fait_jour
        if not avt_fait_jour and apr_fait_jour:
            print("Lever de soleil")
            self.lever_soleil()
        elif avt_fait_jour and not apr_fait_jour:
            print("Coucher de soleil")
            self.coucher_soleil()

        self.appeler_hook(minute, heure, jour, mois, annee)

    def lever_soleil(self):
        """Méthode appelée au moment du lever de soleil."""
        phrase = choice(importeur.temps.cfg.msgs_lever)
        for salle in importeur.salle.salles.values():
            # On n'affiche le message que dans les salles où on voit le ciel
            # Ce code pourrait ëtre optimisé
            if salle.interieur:
                continue

            perturbation = importeur.meteo.get_perturbation(salle)
            if perturbation is None or not perturbation.est_opaque():
                salle.envoyer(phrase, prompt=False)

    def coucher_soleil(self):
        """Méthode appelée au moment du coucher de soleil."""
        phrase = choice(importeur.temps.cfg.msgs_coucher)
        for salle in importeur.salle.salles.values():
            # On n'affiche le message que dans les salles où on voit le ciel
            # Ce code pourrait ëtre optimisé
            if salle.interieur:
                continue

            perturbation = importeur.meteo.get_perturbation(salle)
            if perturbation is None or not perturbation.est_opaque():
                salle.envoyer(phrase, prompt=False)

    def appeler_hook(self, minute, heure, jour, mois, annee):
        """Appelle les hooks correspondant au changement de temps."""
        if minute:
            importeur.temps.changer_minute()
        if heure:
            importeur.temps.changer_heure()
        if jour:
            importeur.temps.changer_jour()
        if mois:
            importeur.temps.changer_mois()
        if annee:
            importeur.temps.changer_annee()

    @staticmethod
    def convertir_heure(chaine, defaut=None):
        """Convertit la chaîne en un tuple (h, m, s).

        Si les minutes ou secondes ne sont pas précisés, retourne defaut
        dans le tuple.

        """
        heure = chaine.split(":")
        try:
            heure = tuple(int(h) for h in heure)
        except ValueError:
            raise ValueError("formattage d'heure invalide".format(heure))
        else:
            if len(heure) == 1:
                return heure + (defaut, defaut)
            elif len(heure) == 2:
                return heure + (defaut, )
            else:
                return heure[:3]

    # Fonctions mathématiques
    def __hash__(self):
        return hash(str(self))

    def __eq__(self, chaine):
        h, m, s = self.convertir_heure(chaine, 0)
        return self.heure == h and self.minute == m and self.seconde == s

    def __ne__(self, chaine):
        h, m, s = self.convertir_heure(chaine, 0)
        return self.heure != h or self.minute != m or self.seconde != s

    def __le__(self, chaine):
        h, m, s = self.convertir_heure(chaine)
        if self.heure < h:
            return True
        elif self.heure == h and m is not None and self.minute <= m and \
                s is None:
            return True
        elif self.heure == h and m is not None and self.minute == m and \
                s is not None and self.seconde <= s:
            return True
        return False

    def __lt__(self, chaine):
        h, m, s = self.convertir_heure(chaine)
        if self.heure < h:
            return True
        elif self.heure == h and m is not None and self.minute < m and \
                s is None:
            return True
        elif self.heure == h and m is not None and self.minute == m and \
                s is not None and self.seconde < s:
            return True
        return False

    def __ge__(self, chaine):
        h, m, s = self.convertir_heure(chaine)
        if self.heure > h:
            return True
        elif self.heure == h and m is not None and self.minute >= m and \
                s is None:
            return True
        elif self.heure == h and m is not None and self.minute == m and \
                s is not None and self.seconde >= s:
            return True
        return False

    def __gt__(self, chaine):
        h, m, s = self.convertir_heure(chaine)
        if self.heure > h:
            return True
        elif self.heure == h and m is not None and self.minute > m and \
                s is None:
            return True
        elif self.heure == h and m is not None and self.minute == m and \
                s is not None and self.seconde > s:
            return True
        return False

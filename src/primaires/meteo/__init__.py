# -*-coding:Utf-8 -*

# Copyright (c) 2010 LE GOFF Vincent
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


"""Fichier contenant le module primaire meteo."""

from random import choice, randint
from math import ceil

from abstraits.module import *
from . import commandes
from .config import cfg_meteo
from .perturbations import perturbations
from .perturbations.base import BasePertu, AUCUN_FLAG

class Module(BaseModule):

    """Cette classe représente le module primaire meteo.

    Comme son nom l'indique, ce module gère la météorologie dans l'univers.
    La météo est régie par un ensemble de perturbations se déplaçant
    de façon semi-aléatoire dans l'univers. Ces perturbations sont décrites
    dans le dossier correspondant ; une partie de leur comportement
    est configurable.

    """

    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "meteo", "primaire")
        self.perturbations_actuelles = []
        self.temperature = 0
        self.temperature_dynamique = True

    def config(self):
        """Configuration du module"""
        self.cfg = type(self.importeur).anaconf.get_config("config_meteo",
                "meteo/config.cfg", "config meteo", cfg_meteo)
        self.temperature = self.cfg.temperature_statique
        self.temperature_dynamique = self.cfg.temperature_dynamique
        importeur.temps.met_changer_jour.append(self.changer_temperature)
        BaseModule.config(self)

    def init(self):
        """Initialisation du module"""
        self.importeur.hook["salle:regarder"].ajouter_evenement(
                self.donner_meteo)
        self.perturbations_actuelles = self.importeur.supenr.charger_groupe(
                BasePertu)
        BaseModule.init(self)

    def ajouter_commandes(self):
        """Ajoute les commandes à l'interpréteur."""
        self.commandes = [
            commandes.meteo.CmdMeteo(),
        ]

        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)

    def preparer(self):
        """Préparation du module"""
        if self.temperature_dynamique:
            min, max = self.cfg.temperatures[importeur.temps.temps.mois]
            self.temperature = randint(min, max)

        self.cycle_meteo()

    @property
    def perturbations(self):
        return perturbations

    def cycle_meteo(self):
        self.importeur.diffact.ajouter_action("cycle_meteo", 60,
                self.cycle_meteo)
        # On tue les perturbations trop vieilles
        for pertu in self.perturbations_actuelles:
            pertu.tick()

        # On tente de créer une perturbation
        if len(self.perturbations_actuelles) < self.cfg.nb_pertu_max:
            t_min = t_max = self.temperature
            if importeur.salle.zones:
                t_min = min(z.temperature for z in \
                        importeur.salle.zones.values())
                t_max = max(z.temperature for z in \
                        importeur.salle.zones.values())
            perturbations = [p for p in self.perturbations if p.origine and ( \
                    p.accepte_temperature(t_min) or p.accepte_temperature(t_max))]
            salles = list(self.importeur.salle._coords.values())
            cls_pertu = choice(perturbations)
            if cls_pertu.temperature_min or cls_pertu.temperature_max:
                t_min = cls_pertu.temperature_min
                t_max = cls_pertu.temperature_max
                zones = list(importeur.salle.zones.values())
                if t_min:
                    zones = [z for z in zones if z.temperature >= t_min]
                if t_max:
                    zones = [z for z in zones if z.temperature <= t_max]
                salles = [s for s in salles if s.zone in zones]
            salles = [s for s in salles if s.coords.valide]
            try:
                salle_dep = choice(salles)
            except IndexError:
                pass
            else:
                deja_pertu = False
                n_pertu = cls_pertu(salle_dep.coords.get_copie())
                for pertu in self.perturbations_actuelles:
                    if pertu.va_recouvrir(n_pertu):
                        deja_pertu = True
                        break
                if not deja_pertu:
                    self.perturbations_actuelles.append(n_pertu)
                    for salle in n_pertu.liste_salles_sous:
                        if salle.exterieur:
                            salle.envoyer("|cy|" + n_pertu.message_debut + \
                                    "|ff|", prompt=False)
                else:
                    n_pertu.detruire()

    def donner_meteo(self, salle, liste_messages, flags):
        """Affichage de la météo d'une salle"""
        if salle.exterieur:
            res = ""
            for pertu in self.perturbations_actuelles:
                if pertu.est_sur(salle):
                    res += pertu.message_pour(salle)
                    break
            if not res:
                res += self.cfg.beau_temps
            liste_messages.append("|cy|" + res + "|ff|")

    def get_perturbation(self, salle):
        """Retourne la perturbation sur la salle ou None."""
        for pertu in self.perturbations_actuelles:
            if pertu.est_sur(salle):
                return pertu

        return None

    def changer_temperature(self):
        """Change aléatoirement la température."""
        if self.temperature_dynamique:
            min, max = self.cfg.temperatures[importeur.temps.temps.mois]
            variation = randint(-2, 2)
            temperature = self.temperature + variation
            if temperature < min:
                temperature = min
            elif temperature > max:
                temperature = max

            self.temperature = temperature

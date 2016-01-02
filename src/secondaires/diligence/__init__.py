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


"""Fichier contenant le module secondaire diligence."""

from abstraits.module import *
from primaires.format.fonctions import format_nb
from secondaires.diligence import commandes
from secondaires.diligence.diligence import DiligenceMaudite
from secondaires.diligence import editeurs


class Module(BaseModule):

    """Module proposant des zones aléatoires.

    Ce module est appelé "diligence", car la diligence maudite est
    le premier type de zone semi-aléatoire développée sur ce MUD.
    L'idée est de définir une zone modèle et de créer des salles
    répliques pour des diligences à déplacement semi-aléatoire. les
    salles définies dans le modèle proposent les titres, descriptions,
    détails et scripts pour les salles dupliquées.

    """

    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "diligence", "secondaire")
        self.commandes = []
        self.diligences = {}
        self.logger = self.importeur.man_logs.creer_logger(
                "diligence", "diligence")

    def config(self):
        """Configuration du module."""
        self.importeur.scripting.a_charger.append(self)

        BaseModule.config(self)

    def init(self):
        """Chargement des objets du module."""
        diligences = self.importeur.supenr.charger_groupe(DiligenceMaudite)
        for diligence in diligences:
            self.ajouter_diligence(diligence)

        self.logger.info(format_nb(len(diligences),
                "{nb} diligence{s} maudite{s} récupérée{s}", fem=True))

        BaseModule.init(self)

    def ajouter_commandes(self):
        """Ajout des commandes dans l'interpréteur"""
        self.commandes = [
            commandes.diligence.CmdDiligence(),
        ]

        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)

        # Ajout des éditeurs
        self.importeur.interpreteur.ajouter_editeur(
                editeurs.diledit.EdtDiledit)

    @property
    def zones(self):
        """Retourne toutes les zones des diligences (actives)."""
        cles = [cle + "_" for cle in self.diligences.keys()]
        zones = []
        for zone in importeur.salle.zones.values():
            if any(zone.cle.startswith(c) for c in cles):
                zones.append(zone)

        return zones

    def creer_diligence(self, cle):
        """Crée une diligence."""
        if cle in self.diligences:
            raise ValueError("la diligence {} existe déjà".format(
                    repr(cle)))

        diligence = DiligenceMaudite(cle)
        self.ajouter_diligence(diligence)
        return diligence

    def ajouter_diligence(self, diligence):
        """Ajoute le diligence."""
        if diligence.cle in self.diligences:
            raise ValueError("la diligence de clé {} est " \
                    "déjà définie".format(repr(diligence.cle)))

        self.diligences[diligence.cle] = diligence

    def supprimer_diligence(self, cle):
        """Supprime une diligence."""
        if cle not in self.diligences:
            raise ValueError("la diligence {} n'existe pas".format(
                    repr(cle)))

        self.diligences.pop(cle).detruire()

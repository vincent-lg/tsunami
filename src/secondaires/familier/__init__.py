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


"""Fichier contenant le module secondaire familier."""

from abstraits.module import *
from primaires.format.fonctions import format_nb
from secondaires.familier import cherchables
from secondaires.familier import commandes
from secondaires.familier import editeurs
from secondaires.familier.familier import Familier
from secondaires.familier.fiche import FicheFamilier

class Module(BaseModule):

    """Module secondaire définissant les familiers.

    Les familiers sont, avant tout, des PNJ avec des attributs
    particuliers, comme les matelots pour l'équipage. Ils obéissent
    à un maître et peuvent être utilisés pour certaines actions.
    Ils ont un régime alimentaire particulier et à la différence des
    PNJ stanrads, peuvent mourir de faim ou de soif.

    Les familiers peuvent aussi être des montures (on peut les
    chevaucher pour se déplacer). Il s'agit juste d'un attribut
    supplémentaire des familiers.

    """

    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "familier", "secondaire")
        self.fiches = {}
        self.familiers = {}
        self.commandes = []
        self.logger = self.importeur.man_logs.creer_logger(
                "familier", "familier")

    def init(self):
        """Chargement des objets du module."""
        # On récupère les fiches de familier
        fiches = self.importeur.supenr.charger_groupe(FicheFamilier)
        for fiche in fiches:
            self.ajouter_fiche_familier(fiche)

        self.logger.info(format_nb(len(fiches),
                "{nb} fiche{s} de familier récupérée{s}", fem=True))

        # On récupère les familiers
        familiers = self.importeur.supenr.charger_groupe(Familier)
        for familier in familiers:
            self.ajouter_familier(familier)

        self.logger.info(format_nb(len(familiers),
                "{nb} familier{s} récupéré{s}"))

        # Ajout de la catégorie de commande
        self.importeur.interpreteur.categories["familier"] = \
                "Familiers et montures"

        # Abonne le module à la destruction d'un PNJ
        self.importeur.hook["pnj:détruit"].ajouter_evenement(
                self.detruire_pnj)

        BaseModule.init(self)

    def ajouter_commandes(self):
        """Ajout des commandes dans l'interpréteur"""
        self.commandes = [
            commandes.familier.CmdFamilier(),
        ]

        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)

        # Ajout des éditeurs
        self.importeur.interpreteur.ajouter_editeur(
                editeurs.famedit.EdtFamedit)

    def creer_fiche_familier(self, cle):
        """Crée une nouvelle fiche de familier."""
        if cle in self.fiches:
            raise ValueError("la fiche de familier {} existe déjà".format(
                    repr(cle)))

        fiche = FicheFamilier(cle)
        self.ajouter_fiche_familier(fiche)
        return fiche

    def ajouter_fiche_familier(self, fiche):
        """Ajoute une fiche de familier."""
        if fiche.cle in self.fiches:
            raise ValueError("la fiche de familier {} existe déjà".format(
                    repr(fiche.cle)))

        self.fiches[fiche.cle] = fiche

    def supprimer_fiche_familier(self, cle):
        """Supprime une fiche de familier."""
        if cle not in self.fiches:
            raise ValueError("la fiche de familier {} n'existe pas".format(
                    repr(cle)))

        self.fiches.pop(cle).detruire()

    def creer_familier(self, pnj):
        """Crée un familier sur un PNJ."""
        if pnj.identifiant in self.familiers:
            raise ValueError("le familier {} existe déjà".format(
                    repr(pnj.identifiant)))

        if pnj.cle not in self.fiches:
            raise ValueError("le pnj {} n'a pas de fiche de familier".format(
                    repr(pnj.cle)))

        familier = Familier(pnj)
        self.ajouter_familier(familier)
        return familier

    def ajouter_familier(self, familier):
        """Ajoute le familier."""
        if familier.identifiant in self.familiers:
            raise ValueError("le familier d'identifiant {} est " \
                    "déjà défini".format(repr(familier.identifiant)))

        self.familiers[familier.identifiant] = familier

    def supprimer_familier(self, identifiant):
        """Supprime un familier."""
        if identifiant not in self.familiers:
            raise ValueError("le familier {} n'existe pas".format(
                    repr(identifiant)))

        self.familiers.pop(identifiant).detruire()

    def detruire_pnj(self, pnj):
        """Détruit le familier si nécessaire."""
        if pnj.identifiant in self.familiers:
            self.supprimer_familier(pnj.identifiant)

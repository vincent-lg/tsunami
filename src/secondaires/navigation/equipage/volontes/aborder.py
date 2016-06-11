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


"""Fichier contenant la volonté Aborder."""

import re

from vector import mag

from primaires.format.fonctions import contient
from secondaires.navigation.equipage.ordres.aborder import Aborder as \
        OrdreAborder
from secondaires.navigation.equipage.ordres.chercher_adversaire import \
        ChercherAdversaire
from secondaires.navigation.equipage.ordres.long_deplacer import LongDeplacer
from secondaires.navigation.equipage.volontes.tirer import Tirer
from secondaires.navigation.equipage.volonte import Volonte

class Aborder(Volonte):

    """Classe représentant une volonté.

    Cette volonté choisit un ou ou plusieurs matelots (du poste
    sabreur) pour aborder un navire adversaire, précisé en paramètre.

    """

    cle = "aborder"
    ordre_court = re.compile(r"^a\s+(.*)$", re.I)
    ordre_long = re.compile(r"^aborder\s+(.*)$", re.I)

    def __init__(self, navire, adverse=None):
        """Construit une volonté."""
        Volonte.__init__(self, navire)
        self.adverse = adverse

    @property
    def arguments(self):
        """Propriété à redéfinir si la volonté comprend des arguments."""
        return (self.adverse, )

    def choisir_matelots(self, exception=None):
        """Retourne le matelot le plus apte à accomplir la volonté."""
        navire = self.navire
        adverse = self.adverse
        matelots = navire.equipage.get_matelots_au_poste(
                "sabreur", endurance_min=30, exception=exception)
        graph = self.navire.graph
        sabreurs = []

        # Détermine la salle la plus proche
        distance = None
        choisie = None
        for salle in navire.salles.values():
            t_mag = mag(salle.coords.x, salle.coords.y, 0,
                    adverse.position.x, adverse.position.y, 0)
            if distance is None or t_mag < distance:
                distance = t_mag
                choisie = salle

        # Maintenant, détermine la salle de l'adversaire la plus proche
        distance = None
        adv_choisie = None
        for salle in adverse.salles.values():
            t_mag = mag(salle.coords.x, salle.coords.y, 0,
                    choisie.coords.x, choisie.coords.y, 0)
            if distance is None or t_mag < distance:
                distance = t_mag
                adv_choisie = salle

        # Enfin, cherche la salle de transition des sabreurs
        for matelot in matelots:
            origine = matelot.salle.mnemonic
            destination = choisie.mnemonic
            if origine == destination:
                sabreurs.append((matelot, [], adv_choisie))
            else:
                chemin = graph.get((origine, destination))
                if chemin:
                    sabreurs.append((matelot, chemin, adv_choisie))

        return sabreurs

    def executer(self, sabreurs):
        """Exécute la volonté."""
        navire = self.navire
        for matelot, sorties, adv_salle in sabreurs:
            ordres = []
            if sorties:
                aller = LongDeplacer(matelot, navire, *sorties)
                ordres.append(aller)

            aborder = OrdreAborder(matelot, navire, adv_salle)
            chercher = ChercherAdversaire(matelot, navire)
            ordres.append(aborder)
            ordres.append(chercher)
            self.ajouter_ordres(matelot, ordres)

    def crier_ordres(self, personnage):
        """On fait crier l'ordre au personnage."""
        adverse = self.adverse
        msg = "{} s'écrie : à l'abordage ! Tous sur {} !".format(
                personnage.distinction_audible, adverse.desc_survol)
        self.navire.envoyer(msg)

    @classmethod
    def extraire_arguments(cls, navire, nom_navire):
        """Extrait les arguments de la volonté."""
        for navire in Tirer.trouver_navires(navire):
            if contient(navire.desc_survol, nom_navire):
                return (navire, )

        raise ValueError("Le navire {} n'est pas en vue.".format(
                nom_navire))

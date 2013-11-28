# -*-coding:Utf-8 -*

# Copyright (c) 2013 LE GOFF Vincent
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


"""Fichier contenant la volonté Tirer."""

import re

from primaires.format.fonctions import contient
from secondaires.navigation.equipage.ordres.charger_boulet import ChargerBoulet
from secondaires.navigation.equipage.ordres.charger_poudre import ChargerPoudre
from secondaires.navigation.equipage.ordres.feu import Feu
from secondaires.navigation.equipage.ordres.long_deplacer import LongDeplacer
from secondaires.navigation.equipage.ordres.viser import Viser
from secondaires.navigation.equipage.volonte import Volonte

class Tirer(Volonte):

    """Classe représentant une volonté.

    Cette volonté choisit un matelot pour, si besoin, se déplacer
    dans la salle d'un canon, le charger (en poudre et boulet), viser un
    navire adverse et tirer.

    """

    cle = "tirer"
    ordre_court = re.compile(r"^t\s+(.*)$", re.I)
    ordre_long = re.compile(r"^tirer\s+(.*)$", re.I)
    def __init__(self, navire, adverse=None, bruyant=True):
        """Construit une volonté."""
        Volonte.__init__(self, navire)
        self.adverse = adverse
        self.bruyant = bruyant

    @property
    def arguments(self):
        """Propriété à redéfinir si la volonté comprend des arguments."""
        return (self.adverse, self.bruyant)

    def choisir_matelots(self):
        """Retourne le matelot le plus apte à accomplir la volonté."""
        navire = self.navire
        equipage = navire.equipage
        canon = None
        for salle in navire.salles.values():
            canon = salle.get_element("canon")
            if canon:
                break

        if canon is None:
            return None

        proches = []
        matelots = equipage.get_matelots_au_poste("artilleur")
        graph = self.navire.graph
        for matelot in matelots:
            origine = matelot.salle.mnemonic
            destination = canon.parent.mnemonic
            if origine == destination:
                proches.append((matelot, [], canon))
            else:
                chemin = graph.get((origine, destination))
                if chemin:
                    proches.append((matelot, chemin, canon))

        proches = sorted([couple for couple in proches],
                key=lambda couple: len(couple[1]))
        if proches:
            return proches[0]

        return None

    def executer(self, couple):
        """Exécute la volonté."""
        if couple is None:
            return

        navire = self.navire
        adverse = self.adverse
        matelot, sorties, canon = couple
        personnage = matelot.personnage
        ordres = []
        if sorties:
            aller = LongDeplacer(matelot, navire, *sorties)
            aller.volonte = self
            ordres.append(aller)

        if canon.onces == 0:
            charger_poudre = ChargerPoudre(matelot, navire, canon)
            charger_poudre.volonte = self
            ordres.append(charger_poudre)

        if canon.projectile is None:
            charger_boulet = ChargerBoulet(matelot, navire, canon)
            charger_boulet.volonte = self
            ordres.append(charger_boulet)

        viser = Viser(matelot, navire, canon, adverse, self.bruyant)
        viser.volonte = self
        ordres.append(viser)

        feu = Feu(matelot, navire, canon)
        feu.volonte = self
        ordres.append(feu)

        for ordre in ordres:
            if ordre:
                matelot.ordonner(ordre)

        matelot.executer_ordres()

    def crier_ordres(self, personnage):
        """On fait crier l'ordre au personnage."""
        adverse = self.adverse
        msg = "{} s'écrie : un boulet sur {} !".format(
                personnage.distinction_audible, adverse.desc_survol)
        self.navire.envoyer(msg)

    @classmethod
    def extraire_arguments(cls, navire, nom_navire):
        """Extrait les arguments de la volonté."""
        for navire in importeur.navigation.navires.values():
            if contient(navire.desc_survol, nom_navire):
                return (navire, )

        return ()

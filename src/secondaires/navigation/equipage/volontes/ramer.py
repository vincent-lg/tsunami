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


"""Fichier contenant la volonté Ramer."""

import re

from secondaires.navigation.equipage.volontes.tenir_rames import TenirRames
from secondaires.navigation.equipage.ordres.ramer import Ramer as OrdreRamer

class Ramer(TenirRames):

    """Classe représentant une volonté.

    Cette volonté est appelée pour demander aux rameurs de ramer
    à une certaine vitesse.

    """

    cle = "ramer"
    ordre_court = re.compile(r"^r\s?(-?[0-3cbt])$", re.I)
    ordre_long = re.compile(
            r"^ramer\s+(arriere|immobile|lente|moyenne|" \
            r"rapide|centre|babord|tribord)$", re.I)

    def __init__(self, navire, vitesse=""):
        """Construit une volonté."""
        TenirRames.__init__(self, navire)
        self.vitesse = vitesse

    @property
    def arguments(self):
        """Propriété à redéfinir si la volonté comprend des arguments."""
        return (self.vitesse, )

    def executer(self, objectifs):
        """Exécute la volonté."""
        TenirRames.executer(self, objectifs)

        navire = self.navire
        equipage = navire.equipage
        vitesse = self.vitesse
        for rames in navire.rames:
            if rames.tenu is None:
                continue

            personnage = rames.tenu
            matelot = equipage.get_matelot_depuis_personnage(personnage)
            if matelot is None:
                continue

            matelot.invalider_ordres("ramer")
            ordres = []
            ramer = OrdreRamer(matelot, navire, rames, vitesse)
            ordres.append(ramer)
            self.ajouter_ordres(matelot, ordres)

    def crier_ordres(self, personnage):
        """On fait crier l'ordre au personnage."""
        vitesse = self.vitesse
        if vitesse == "arrière":
            msg_vitesse = "en arrière"
        elif vitesse == "centre":
            msg_vitesse = "au centre"
        elif vitesse == "droite":
            msg_vitesse = "sur tribord"
        elif vitesse == "gauche":
            msg_vitesse = "sur bâbord"
        elif vitesse == "immobile":
            msg_vitesse = "on arrête"
        elif vitesse == "lente":
            msg_vitesse = "cadence lente"
        elif vitesse == "moyenne":
            msg_vitesse = "cadence moyenne"
        elif vitesse == "rapide":
            msg_vitesse = "donnez tout"

        msg = "{} s'écrie : les rameurs, {} !".format(
                personnage.distinction_audible, msg_vitesse)
        self.navire.envoyer(msg)

    @classmethod
    def extraire_arguments(cls, navire, vitesse):
        """Extrait les arguments de la volonté."""
        if vitesse in ("arriere", "-1"):
            vitesse = "arrière"
        elif vitesse in ("babord", "b"):
            vitesse = "gauche"
        elif vitesse in ("centre", "c"):
            vitesse = "centre"
        elif vitesse in ("immobile", "0"):
            vitesse = "immobile"
        elif vitesse in ("lente", "1"):
            vitesse = "lente"
        elif vitesse in ("moyenne", "2"):
            vitesse = "moyenne"
        elif vitesse in ("rapide", "3"):
            vitesse = "rapide"
        elif vitesse in ("tribord", "t"):
            vitesse = "droite"
        else:
            raise ValueError("La vitesse {} est inconnue.".format(
                vitesse))

        return (vitesse, )

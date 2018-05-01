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


"""Fichier contenant la volonté Vitesse."""

import re

from corps.fonctions import lisser
from secondaires.navigation.equipage.ordres.long_deplacer import LongDeplacer
from secondaires.navigation.equipage.ordres.relacher_gouvernail import \
        RelacherGouvernail
from secondaires.navigation.equipage.ordres.tenir_gouvernail import \
        TenirGouvernail
from secondaires.navigation.equipage.ordres.virer import Virer as OrdreVirer
from secondaires.navigation.equipage.volonte import Volonte

class Vitesse(Volonte):

    """Classe représentant une volonté.

    Cette volonté crée le contrôle 'vitesse' qui permet de contrôler
    la vitesse du navire. On peut préciser une vitese optimale
    (c'est-à-dire le maximum de vitesse que le navire peut obtenir
    sous ces circonstances) ou une vitesse plus précise.

    """

    cle = "vitesse"
    ordre_court = re.compile(r"^vi([0-9]+,?[0-9]?)?$", re.I)
    ordre_long = re.compile(r"^vitesse\s+([0-9]+,?[0-9]?)?$", re.I)

    def __init__(self, navire, vitesse=None):
        """Construit une volonté."""
        Volonte.__init__(self, navire)
        self.vitesse = vitesse

    @property
    def arguments(self):
        """Propriété à redéfinir si la volonté comprend des arguments."""
        return (self.vitesse, )

    def choisir_matelots(self, exception=None):
        """On ne retourne aucun matelot."""
        return None

    def executer(self, matelot):
        """Exécute la volonté."""
        navire = self.navire
        navire.equipage.controler("vitesse", self.vitesse)

    def crier_ordres(self, personnage):
        """On fait crier l'ordre au personnage."""
        vitesse = self.vitesse
        if vitesse is None:
            msg = "En avant !"
        else:
            vitesse = round(vitesse, 1)
            s = "s" if vitesse != 1 else ""
            vitesse = str(vitesse).rstrip("0.").replace(".", ",")
            msg = "Restez sous {} noeud{s} !".format(vitesse, s=s)

        msg = "{} s'écrie : {}".format(
                personnage.distinction_audible, msg)
        self.navire.envoyer(msg)

    @classmethod
    def extraire_arguments(cls, navire, vitesse=None):
        """Extrait les arguments de la volonté."""
        if isinstance(vitesse, str):
            vitesse = round(float(vitesse.replace(",", ".")), 1)
        else:
            vitesse = None

        return (vitesse, )

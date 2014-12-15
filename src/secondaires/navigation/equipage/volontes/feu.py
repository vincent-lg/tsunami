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
from secondaires.navigation.equipage.volontes.tirer import Tirer
from secondaires.navigation.equipage.volonte import Volonte

class Feu(Volonte):

    """Classe représentant une volonté.

    Cette volonté inscrit tout simplement le navire précisé
    comme cible. Il s'en suivra, dans la mesure où l'équipage le
    peut, un tir continu sur la cible jusqu'à ce qu'elle coule.

    """

    cle = "feu"
    ordre_court = re.compile(r"^f\s+(.*)$", re.I)
    ordre_long = re.compile(r"^feu\s+(.*)$", re.I)
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
        return None

    def executer(self, matelot):
        """Exécute la volonté."""
        self.navire.equipage.ajouter_objectif("couler", self.adverse)

    def crier_ordres(self, personnage):
        """On fait crier l'ordre au personnage."""
        adverse = self.adverse
        msg = "{} s'écrie : feu à volonté sur {} !".format(
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

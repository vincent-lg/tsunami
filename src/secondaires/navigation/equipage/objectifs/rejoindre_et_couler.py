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


"""Objectif rejoindre_et_couler."""

from secondaires.navigation.equipage.objectifs.couler import Couler
from secondaires.navigation.equipage.objectifs.rejoindre_navire import \
        RejoindreNavire

class RejoindreEtCouler(RejoindreNavire, Couler):

    """Objectif rejoindre_et_couler.

    Cet objectif, assez offensif, se charge de rejoindre le navire
    cible (à assez faible distance pour pouvoir l'aborder) tandis
    qu'il le canone dès qu'il se trouve à portée.

    """

    cle = "rejoindre_et_couler"

    def __init__(self, equipage, cible=None, distance_min=1.3):
        RejoindreNavire.__init__(self, equipage, cible, distance_min)
        Couler.__init__(self, equipage, cible)

    actif = Couler.actif

    def afficher(self):
        """Méthode à redéfinir retournant l'affichage de l'objectif."""
        cible = self.cible
        return "Rejoindre et couler {}".format(cible.desc_survol)

    def creer(self):
        """L'objectif est créé.

        On crée les contrôles associés pour atteindre l'objectif
        et on attaque la cible.

        """
        RejoindreNavire.creer(self)
        Couler.creer(self)

    def verifier(self, prioritaire):
        """Vérifie les objectifs."""
        RejoindreNavire.verifier(self, prioritaire)
        Couler.verifier(self, prioritaire)

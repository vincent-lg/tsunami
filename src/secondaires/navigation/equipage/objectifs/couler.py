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


"""Objectif couler."""

from secondaires.navigation.equipage.objectif import Objectif

class Couler(Objectif):

    """Objectif couler.

    Cet objectif demande à un équipage de couler un navire cible
    précisé. À la différence de la plupart des objectifs, cet
    objectif reste actif même si l'objectif n'est pas prioritaire
    (si un autre objectif est plus important). Cet objectif
    continue d'essayer de couler la cible.

    """

    cle = "couler"

    def __init__(self, equipage, cible=None):
        Objectif.__init__(self, equipage, cible)
        self.cible = cible

    @property
    def actif(self):
        """Retourne True si l'objectif est actif, False sinon."""
        navire = self.navire
        cible = self.cible
        if cible is None or not cible.e_existe:
            return False

        if cible.accoste:
            return False

        distance = (navire.opt_position - cible.opt_position).mag
        if distance > 200:
            return False

        return True

    def afficher(self):
        """Méthode à redéfinir retournant l'affichage de l'objectif."""
        cible = self.cible
        return "Couler {}".format(cible.desc_survol)

    def tirer_sur_cible(self):
        """Tire sur la cible si il y a un canon disponible au minimum."""
        equipage = self.equipage
        if equipage.get_canons_libres():
            equipage.demander("tirer", self.cible, False)

    def creer(self):
        """L'objectif est créé.

        On essaye tout de suite de tirer sur la cible.

        """
        equipage = self.equipage
        commandant = self.commandant
        if commandant is None:
            return

        self.tirer_sur_cible()

    def verifier(self, prioritaire):
        """Vérifie que l'objectif est toujours valide.

        Dans cette méthode, on essaye de tirer sur la cible.

        """
        equipage = self.equipage
        navire = self.navire
        commandant = self.commandant
        if commandant is None:
            return

        self.tirer_sur_cible()

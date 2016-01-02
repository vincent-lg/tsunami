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


"""Fichier contenant l'ordre Revenir."""

from secondaires.navigation.equipage.signaux import *
from secondaires.navigation.equipage.ordres.long_deplacer import LongDeplacer

from ..ordre import *

class Revenir(Ordre):

    """Ordre demandant au matelot de revenir à sa salle d'affectation.

    Cet ordre est généralement appelé à la fin d'une volonté pour
    demander au matelot de rejoindre son poste affecté.

    """

    cle = "revenir"
    def executer(self):
        """Exécute l'ordre : déplace le matelot."""
        matelot = self.matelot
        navire = self.navire
        personnage = matelot.personnage
        salle = personnage.salle
        affectation = matelot.affectation
        if affectation and affectation is not salle:
            graph = navire.graph
            chemin = graph.get((salle.mnemonic, affectation.mnemonic))
            if chemin:
                long_deplacement = LongDeplacer(matelot, navire, *chemin)
                generateur = long_deplacement.creer_generateur()
                yield SignalAttendre(generateur)
            yield SignalTermine()
        elif affectation:
            yield SignalInutile("Je suis déjà dans ma salle affectée")

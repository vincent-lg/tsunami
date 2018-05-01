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


"""Fichier contenant l'ordre Aborder."""

from vector import mag

from secondaires.navigation.equipage.signaux import *

from ..ordre import *

class Aborder(Ordre):

    """Ordre aborder.

    Cet ordre demande au matelot d'aborder un navire adverse.

    """

    cle = "aborder"
    ENDURANCE_MIN = 20

    def __init__(self, matelot, navire, salle=None):
        Ordre.__init__(self, matelot, navire, salle)
        self.salle = salle

    def executer(self):
        """Exécute l'ordre : essaye d'aborder."""
        navire = self.navire
        matelot = self.matelot
        personnage = matelot.personnage
        salle = personnage.salle
        d_salle = self.salle
        navire = d_salle.navire

        if d_salle is personnage.salle:
            yield SignalInutile("le matelot a déjà abordé")

        if mag(salle.coords.x, salle.coords.y, 0, d_salle.coords.x,
                d_salle.coords.y, 0) > 2:
            yield SignalAbandonne("Ce navire est trop loin, capitaine !",
                    True)

        matelot.armer()
        personnage.salle = d_salle
        personnage << "Vous sautez dans {}.".format(
                navire.desc_survol)
        personnage << salle.regarder(personnage)
        d_salle.envoyer("{{}} arrive en sautant depuis {}.".format(
                salle.titre.lower()), personnage)
        salle.envoyer("{{}} saute dans {}.".format(
                navire.nom), personnage)
        importeur.hook["personnage:deplacer"].executer(
                personnage, d_salle, None, 0)

        # On appelle les pnj.arrive des PNJs de la salle
        for perso in d_salle.personnages:
            if perso is not personnage and hasattr(perso, "script") and \
                    perso.peut_voir(personnage):
                importeur.hook["pnj:arrive"].executer(perso,
                        personnage)

        yield SignalTermine()

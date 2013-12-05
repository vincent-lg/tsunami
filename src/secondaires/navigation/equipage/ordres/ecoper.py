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


"""Fichier contenant l'ordre Ecoper."""

from secondaires.navigation.equipage.signaux import *

from ..ordre import *

class Ecoper(Ordre):

    """Ordre écoper.

    Cet ordre demande au matelot d'écoper l'eau dans une salle. Cet
    ordre est responsable de récupérer une écope depuis la cale si
    besoin. Cet ordre est répété tant qu'il y a de l'eau sur le
    pont.

    """

    cle = "écoper"
    ENDURANCE_MIN = 30
    def __init__(self, matelot, navire, salle=None):
        Ordre.__init__(self, matelot, navire)
        self.salle = salle

    def executer(self):
        """Exécute l'ordre : écope."""
        navire = self.navire
        matelot = self.matelot
        personnage = matelot.personnage
        salle = self.salle
        if salle is not personnage.salle:
            yield SignalInutile("le matelot ne se trouve pas dans la bonne salle")
        if salle.poids_eau == 0:
            yield SignalInutile("il n'y a pas d'eau à écoper ici")
        else:
            yield self.relayer_si_fatigue(self.ENDURANCE_MIN)
            ecope = self.prendre_ecope(personnage)
            salle.ecoper(personnage, ecope)
            yield SignalRepete(1)

    def prendre_ecope(self, personnage):
        """Prend une écope depuis la cale si besoin."""
        self.jeter_ou_entreposer("écope")
        ecope = None
        for objet in list(personnage.equipement.tenus):
            if objet.nom_type == "écope":
                ecope = objet

        if ecope is None:
            # On cherche à en récupérer dans la cale
            cale = personnage.salle.navire.cale
            ecopes = cale.ecopes
            if not ecopes:
                return None

            ecopes = [importeur.objet.prototypes[cle] for cle in \
                    ecopes.keys()]
            ecopes.sort(key=lambda prototype: prototype.poids_max,
                    reverse=True)
            ecope = ecopes[0]
            return cale.recuperer(personnage, ecope.cle)

        return ecope

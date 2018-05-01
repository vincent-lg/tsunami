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


"""Fichier contenant l'ordre ChargerPoudre."""

from secondaires.navigation.equipage.signaux import *

from ..ordre import *

class ChargerBoulet(Ordre):

    """Ordre charger_boulet.

    Cet ordre demande au matelot de charger en boulet un canon du
    navire. Cet ordre est également responsable de collecter un boulet
    de canon de la cale si besoin est.

    """

    cle = "charger_boulet"
    etats_autorises = ("charger_canon", "")

    def __init__(self, matelot, navire, canon=None, bruyant=False):
        Ordre.__init__(self, matelot, navire, canon, bruyant)
        self.canon = canon
        self.bruyant = bruyant

    def executer(self):
        """Exécute l'ordre : colmate."""
        navire = self.navire
        matelot = self.matelot
        personnage = matelot.personnage
        canon = self.canon
        salle = canon.parent
        yield 0.3
        boulet = self.prendre_boulet_canon(personnage)
        if boulet is None:
            yield SignalAbandonne("Il n'y a pas de boulet de canon en " \
                    "cale !", self.bruyant)

        yield canon.pre_charger(personnage)
        canon.post_charger(personnage, boulet)
        yield SignalTermine()

    def prendre_boulet_canon(self, personnage):
        """Prend un boulet de canon depuis la cale si besoin."""
        self.jeter_ou_entreposer("boulet de canon")
        for objet in list(personnage.equipement.tenus):
            if objet.nom_type == "boulet de canon":
                personnage.equipement.tenus.retirer(objet)
                return objet

        # On cherche à en récupérer dans la cale
        cale = personnage.salle.navire.cale
        boulets = cale.boulets
        if not boulets:
            return None

        boulets = [importeur.objet.prototypes[cle] for cle in \
                boulets.keys()]
        boulets.sort(key=lambda prototype: prototype.degats)
        boulet = boulets[0]
        return cale.recuperer(personnage, boulet.cle, donner=False)

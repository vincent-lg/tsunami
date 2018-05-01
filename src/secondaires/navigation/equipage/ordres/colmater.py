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


"""Fichier contenant l'ordre Colmater."""

from secondaires.navigation.constantes import *
from secondaires.navigation.equipage.signaux import *

from ..ordre import *

class Colmater(Ordre):

    """Ordre colmater.

    Cet ordre demande au matelot de colmater une brèche dans la coque
    Cet ordre est responsable de récupérer un tonneau de poix (type
    calfeutrage) depuis la cale si besoin.

    """

    cle = "colmater"
    def __init__(self, matelot, navire, salle=None, bruyant=False):
        Ordre.__init__(self, matelot, navire, salle, bruyant)
        self.salle = salle
        self.bruyant = bruyant

    def executer(self):
        """Exécute l'ordre : colmate."""
        navire = self.navire
        matelot = self.matelot
        personnage = matelot.personnage
        salle = self.salle
        if salle is not personnage.salle:
            yield SignalInutile("le matelot ne se trouve pas dans la bonne salle")
        if salle.voie_eau != COQUE_OUVERTE:
            yield SignalInutile("la coque n'est pas endommagée ici")
        else:
            calfeutrage = self.prendre_calfeutrage(personnage)
            if calfeutrage is None:
                yield SignalAbandonne("Il n'y a pas de poix en cale.",
                        self.bruyant)

            salle.colmater(personnage, calfeutrage)
            yield SignalTermine()

    def prendre_calfeutrage(self, personnage):
        """Prend un calfeutrage depuis la cale si besoin."""
        self.jeter_ou_entreposer("calfeutrage")
        calfeutrage = None
        for objet in list(personnage.equipement.tenus):
            if objet.nom_type == "calfeutrage":
                if objet.onces_contenu == 0:
                    personnage.equipement.tenus.retirer(objet)
                    importeur.objet.supprimer_objet(objet.identifiant)
                else:
                    calfeutrage = objet

        if calfeutrage is None:
            # On cherche à en récupérer dans la cale
            cale = personnage.salle.navire.cale
            tonneaux = cale.tonneaux_poix
            if not tonneaux:
                return None

            tonneaux = [importeur.objet.prototypes[cle] for cle in \
                    tonneaux.keys()]
            tonneaux.sort(key=lambda prototype: prototype.onces_max_contenu,
                    reverse=True)
            calfeutrage = tonneaux[0]
            return cale.recuperer(personnage, calfeutrage.cle)

        return calfeutrage

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


"""Fichier contenant l'ordre ChargerPoudre."""

from secondaires.navigation.constantes import *
from secondaires.navigation.equipage.signaux import *

from ..ordre import *

class ChargerPoudre(Ordre):

    """Ordre charger_poudre.

    Cet ordre demande au matelot de charger en poudre un canon du
    navire. Cet ordre est également responsable de collecter un sac
    de poudre de la cale si besoin est.

    """

    cle = "charger_poudre"
    def __init__(self, matelot, navire, canon=None, onces=5, bruyant=False):
        Ordre.__init__(self, matelot, navire, canon, onces, bruyant)
        self.canon = canon
        self.onces = onces
        self.bruyant = bruyant

    def executer(self):
        """Exécute l'ordre : colmate."""
        navire = self.navire
        matelot = self.matelot
        personnage = matelot.personnage
        canon = self.canon
        salle = canon.parent
        onces = self.onces
        if canon.onces >= onces or canon.onces >= canon.max_onces:
            yield SignalInutile("ce canon est déjà chargé en poudre")

        sac = self.prendre_sac_poudre(personnage)
        if sac is None:
            yield SignalAbandonne("Il n'y a pas de sac de poudre en cale.",
                    self.bruyant)

        if onces > canon.max_onces - canon.onces:
            onces = canon.max_onces - canon.onces

        if onces == 1:
            msg = "une once de poudre dans {}.".format(canon.nom)
        else:
            msg = "{} onces de poudre dans {}.".format(onces, canon.nom)

        canon.onces += onces
        sac.onces_contenu -= onces
        personnage << "Vous versez " + msg
        salle.envoyer("{} verse " + msg, personnage)
        yield SignalTermine()

    def prendre_sac_poudre(self, personnage):
        """Prend un sac de poudre depuis la cale si besoin."""
        self.jeter_ou_entreposer("sac de poudre")
        sac = None
        for objet in list(personnage.equipement.tenus):
            if objet.nom_type == "sac de poudre":
                if objet.onces_contenu < self.onces:
                    personnage.equipement.tenus.retirer(objet)
                    importeur.objet.supprimer_objet(objet.identifiant)
                else:
                    sac = objet

        if sac is None:
            # On cherche à en récupérer dans la cale
            cale = personnage.salle.navire.cale
            sacs = cale.sacs_poudre
            if not sacs:
                return None

            sacs = [importeur.objet.prototypes[cle] for cle in \
                    sacs.keys()]
            sacs.sort(key=lambda prototype: prototype.onces_max_contenu,
                    reverse=True)
            sac = sacs[0]
            return cale.recuperer(personnage, sac.cle)

        return sac

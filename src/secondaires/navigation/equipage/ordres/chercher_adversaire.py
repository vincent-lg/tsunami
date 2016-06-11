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


"""Fichier contenant l'ordre ChercherAdversaire."""

from random import choice

from secondaires.navigation.constantes import est_capturable
from secondaires.navigation.equipage.signaux import *

from ..ordre import *

class ChercherAdversaire(Ordre):

    """Ordre chercher_adversaire.

    Cet ordre demande au matelot d'attaquer et chercher un adversaire.
    Le matelot cherche l'équipage auquel il appartient et cherche
    les autres PNJ qui ne sont pas dans le même équipage que lui.
    Il n'attaque pas les joueurs ni les PNJ sans équipage. Si il
    n'y a aucun adversaire présent, essaye de se déplacer dans le
    navire pour trouver une cible.

    """

    cle = "chercher_adversaire"
    etats_autorises = ("combat", )

    def executer(self):
        """Exécute l'ordre : cherche un adversaire."""
        navire = self.navire
        matelot = self.matelot
        personnage = matelot.personnage
        salle = personnage.salle

        # Regarde si ce battre est absolument nécessaire
        adv_navire = getattr(salle, "navire", None)
        adv_equipage = getattr(adv_navire, "equipage", None)
        actuels = getattr(adv_equipage, "points_actuels", 0)
        if est_capturable(navire, actuels):
            yield SignalTermine()
        else:
            # Regarde si il y a des matelots adversaires dans la salle
            adversaires = self.get_adversaires(salle, personnage)
            if adversaires:
                if not personnage.etats:
                    adversaire = choice(adversaires)
                    personnage.attaquer(adversaire)
                yield SignalRepete(5)
            else:
                # On récupère les salles où il y a des possibilités de combat
                sorties = []
                avec_adversaires = []
                for sortie in salle.sorties:
                    if sortie and sortie.salle_dest:
                        sorties.append(sortie)
                        if self.get_adversaires(sortie.salle_dest,
                                personnage):
                            avec_adversaires.append(sortie)

                sortie = None
                if avec_adversaires:
                    sortie = choice(avec_adversaires)
                elif sorties:
                    sortie = choice(sorties)

                if sortie:
                    personnage.deplacer_vers(sortie.nom)

                yield SignalRepete(5)

    def get_adversaires(self, salle, personnage):
        """Retourne les adversaires du personnage."""
        adversaires = []
        identifiant = personnage.identifiant
        equipage = importeur.navigation.matelots[identifiant].equipage
        for pnj in salle.PNJ:
            if pnj is personnage:
                continue

            if pnj.identifiant not in importeur.navigation.matelots:
                continue

            matelot = importeur.navigation.matelots[pnj.identifiant]
            if equipage is not matelot.equipage:
                adversaires.append(pnj)

        return adversaires

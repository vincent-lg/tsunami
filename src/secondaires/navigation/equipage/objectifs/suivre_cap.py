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


"""Objectif suivre_cap."""

from primaires.vehicule.vecteur import get_direction
from secondaires.navigation.constantes import *
from secondaires.navigation.equipage.objectifs.rejoindre import Rejoindre

# Constantes
DISTANCE_MIN = 3

class SuivreCap(Rejoindre):

    """Objectif suivre_cap.

    Cet objectif, basé sur l'objectif rejoindre, demande à un
    équipage de suivre un cap assigné. Cet objectif est responsable
    de trouver la destination indiquée, la distance qui l'en sépare
    et d'utiliser la vitesse nécssaire, ainsi que de modifier le
    cap si besoin, quand le navire atteint sa destination.

    """

    cle = "suivre_cap"
    def __init__(self, equipage, vitesse_max=None):
        Rejoindre.__init__(self, equipage)
        self.vitesse_max = vitesse_max

    def trouver_cap(self):
        """Trouve le cap (x, y, vitesse).

        Cette méthode trouve le cap tel que renseigné par
        l'équipage.

        """
        equipage = self.equipage
        navire = self.navire
        commandants = equipage.get_matelots_au_poste("commandant", False)
        if commandants:
            commandant = commandants[0].personnage

        if equipage.destination and not self.doit_reculer:
            self.x, self.y = equipage.destination
            distance = self.get_distance()
            norme = distance.norme
            vitesse = get_vitesse_noeuds(norme)
            if norme < 40:
                vitesse = 0.6
            elif norme < 15:
                vitesse = 0.2
            elif vitesse > self.vitesse_max:
                vitesse = self.vitesse_max

            self.vitesse = vitesse
            direction = round(distance.direction)
            if distance.norme <= DISTANCE_MIN:
                # On cherche le point suivant sur la carte
                print("changement de point")
                try:
                    cle = equipage.caps[0]
                except IndexError:
                    suivant = None
                else:
                    trajet = importeur.navigation.trajets[cle]
                    suivant = trajet.points.get(tuple(equipage.destination))

                print("suivant", suivant)
                if suivant is None:
                    del equipage.caps[0]
                    try:
                        cle = equipage.caps[0]
                    except IndexError:
                        # Le cap n'est pas circulaire
                        equipage.destination = None
                        self.vitesse = 0
                        equipage.demander("relacher_rames",
                                personnage=commandant)
                        equipage.demander("relacher_gouvernail",
                                personnage=commandant)
                        equipage.demander("plier_voiles", None,
                                personnage=commandant)
                        equipage.demander("jeter_ancre", personnage=commandant)
                        equipage.objectifs.remove(self)
                        equipage.retirer_controle("vitesse")
                        return
                    else:
                        trajet = importeur.navigation.trajets[cle]
                        suivant = trajet.point_depart

                equipage.destination = suivant

        # On retransmet les contrôles
        Rejoindre.trouver_cap(self)

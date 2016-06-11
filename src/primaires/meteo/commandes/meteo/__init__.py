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


"""Package contenant la commande 'meteo'."""

from primaires.format.fonctions import oui_ou_non
from primaires.interpreteur.commande.commande import Commande
from .creer import PrmCreer
from .liste import PrmListe

class CmdMeteo(Commande):

    """Commande 'meteo'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "météo", "meteo")
        self.groupe = "administrateur"
        self.nom_categorie = "batisseur"
        self.aide_courte = "manipule la météorologie"
        self.aide_longue = \
            "Cette commande permet de manipuer les perturbations " \
            "météorologiques, dans un premier temps de savoir les " \
            "perturbations existantes et d'en ajouter si besoin."

    def ajouter_parametres(self):
        """Ajout des paramètres."""
        self.ajouter_parametre(PrmCreer())
        self.ajouter_parametre(PrmListe())

    def erreur_validation(self, personnage, dic_masques):
        """Définit la réaction de la commande lors d'une erreur."""
        zone = personnage.salle.zone
        msg = "Informations actuelles sur la météo :"
        msg += "\n  Température dynamique : " + oui_ou_non(
                importeur.meteo.temperature_dynamique)
        msg += "\n  Nombre de perturbations en jeu : {}".format(
                len(importeur.meteo.perturbations_actuelles))
        msg += "\n  Température de l'univers : {}°".format(
                importeur.meteo.temperature)
        msg += "\n  Température dans la zone {} : {}°".format(
                zone.cle, zone.temperature)

        # Affichage des perturbations les plus proches
        salle = personnage.salle
        if len(importeur.meteo.perturbations_actuelles) == 0:
            msg += "  \nIl n'y a pas de perturbations en jeu."
        elif salle.coords.valide:
            proches = sorted([(p, p.distance_au_centre(salle)) for p in \
                    importeur.meteo.perturbations_actuelles],
                    key=lambda c: c[1])
            msg += "\n  Perturbations proches :"
            for i, (perturbation, distance) in enumerate(proches):
                if i > 2:
                    break

                msg += "\n    {} distant de {} salles".format(
                        perturbation.nom_pertu, round(distance))
        else:
            msg += "\n  La salle actuelle n'a pas de coordonnées valides."

        return msg

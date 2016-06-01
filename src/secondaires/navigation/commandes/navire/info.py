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


"""Fichier contenant le paramètre 'info' de la commande 'navire'."""

from primaires.interpreteur.masque.parametre import Parametre
from primaires.format.fonctions import oui_ou_non
from secondaires.navigation.constantes import get_longitude_latitude

class PrmInfo(Parametre):

    """Commande 'navire info'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "info", "info")
        self.schema = "(<cle_navire>)"
        self.aide_courte = "donne des informations sur un navire"
        self.aide_longue = \
            "Cette commande donne des informations, soit sur le navire " \
            "passé en paramètre, soit sur le navire où vous vous trouvez " \
            "si aucun paramètre n'est précisé."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        navire = dic_masques["cle_navire"]
        salle = personnage.salle
        if navire is None:
            if not hasattr(salle, "navire") or salle.navire is None:
                personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
                return

            navire = salle.navire
        else:
            navire = navire.navire

        modele = navire.modele
        etendue = navire.etendue
        etendue = etendue and etendue.cle or "aucune"
        direction = navire.direction.direction
        direction = round(direction, 3)
        direction = str(direction).replace(".", ",")
        nom_direction = navire.direction.nom_direction
        vitesse = navire.vitesse.norme
        vitesse = round(vitesse, 3)
        vitesse = str(vitesse).replace(".", ",")
        vitesse_n = navire.vitesse_noeuds
        vitesse_n = round(vitesse_n, 3)
        vitesse_n = str(vitesse_n).replace(".", ",")
        acceleration = navire.acceleration.norme
        acceleration = round(acceleration, 3)
        acceleration = str(acceleration).replace(".", ",")
        dir_acceleration = navire.acceleration.direction
        dir_acceleration = round(dir_acceleration, 3)
        dir_acceleration = str(dir_acceleration).replace(".", ",")
        gouvernail = navire.gouvernail
        cale = navire.cale
        voiles = navire.voiles
        hissees = [v for v in voiles if v.hissee]
        rames = navire.rames
        if gouvernail:
            orient = gouvernail.orientation
            if orient < 0:
                orient = -orient
                msg_gouv = "poussé de {}° sur bâbord".format(orient)
            elif orient > 0:
                msg_gouv = "poussé de {}° sur tribord".format(orient)
            else:
                msg_gouv = "parfaitement au centre"
        else:
            msg_gouv = "aucun"
        msg_rames = ""
        if rames:
            for rame in rames:
                 msg_rames += ", " + rame.vitesse
            msg_rames = msg_rames.lstrip(", ")
        else:
            msg_rames = "Aucune"
        compteur = round(navire.compteur / 1000, 3)
        if compteur >= 2:
            compteur = "{} milles".format(str(compteur).replace(".", ","))
        else:
            compteur = "{} mille".format(str(compteur).replace(".", ","))

        msg = "Informations sur le navire {} :\n".format(navire.cle)
        msg += "\n  Modèle : {} ({})".format(modele.cle, modele.nom)
        msg += "\n  Nom : " + (navire.nom_personnalise if \
                navire.nom_personnalise else "Aucun")
        msg += "\n  Propriétaire : " + (navire.proprietaire and \
                navire.proprietaire.nom or "Aucun")
        msg += "\n  Étendue : " + etendue
        msg += " (profondeur={})".format(navire.profondeur)
        msg += "\n  Immobilisé : {}   En collision : {}   Orientation : " \
                "{}".format(oui_ou_non(navire.immobilise), oui_ou_non(
                navire.en_collision), navire.orientation)
        msg += "\n  Cale : " + str(int(cale.poids)).rjust(6)
        msg += " / " + str(int(cale.poids_max)).rjust(6) + " ("
        msg += str(int(cale.poids / cale.poids_max * 100)).rjust(3) + "%)"
        msg += "\n  Compteur : {}".format(compteur)
        msg += "\n  Coordonnées : {}".format(navire.position.coordonnees)
        msg += "\n  Point : {}".format(get_longitude_latitude(
                navire.position.x, navire.position.y))
        msg += "\n  Allure : {}".format(navire.nom_allure)
        msg += "\n  Voiles : {} / {}".format(len(hissees), len(voiles))
        msg += "\n  Rames : " + msg_rames
        msg += "\n  Gouvernail : " + msg_gouv
        msg += "\n  Vitesse : {} ({} noeuds)".format(vitesse, vitesse_n)
        msg += "\n  Accélération : {} ({}°)".format(acceleration,
                dir_acceleration)
        msg += "\n  Direction : {} ({})".format(direction, nom_direction)
        personnage << msg

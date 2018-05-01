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


"""Package contenant la commande 'calfeutrer'."""

from primaires.interpreteur.commande.commande import Commande
from secondaires.navigation.constantes import *

class CmdCalfeutrer(Commande):

    """Commande 'calfeutrer'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "calfeutrer", "seal")
        self.nom_categorie = "navire"
        self.aide_courte = "colmate une fissure dans la coque"
        self.aide_longue = \
            "Cette commande permet de colmater une fissure dans la " \
            "coque. Autrement dit, d'effectuer une réparation sommaire. " \
            "Si elle réussit, l'eau cessera d'envahir le navire, mais " \
            "la réparation ne sera pas très solide : si de nouveaux " \
            "dommages sont infligés à la coque, la voie d'eau sera " \
            "encore plus importante qu'auparavant. Pour faire cette " \
            "réparation sommaire, vous devez posséder sur vous un " \
            "conteneur particulier, contenant la poix et les différents " \
            "outils utilisés pour l'opération. Cette commande utilise " \
            "le tout automatiquement et vous ne devez posséder qu'un " \
            "seul objet. Quand une voie d'eau s'est déclarée cependant, " \
            "il est plus difficile de travailler au fur et à mesure " \
            "que l'eau monte. Le talent \"calfeutrage\" vous permet de " \
            "réussir plus facilement à réparer dans ces conditions. " \
            "L'autre solution consiste à écoper (en utilisant la " \
            "commande %écoper%) avant de réparer. Pour réparer plus " \
            "complètement un navire et rendre sa solidité à la coque, " \
            "vous devez aller dans un chantier naval."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        salle = personnage.salle
        if not hasattr(salle, "navire") or salle.navire is None:
            personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
            return

        navire = salle.navire
        if salle.voie_eau != COQUE_OUVERTE:
            personnage << "|err|Il n'y a aucune fissure dans la coque " \
                    "ici.|ff|"
            return

        # On cherche les outils pour colmater
        calfeutrage = None
        for objet in personnage.equipement.inventaire:
            if objet.est_de_type("calfeutrage") and objet.onces_contenu > 0:
                calfeutrage = objet
                break

        if calfeutrage is None:
            personnage << "|err|Vous ne possédez aucun conteneur " \
                    "susceptible de vous aider à réparer une coque.|ff|"
            return

        salle.colmater(personnage, calfeutrage)

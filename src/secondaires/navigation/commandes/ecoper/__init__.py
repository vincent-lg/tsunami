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


"""Package contenant la commande 'écoper'."""

from primaires.interpreteur.commande.commande import Commande
from secondaires.navigation.constantes import *

class CmdEcoper(Commande):

    """Commande 'écoper'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "écoper", "bale")
        self.nom_categorie = "navire"
        self.aide_courte = "écope"
        self.aide_longue = \
            "Cette commande permet d'écoper, c'est-à-dire de rejeter " \
            "à l'extérieur du navire une partie de l'eau qui s'y trouve. " \
            "Cette commande est souvent nécessaire juste avant ou après " \
            "la réparation d'une voie d'eau. Pour écoper, vous devez " \
            "disposer d'un conteneur particulier (les autres conteneurs " \
            "ne sont pas adaptés pour ce travail). Le maximum, fonction " \
            "de votre force, de la capacité du conteneur, de la quantité " \
            "d'eau qui se trouve ici, est toujours choisi. Cette " \
            "opération fatigue proportionnellement à la quantité d'eau " \
            "que vous récupérez dans le conteneur puis reversez par-dessus " \
            "bord."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        salle = personnage.salle
        if not hasattr(salle, "navire") or salle.navire is None:
            personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
            return

        navire = salle.navire
        if salle.poids_eau == 0:
            personnage << "|err|Il n'y a pas d'eau ici.|ff|"
            return

        # On cherche l'écope
        ecope = None
        for objet in personnage.equipement.inventaire:
            if objet.est_de_type("écope"):
                ecope = objet
                break

        if ecope is None:
            personnage << "|err|Vous ne possédez aucune écope.|ff|"
            return

        salle.ecoper(personnage, ecope)

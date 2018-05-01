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


"""Ce fichier contient la classe Neige, détaillée plus bas."""

from .base import *

class Neige(BasePertu):

    """Classe abstraite représentant la perturbation 'neige'.

    """

    nom_pertu = "neige"
    rayon_max = 10
    duree_max = 8
    temperature_max = 4
    origine = False
    attributs = ("neige", "blanc", "nuage", "glacial", "humide", "brise")

    def __init__(self, pos):
        """Constructeur de la perturbation"""
        BasePertu.__init__(self, pos)
        self.flags = OPAQUE
        self.alea_dir = 1
        self.etat = [
            (10, "De fins flocons tourbillonnent dans l'air frais."),
        ]
        self.message_fin = "Les nuages blancs se divisent en fines " \
                "écharpes emportées par le vent et la neige cesse."
        self.message_entrer = "De lourds nuages blancs " \
                "arrivent {dir}, apportant la neige."
        self.message_sortir = "Les lourds nuages blancs s'éloignent " \
                "peu à peu vers {dir} et la neige cesse."
        self.fins_possibles = [
            ("tempete_neige", "Le vent forcit soudain et la neige " \
                    "devient subitement épaisse.", 30),
        ]

    def action_cycle(self, salles):
        """Définit une ou plusieurs actions effectuées à chaque cycle."""
        for salle in salles:
            if salle.peut_affecter("neige"):
                salle.affecte("neige", 2, 1)

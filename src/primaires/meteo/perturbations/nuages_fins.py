# -*-coding:Utf-8 -*

# Copyright (c) 2010 LE GOFF Vincent
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


"""Ce fichier contient la classe NuagesFins, détaillée plus bas."""

from .base import *

class NuagesFins(BasePertu):
    
    """Classe représentant la perturbation 'nuages_fins'.
    
    """
    
    nom_pertu = "nuages_fins"
    rayon_max = 23
    duree_max = 18
    
    def __init__(self, pos):
        """Constructeur de la perturbation"""
        BasePertu.__init__(self, pos)
        self.flags = AUCUN_FLAG
        self.alea_dir = 0
        self.etat = [
            (10, "De fins nuages cotonneux croisent dans le ciel en haute " \
                    "altitude."),
        ]
        self.message_debut = "Des rubans de nuages laiteux se forment haut " \
                "dans le ciel."
        self.message_fin = "Les légers nuages s'effilochent et laissent " \
                "place à un ciel d'azur pur."
        self.message_entrer = "Quelques nuages venus {dir} projettent une " \
                "ombre diaphane sur le sol."
        self.message_sortir = "Le coton céleste continue sa course vers " \
                "{dir}, porté par le vent."
        self.fins_possibles = [
            ("nuages", "Les nuées s'épaississent, comme gonflées par un " \
                    "souffle invisible.", 12),
        ]

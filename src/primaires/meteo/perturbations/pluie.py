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


"""Ce fichier contient la classe Pluie, détaillée plus bas."""

from .base import *

class Pluie(BasePertu):
    
    """Classe abstraite représentant la perturbation 'pluie'.
    
    """
    
    nom_pertu = "pluie"
    rayon_max = 16
    duree_max = 12
    temperature_min = 4
    origine = False
    
    def __init__(self, pos):
        """Constructeur de la perturbation"""
        BasePertu.__init__(self, pos)
        self.flags = OPAQUE
        self.alea_dir = 4
        self.etat = [
            (5, "Une pluie incessante et violente tombe du ciel en colère."),
            (10, "Une fine pluie martèle le sol dans un doux crépitement."),
        ]
        self.message_debut = "Quelques nuages s'amoncellent, grossisent " \
                "puis donnent naissance à une averse."
        self.message_fin = "Les nuées se dispersent rapidement et la pluie " \
                "cesse."
        self.message_entrer = "Des nuages gonflés d'eau arrivent {dir} et " \
                "apportent la pluie."
        self.message_sortir = "Les nuages s'éloignent peu à peu vers {dir}, " \
                "la pluie cessant soudain."
        self.fins_possibles = [
            ("nuages", "L'averse cesse sans un souffle mais les nuages " \
                    "restent, encore menaçants.", 12),
            ("orage", "La pluie s'intensifie soudain et le tonnerre retentit.",
                    30),
        ]

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


"""Ce fichier contient la classe NuagesNeige, détaillée plus bas."""

from .base import *

class NuagesNeige(BasePertu):
    
    """Classe abstraite représentant la perturbation 'nuages_neige'.
    
    """
    
    nom_pertu = "nuages_neige"
    rayon_max = 10
    duree_max = 6
    temperature_max = 4
    
    def __init__(self, pos):
        """Constructeur de la perturbation"""
        BasePertu.__init__(self, pos)
        self.flags = OPAQUE
        self.alea_dir = 1
        self.etat = [
            (5, "D'épais nuages chargés de neige croisent dans le ciel."),
            (10, "Quelques nuages blancs flottent dans le ciel."),
        ]
        self.message_debut = "De fines volutes s'épaississent pour " \
                "former peu à peu de lourds nuages blancs."
        self.message_fin = "Les nuages blancs se divisent en fines " \
                "écharpes emportées par le vent."
        self.message_entrer = "De lourds nuages blancs " \
                "arrivent {dir}, portés par le vent."
        self.message_sortir = "Les lourds nuages blancs s'éloignent " \
                "peu à peu vers {dir}."
        self.fins_possibles = [
            ("neige", "De fins flocons commencent à tourbillonner " \
                    "vers le sol dans un doux chuintement.", 60),
            ("tempete_neige", "Le vent forcit soudain et d'épais " \
                    "flocons commencent à choire des lourds nuages.", 70),
            ("grele", "Des nuages blancs commencent à tomber de " \
                    "fins grêlons.", 77),
        ]

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


"""Ce fichier contient la classe Nuages, détaillée plus bas."""

from .base import *

class Nuages(BasePertu):
    
    """Classe abstraite représentant la perturbation 'nuages'.
    
    """
    
    nom_pertu = "nuages"
    rayon_max = 10
    duree_max = 6
    
    def __init__(self, pos):
        """Constructeur de la perturbation"""
        BasePertu.__init__(self, pos)
        self.flags = OPAQUE
        self.alea_dir = 1
        self.etat = [
            (5, "De lourds nuages sont amoncellés au-dessus de vous."),
            (10, "Quelques nuages gris, s'épaississant non loin, flottent" \
                    "dans le ciel au gré des vents."),
        ]
        self.message_debut = "Quelques voiles de brume s'agrègent peu à peu" \
                "pour former un plafond nuageux menaçant."
        self.message_fin = "Les nuées se dispersent rapidement."
        self.message_sortir = "Les nuages s'éloignent peu à peu vers {dir}."

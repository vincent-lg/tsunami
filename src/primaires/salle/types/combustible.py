# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 NOEL-BARON Léo
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


"""Fichier contenant le type combustible."""

from primaires.interpreteur.editeur.entier import Entier
from primaires.interpreteur.editeur.selection import Selection
from primaires.objet.types.base import BaseType

class Combustible(BaseType):
    
    """Type d'objet: combustible.
    
    """
    
    nom_type = "combustible"
    
    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        BaseType.__init__(self, cle)
        self.terrains = []
        self.rarete = 1
        self.qualite = 2
        
        # Editeurs
        self.etendre_editeur("t", "terrains", Selection, self, "terrains",
                list(importeur.salle.terrains.keys()))
        self.etendre_editeur("r", "rareté", Entier, self, "rarete", 1, 10)
        self.etendre_editeur("a", "qualité", Entier, self, "qualite", 1, 10)
    
    @property
    def aff_terrains(self):
        return ", ".join(self.terrains) if self.terrains else "aucun"
    
    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes"""
        l_terrains = sorted(type(self).importeur.salle.terrains.keys())
        terrains = enveloppes["t"]
        terrains.apercu = "{objet.aff_terrains}"
        terrains.prompt = "Entrez un terrain : "
        terrains.aide_courte = \
            "Entrez les |ent|terrains|ff| où l'on peut trouver ce " \
            "combustible.\n\nTerrains disponibles : {}.\n\n" \
            "Terrains actuels : {{objet.aff_terrains}}".format(
            ", ".join(l_terrains))
        
        rarete = enveloppes["r"]
        rarete.apercu = "{objet.rarete}"
        rarete.prompt = "Rareté du combustible : "
        rarete.aide_courte = \
            "Entrez la |ent|rareté|ff| du combustible, entre |cmd|1|ff| " \
            "(courant) et |cmd|10|ff| (rare).\n\n" \
            "Rareté actuelle : {objet.rarete}"
        
        qualite = enveloppes["a"]
        qualite.apercu = "{objet.qualite}"
        qualite.prompt = "Qualité du combustible : "
        qualite.aide_courte = \
            "Entrez la |ent|qualité|ff| du combustible, entre |cmd|1|ff| " \
            "(mauvais) et |cmd|10|ff| (très bon).\n\n" \
            "Qualité actuelle : {objet.qualite}"

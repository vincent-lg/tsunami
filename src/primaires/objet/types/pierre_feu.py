# -*-coding:Utf-8 -*

# Copyright (c) 2012 NOEL-BARON Léo
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


"""Fichier contenant le type pierre à feu."""

from primaires.interpreteur.editeur.entier import Entier
from primaires.objet.types.base import BaseType

class PierreFeu(BaseType):
    
    """Type d'objet: pierre à feu.
    
    """
    
    nom_type = "pierre à feu"
    
    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        BaseType.__init__(self, cle)
        self.efficacite = 30
        
        # Editeur
        self.etendre_editeur("f", "efficacite", Entier, self, "efficacite",
                1, 50)
    
    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes"""
        efficacite = enveloppes["f"]
        efficacite.apercu = "{objet.efficacite}"
        efficacite.prompt = "Entrez une efficacité : "
        efficacite.aide_courte = \
            "Entrez l'|ent|efficacité|ff| initiale de la pierre, de " \
            "|cmd|1|ff| (quasi nulle) à |cmd|50|ff| (maximale).\nCette " \
            "efficacité conditionne la solidité de la pierre et se " \
            "décrémente de 1\nà chaque utilisation.\n\n" \
            "Efficacité actuelle : {objet.efficacite}"

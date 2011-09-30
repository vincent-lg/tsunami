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


"""Fichier contenant le type Nourriture."""

from primaires.interpreteur.editeur.uniligne import Uniligne
from bases.objet.attribut import Attribut
from .base import BaseType

class Nourriture(BaseType):
    
    """Type d'objet: nourriture.
    
    """
    
    nom_type = "nourriture"
    
    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        BaseType.__init__(self, cle)
        self.qualite = 1
        self.nourrissant = 1
        self.etendre_editeur("u", "qualité", Uniligne, self, "qualite")
        self.etendre_editeur("o", "nourrissant", Uniligne, self, "nourrissant")
    
    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes"""
        qualite = enveloppes["u"]
        qualite.apercu = "{objet.qualite}"
        qualite.prompt = "Qualité de la nourriture : "
        qualite.aide_courte = \
            "Entrez la |ent|qualité|ff| de la nourriture, entre |cmd|1|ff| " \
            "et |cmd|10|ff|\nou |cmd|/|ff| pour revenir à la fenêtre " \
            "parente.\n\n" \
            "Qualité actuelle : {objet.qualite}"
        qualite.type = int
        
        nourrissant = enveloppes["o"]
        nourrissant.apercu = "{objet.nourrissant}"
        nourrissant.prompt = "Valeur nourrissante : "
        nourrissant.aide_courte = \
            "Entrez la |ent|valeur nourrissante|ff| de la nourriture, entre " \
            "|cmd|1|ff| et |cmd|10|ff|\nou |cmd|/|ff| pour revenir à la " \
            "fenêtre parente.\n\n" \
            "Valeur nourrissante actuelle : {objet.nourrissant}"
        nourrissant.type = int

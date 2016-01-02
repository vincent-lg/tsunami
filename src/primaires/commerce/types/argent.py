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


"""Fichier contenant le type Argent."""

from primaires.interpreteur.editeur.uniligne import Uniligne
from bases.objet.attribut import Attribut
from primaires.objet.types.base import BaseType

class Argent(BaseType):
    
    """Type d'objet: argent.
    
    """
    
    nom_type = "argent"
    
    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        BaseType.__init__(self, cle)
        self.unique = False
        self.valeur = 1
        self.sans_prix = True
        self.etendre_editeur("m", "valeur monétaire", Uniligne, self, "valeur")
    
    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes"""
        valeur = enveloppes["m"]
        valeur.apercu = "{objet.valeur}"
        valeur.prompt = "Valeur monétaire : "
        valeur.aide_courte = \
            "Entrez la |ent|valeur monétaire|ff| de l'argent, supérieur " \
            "ou égal à |cmd|1|ff|.\n" \
            "Entrez |cmd|/|ff| pour revenir à la fenêtre parente.\n\n" \
            "Valeur monétaire actuelle : {objet.valeur}"
        valeur.type = int
    
    def peut_vendre(self, vendeur):
        """On ne peut en aucun cas vendre de l'argent."""
        return False

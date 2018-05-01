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


"""Fichier contenant le type ustensile."""

from primaires.objet.types.conteneur_nourriture import ConteneurNourriture
from primaires.interpreteur.editeur.uniligne import Uniligne
from primaires.interpreteur.editeur.entier import Entier
from corps.fonctions import lisser

class Ustensile(ConteneurNourriture):
    
    """Type d'objet: ustensile.
    
    """
    
    nom_type = "ustensile"
    
    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        ConteneurNourriture.__init__(self, cle)
        self.qualite = 10
        self.etat_cuisson = "mijote sur le feu"
        self.etendre_editeur("a", "qualité", Entier, self, "qualite", 1, 10)
        self.etendre_editeur("c", "état en cours de cuisson",
                Uniligne, self, "etat_cuisson")
    
    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes"""
        ConteneurNourriture.travailler_enveloppes(self, enveloppes)
        
        qualite = enveloppes["a"]
        qualite.apercu = "{objet.qualite}"
        qualite.prompt = "Qualité de l'ustensile : "
        qualite.aide_courte = \
            "Entrez la |ent|qualité|ff| de l'ustensile, |cmd|1|ff| au " \
            "minimum, |cmd|10|ff| au maximum, ou |cmd|/|ff| pour\nrevenir " \
            "à la fenêtre parente.\n\n" \
            "Qualité actuelle : {objet.qualite}"
        
        etat_cuisson = enveloppes["c"]
        etat_cuisson.apercu = "{objet.etat_cuisson}"
        etat_cuisson.prompt = "Etat de l'ustensile : "
        etat_cuisson.aide_courte = \
            "Entrez l'|ent|état|ff| de l'ustensile posé sur un feu ou " \
            "|cmd|/|ff| pour revenir à\nla fenêtre parente.\n\n" \
            "Etat actuel : {objet.etat_cuisson}"

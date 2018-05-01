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


"""Fichier contenant le type poisson."""

from primaires.objet.types.nourriture import Nourriture
from primaires.interpreteur.editeur.entier import Entier

class Poisson(Nourriture):
    
    """Type d'objet: poisson.
    
    """
    
    nom_type = "poisson"
    
    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        Nourriture.__init__(self, cle)
        self.nourrissant = 3
        self.niveau_peche = 5
        self.etendre_editeur("ni", "niveau", Entier, self, "niveau_peche",
                1, 100)

    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes"""
        Nourriture.travailler_enveloppes(self, enveloppes)
        niveau = enveloppes["ni"]
        niveau.apercu = "{objet.niveau_peche}"
        niveau.prompt = "Niveau pêche du poisson : "
        niveau.aide_courte = \
            "Entrez le |ent|niveau|ff| du poisson, entre |cmd|1|ff| " \
            "et |cmd|100|ff|\nou |cmd|/|ff| pour revenir à la fenêtre " \
            "parente.\n\n" \
            "Le niveau du poisson influence l'XP gagnée par le joueur " \
            "qui le pêchera.\n" \
            "C'est un calcul d'XP relative se faisant entre le niveau " \
            "du poisson et\n" \
            "le niveau survie du joueur pêchant le poisson. Plus " \
            "le poisson est difficile\n" \
            "et rare, plus son niveau peut être élevé. Au contraire, " \
            "un poisson très\n" \
            "commun ne devra pas être au-delà du niveau 10.\n\n" \
            "Niveau actuel : {objet.niveau_peche}"

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


"""Fichier contenant la classe EdtCycle."""

from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.uniligne import Uniligne
from primaires.interpreteur.editeur.entier import Entier
from primaires.interpreteur.editeur.flag import Flag
from .edt_periodes import EdtPeriodes

class EdtCycle(Presentation):
    
    """Classe définissant l'éditeur de cycle végétal."""
    
    def __init__(self, instance_connexion, cycle, attribut=None):
        """Constructeur de l'éditeur"""
        Presentation.__init__(self, instance_connexion, cycle, attribut, False)
        if instance_connexion and cycle:
            self.construire(cycle)
    
    def __getnewargs__(self):
        return (None, None)
    
    def construire(self, cycle):
        """Construction de l'éditeur"""
        # Nom
        nom = self.ajouter_choix("nom", "n", Uniligne, cycle, "nom")
        nom.parent = self
        nom.prompt = "Nom du cycle : "
        nom.apercu = "{objet.nom}"
        nom.aide_courte = \
            "Entrez le |ent|nouveau nom|ff| du cycle, ou " \
            "|cmd|/|ff| pour revenir à la\nfenêtre parente.\n\n" \
            "Nom actuel : {objet.nom}"
        
        # Age
        age = self.ajouter_choix("age minimum", "a", Entier, cycle,
                "age", 0)
        age.parent = self
        age.prompt = "Age minimum du cycle : "
        age.apercu = "{objet.age}"
        age.aide_courte = \
            "Entrez l'|ent|âge minimum|ff| d'une plante de ce cycle ou " \
            "|cmd|/|ff| pour revenir à la\nfenêtre parente.\n\n" \
            "Age minimum actuel : |bc|{valeur}|ff|"
        
        # Durée
        duree = self.ajouter_choix("durée du cycle", "d", Entier, cycle,
                "duree", 1)
        duree.parent = self
        duree.prompt = "Durée en année du cycle : "
        duree.apercu = "{objet.duree}"
        duree.aide_courte = \
            "Entrez |ent|la durée|ff| du cycle ou " \
            "|cmd|/|ff| pour revenir à la\nfenêtre parente.\n\n" \
            "Un cycle dure au minimum un an.\n\n" \
            "Durée actuelle : |bc|{valeur}|ff|"
        
        # Variation
        variation = self.ajouter_choix("variation", "v", Entier, cycle,
                "variation", 0)
        variation.parent = self
        variation.prompt = "Variation en année du cycle : "
        variation.apercu = "{objet.variation}"
        variation.aide_courte = \
            "Entrez |ent|la variation|ff| du cycle en année " \
            "|cmd|/|ff| pour revenir à la\nfenêtre parente.\n\n" \
            "La variation influence aléatoirement la fin du " \
            "cycle. Si un cycle comence\n" \
            "à l'âge 0 de la plante et dure 3 ans avec une " \
            "variation de 1, la plante\n" \
            "pourra passer au cycle suivant entre 2 et 4 ans.\n\n" \
            "Variation actuelle : |bc|{valeur}|ff|"
        
        # Périodes
        periodes = self.ajouter_choix("périodes", "p", EdtPeriodes, cycle)
        periodes.parent = self
        periodes.aide_courte = "Options :\n" \
            "  |ent|/n <nouveau nom>|ff| : ajoute une période\n" \
            "  |ent|/d <nom>|ff| : supprime une période"
        
        # Visible
        visible = self.ajouter_choix("visible", "vi", Flag, cycle,
                "visible")
        visible.parent = self

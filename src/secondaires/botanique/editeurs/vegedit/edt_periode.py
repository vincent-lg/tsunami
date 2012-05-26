# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Fichier contenant la classe Edtperiode."""

from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.uniligne import Uniligne
from primaires.interpreteur.editeur.description import Description
from primaires.interpreteur.editeur.entier import Entier
from primaires.interpreteur.editeur.flag import Flag
from .edt_date import EdtDate

class EdtPeriode(Presentation):
    
    """Classe définissant l'éditeur de periode végétal."""
    
    def __init__(self, instance_connexion, periode, attribut=None):
        """Constructeur de l'éditeur"""
        Presentation.__init__(self, instance_connexion, periode, attribut, False)
        if instance_connexion and periode:
            self.construire(periode)
    
    def __getnewargs__(self):
        return (None, None)
    
    def construire(self, periode):
        """Construction de l'éditeur"""
        # Nom
        nom = self.ajouter_choix("nom", "n", Uniligne, periode, "nom")
        nom.parent = self
        nom.prompt = "Nom du periode : "
        nom.apercu = "{objet.nom}"
        nom.aide_courte = \
            "Entrez le |ent|nouveau nom|ff| du periode, ou " \
            "|cmd|/|ff| pour revenir à la\nfenêtre parente.\n\n" \
            "Nom actuel : {objet.nom}"
        
        # Nom singulier
        nom_s = self.ajouter_choix("nom singulier de la plante", "s",
                Uniligne, periode, "nom_singulier")
        nom_s.parent = self
        nom_s.prompt = "Nom singulier de la plante pour cette période : "
        nom_s.apercu = "{objet.nom_singulier}"
        nom_s.aide_courte = \
            "Entrez le |ent|nouveau nom singulier|ff| de la plante ou " \
            "|cmd|/|ff| pour revenir à la\nfenêtre parente.\n\n" \
            "Nom singulier actuel : {objet.nom_singulier}"
        
        # Nom pluriel
        nom_p = self.ajouter_choix("nom pluriel de la plante", "p",
                Uniligne, periode, "nom_pluriel")
        nom_p.parent = self
        nom_p.prompt = "Nom pluriel de la plante pour cette période : "
        nom_p.apercu = "{objet.nom_pluriel}"
        nom_p.aide_courte = \
            "Entrez le |ent|nouveau nom pluriel|ff| de la plante ou " \
            "|cmd|/|ff| pour revenir à la\nfenêtre parente.\n\n" \
            "Nom pluriel actuel : {objet.nom_pluriel}"
        
        # Description
        description = self.ajouter_choix("description", "d", Description, \
                periode)
        description.parent = self
        description.apercu = "{objet.description.paragraphes_indentes}"
        description.aide_courte = \
            "| |tit|" + "Description de la période {}".format(
            periode).ljust(76) + "|ff||\n" + self.opts.separateur
        
        # Date de fin
        date = self.ajouter_choix("date de fin", "t", EdtDate, periode)
        date.parent = self
        date.prompt = "Entrez la date de fin de période : "
        date.apercu = "{objet.date_fin}"
        
        # Variation
        variation = self.ajouter_choix("variation", "v", Entier, periode,
                "variation", 0)
        variation.parent = self
        variation.prompt = "Variation en année de la période : "
        variation.apercu = "{objet.variation}"
        variation.aide_courte = \
            "Entrez |ent|la variation|ff| de la période en année ou " \
            "|cmd|/|ff| pour revenir à la\nfenêtre parente.\n\n" \
            "La variation influence aléatoirement la fin de la " \
            "période. Si une période fini\n" \
            "le dixième jour du quatrième mois avec " \
            "une variation de 20 jours, la\n" \
            "plante pourrait passer à la période suivante " \
            "le vingtième jour du\n" \
            "troisième mois au plus tôt.\n\n" \
            "Variation actuelle : |bc|{valeur}|ff|"

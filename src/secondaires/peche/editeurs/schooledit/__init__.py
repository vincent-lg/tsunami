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


"""Package contenant l'éditeur 'schooledit'.

Si des redéfinitions de contexte-éditeur standard doivent être faites, elles
seront placées dans ce package

Note importante : ce package contient la définition d'un éditeur, mais
celui-ci peut très bien être étendu par d'autres modules. Au quel cas,
les extensions n'apparaîtront pas ici.

"""

from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.description import Description
from primaires.interpreteur.editeur.uniligne import Uniligne
from primaires.interpreteur.editeur.entier import Entier
from primaires.interpreteur.editeur.choix import Choix
from primaires.interpreteur.editeur.flag import Flag
from .edt_etendue import EdtEtendue
from .edt_poissons import EdtPoissons
from .supprimer import NSupprimer

class EdtSchooledit(Presentation):
    
    """Classe définissant l'éditeur de banc de poisson 'schooledit'.
    
    """
    
    nom = "schooledit"
    
    def __init__(self, personnage, banc):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None
        
        Presentation.__init__(self, instance_connexion, banc)
        if personnage and banc:
            self.construire(banc)
    
    def __getnewargs__(self):
        return (None, None)
    
    def construire(self, banc):
        """Construction de l'éditeur"""
        # Etendue
        etendue = self.ajouter_choix("etendue", "e", EdtEtendue, banc)
        etendue.parent = self
        etendue.prompt = "Entrez une clé d'étendue : "
        etendue.apercu = "{objet.aff_etendue}"
        etendue.aide_courte = \
            "Entrez une |ent|clé d'étendue|ff|, ou " \
            "|cmd|/|ff| pour revenir à la\nfenêtre parente.\n\n" \
            "Etendue actuelle : {objet.aff_etendue}"
        
        # Abondance
        abondance = self.ajouter_choix("abondance maximum", "a", Entier, banc,
                "abondance_max")
        abondance.parent = self
        abondance.prompt = "Abondance du banc (en kilogramme par heure) : "
        abondance.apercu = "{objet.abondance_max} Kg/h"
        abondance.aide_courte = \
            "Entrez l'|ent|abondance maximum|ff| en Kg / h du banc ou " \
            "|cmd|/|ff| pour revenir à la\nfenêtre parente.\n\n" \
            "L'abondance doit être précisée en kilogramme par heure.\n" \
            "Chaque poisson pêché dans ce banc ôtera de l'abondance " \
            "actuelle son propre\npoids.\n\n" \
            "Abondance maximum actuelle : |bc|{valeur}|ff|"
        
        # Poissons
        poissons = self.ajouter_choix("poissons", "p", EdtPoissons, banc)
        poissons.parent = self
        poissons.aide_courte = \
            "Entrez |cmd|/|ff| pour revenir à la\nfenêtre parente.\n\n" \
            "Pour ajouter un poisson dans ce banc, entrez la clé de " \
            "l'objet poisson suivie\n" \
            "d'un espace et de sa probabilité\n" \
            "Exemple : |ent|truite 5|ff|\n" \
            "Pour le supprimer, précisez une probabilité de |ent|0|ff|.\n" \
            "La probabilité maximale n'est pas 100 mais la somme des " \
            "probabilité de\n" \
            "chaque poisson."
        
        # Supprimer
        sup = self.ajouter_choix("supprimer", "sup", NSupprimer,
                banc)
        sup.parent = self
        sup.aide_courte = "Souhaitez-vous réellement supprimer " \
                "le banc {} ?".format(banc.cle)

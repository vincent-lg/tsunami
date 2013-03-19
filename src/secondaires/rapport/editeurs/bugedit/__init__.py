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


"""Package contenant l'éditeur 'bugedit'.

Si des redéfinitions de contexte-éditeur standard doivent être faites, elles
seront placées dans ce package

Note importante : ce package contient la définition d'un éditeur, mais
celui-ci peut très bien être étendu par d'autres modules. Au quel cas,
les extensions n'apparaîtront pas ici.

"""

from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.description import Description
from primaires.interpreteur.editeur.uniligne import Uniligne
from primaires.interpreteur.editeur.choix import Choix
from primaires.interpreteur.editeur.flag import Flag
from secondaires.rapport.constantes import CATEGORIES
from .edt_annuler import EdtAnnuler
from .edt_envoyer import EdtEnvoyer

class EdtBugedit(Presentation):
    
    """Classe définissant l'éditeur de rapport 'bugedit'.
    
    """
    
    nom = "bugedit"
    
    def __init__(self, personnage, rapport):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None
        
        Presentation.__init__(self, instance_connexion, rapport,
                peut_quitter=False)
        if personnage and rapport:
            self.construire(rapport)
    
    def __getnewargs__(self):
        return (None, None)
    
    def construire(self, rapport):
        """Construction de l'éditeur"""
        # Titre
        titre = self.ajouter_choix("titre", "t", Uniligne, rapport, "titre")
        titre.parent = self
        titre.prompt = "Titre du rapport : "
        titre.apercu = "{objet.titre}"
        titre.aide_courte = \
            "Entrez le |ent|titre|ff| du rapport ou |cmd|/|ff| pour revenir " \
            "à la fenêtre parente.\n\nTitre actuel : |bc|{objet.titre}|ff|"
        
        # Description
        description = self.ajouter_choix("description", "d", Description, \
                rapport)
        description.parent = self
        description.apercu = "{objet.description.paragraphes_indentes}"
        description.aide_courte = \
            "| |tit|" + "Description du rapport #{}".format(
            rapport.id).ljust(76) + "|ff||\n" + self.opts.separateur
        
        # Catégorie
        categories = sorted(CATEGORIES)
        categorie = self.ajouter_choix("catégorie", "c", Choix, rapport,
                "categorie", categories)
        categorie.parent = self
        categorie.prompt = "Catégorie du rapport : "
        categorie.apercu = "{objet.categorie}"
        categorie.aide_courte = \
            "Entrez la |ent|catégorie|ff| du rapport ou |cmd|/|ff| pour " \
            "revenir à la fenêtre parente.\n\nCatégories disponibles : {}.\n" \
            "\nCatégorie actuelle : |bc|{{objet.categorie}}|ff|".format(
            ", ".join(categories))
        # Public
        public = self.ajouter_choix("public", "p", Flag, rapport, "public")
        public.parent = self
        # Envoyer
        envoyer = self.ajouter_choix("envoyer", "e", EdtEnvoyer, rapport)
        envoyer.parent = self
        
        # Annuler
        annuler = self.ajouter_choix("annuler et quitter la fenêtre", "ann", \
                EdtAnnuler, rapport)
        annuler.parent = self

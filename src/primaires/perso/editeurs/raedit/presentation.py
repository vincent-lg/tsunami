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


"""Fichier contenant la classe EdtPresentation, détaillée plus bas.

"""

from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.description import Description
from primaires.interpreteur.editeur.uniligne import Uniligne
from .edt_stats import EdtStats
from .edt_squelette import EdtSquelette
from .edt_genres import EdtGenres

class EdtPresentation(Presentation):
    
    """Classe définissant l'éditeur de race 'raedit'.
    
    """
    
    def __init__(self, personnage, race, attribut=""):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None
        
        Presentation.__init__(self, instance_connexion, race)
        if personnage and race:
            self.construire(race)
    
    def __getnewargs__(self):
        return (None, None)
    
    def construire(self, race):
        """Construction de l'éditeur"""
        race = self.objet
        
        # Description
        description = self.ajouter_choix("description", "d", Description, \
                race)
        description.parent = self
        description.apercu = "{objet.description.paragraphes_indentes}"
        description.aide_courte = \
            "| |tit|" + "Description de la race {}".format(race).ljust(
            76) + "|ff||\n" + self.opts.separateur
        
        # Genres
        genres = self.ajouter_choix("genres", "g", EdtGenres, race.genres)
        genres.parent = self
        genres.prompt = "Entrez un genre : "
        genres.apercu = "{objet.str_genres}"
        genres.aide_courte = \
            "Entrez un |ent|genre|ff| suivi de sa correspondance " \
            "grammaticale (masculin ou féminin)\n" \
            "pour l'ajouter ; simplement |cmd|masculin|ff| ou " \
            "|cmd|féminin|ff| pour ajouter ceux-là. Si\n" \
            "vous envoyez un genre déjà dans la liste, il sera supprimé.\n" \
            "Entrez |cmd|/|ff| pour revenir à la fenêtre parente.\n\n" \
            "Genre(s) actuel(s) :\n      {objet.tableau_genres}"
        
        # Stats
        stats = self.ajouter_choix("stats", "s", EdtStats, \
                race.stats)
        stats.parent = self
        
        # Squelette
        squelette = self.ajouter_choix("squelette", "sq", EdtSquelette,
                race)
        squelette.parent = self
        squelette.prompt = "Clé du squelette : "
        squelette.apercu = "{objet.nom_squelette}"
        squelette.aide_courte = \
            "Entrez la |ent|clé identifiante|ff| du squelette ou |cmd|/|ff| " \
            "pour revenir à la fenêtre parente.\n\nSquelette actuel : " \
            "|bc|{objet.cle_squelette}|ff|"

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


"""Fichier contenant la classe Pedit, détaillée plus bas.

"""

from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.description import Description
from primaires.interpreteur.editeur.uniligne import Uniligne
from primaires.interpreteur.editeur.entier import Entier
from primaires.interpreteur.editeur.flottant import Flottant
from primaires.scripting.editeurs.edt_script import EdtScript
from .edt_noms import EdtNoms
from .edt_stats import EdtStats
from .edt_race import EdtRace
from .edt_genre import EdtGenre
from .edt_squelette import EdtSquelette
from .edt_equipement import EdtEquipement

class EdtPedit(Presentation):
    
    """Classe définissant l'éditeur de prototype de pnj 'pedit'.
    
    """
    
    nom = "pedit"
    def __init__(self, personnage, prototype, attribut=""):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None
        
        Presentation.__init__(self, instance_connexion, prototype)
        if personnage and prototype:
            self.construire(prototype)
    
    def __getnewargs__(self):
        return (None, None)
    
    def construire(self, prototype):
        """Construction de l'éditeur"""
        prototype = self.objet
        
        # Noms
        noms = self.ajouter_choix("noms", "n", EdtNoms, prototype)
        noms.parent = self
        noms.apercu = "{objet.nom_singulier}"
        
        # Description
        description = self.ajouter_choix("description", "d", Description, \
                prototype)
        description.parent = self
        description.apercu = "{objet.description.paragraphes_indentes}"
        description.aide_courte = \
            "| |tit|" + "Description du PNJ {}".format(prototype).ljust(
            76) + "|ff||\n" + self.opts.separateur
        
        # Stats
        stats = self.ajouter_choix("stats", "s", EdtStats, \
                prototype.stats)
        stats.parent = self
        
        # Race
        race = self.ajouter_choix("race", "r", EdtRace,
                prototype)
        race.parent = self
        race.prompt = "Nom de la race : "
        race.apercu = "{objet.nom_race}"
        race.aide_courte = \
            "Entrez le |ent|nom|ff| de la race ou |cmd|/|ff| " \
            "pour revenir à la fenêtre parente.\n\nRace actuelle : " \
            "|bc|{objet.nom_race}|ff|"
        
        # Genre
        genre = self.ajouter_choix("genre", "g", EdtGenre, prototype)
        genre.parent = self
        genre.prompt = "Entrez un genre : "
        genre.apercu = "{objet.genre}"
        genre.aide_courte = \
            "Entrez le |ent|genre|ff| du PNJ ou |cmd|/|ff| " \
            "pour revenir à la fenêtre parente.\n\nGenres disponibles : " \
            "|bc|{objet.genres_possibles}|ff|\nGenre actuel : " \
            "|bc|{objet.genre}|ff|"
        
        # Squelette
        squelette = self.ajouter_choix("squelette", "sq", EdtSquelette,
                prototype)
        squelette.parent = self
        squelette.prompt = "Clé du squelette : "
        squelette.apercu = "{objet.nom_squelette}"
        squelette.aide_courte = \
            "Entrez la |ent|clé identifiante|ff| du squelette ou |cmd|/|ff| " \
            "pour revenir à la fenêtre parente.\n\nSquelette actuel : " \
            "|bc|{objet.cle_squelette}|ff|"
        
        # Squelette
        eq = self.ajouter_choix("equipement", "eq", EdtEquipement,
                prototype)
        eq.parent = self
        eq.aide_courte = \
            "Entrez |cmd|/|ff| pour revenir à la fenêtre précédente.\n" \
            "Pour ajouter un nouvel emplacement défini dans l'équipement, " \
            "entrez |cmd|le nom du\nmembre|ff| suivi de |cmd|la clé de " \
            "l'objet à ajouter sur ce membre|ff|.\n" \
            "Exemple : |cmd|main gauche sarbacane_bambou|ff|\n" \
            "Pour supprimer un membre, entrez |cmd|0|ff| comme clé de " \
            "l'objet.\nExemple : |cmd|main gauche 0|ff|\n\n"
        
        # Niveau
        niveau = self.ajouter_choix("niveau", "ni", Entier, prototype,
                "niveau", 0)
        niveau.parent = self
        niveau.apercu = "{objet.niveau}"
        niveau.prompt = "Entrez un niveau : "
        niveau.aide_courte = \
            "Entrez le niveau du PNJ.\n\nNiveau actuel : {objet.niveau}"
        
        # XP
        xp = self.ajouter_choix("xP", "x", Flottant, prototype,
                "gain_xp")
        xp.parent = self
        xp.apercu = "{objet.gain_xp}%"
        xp.prompt = "Entrez le pourcentage d'XP reçue par l'adversaire : "
        xp.aide_courte = \
            "Entrez le pourcentage d'XP relative gagnée par l'adversaire lors " \
            "de la mort du\nPNJ.\n\n" \
            "Pourcentage actuel : {objet.gain_xp}%"
        
        # Script
        scripts = self.ajouter_choix("scripts", "sc", EdtScript,
                prototype.script)
        scripts.parent = self

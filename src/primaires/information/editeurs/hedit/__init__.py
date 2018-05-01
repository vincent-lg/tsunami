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


"""Package contenant l'éditeur 'hedit'.
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
from .edt_resume import EdtResume
from .edt_mots_cles import EdtMotscles
from .edt_lies import EdtLies
from .edt_fils import EdtFils
from .supprimer import NSupprimer

class EdtHedit(Presentation):
    
    """Classe définissant l'éditeur de sujet d'aide hedit.
    
    """
    
    nom = "hedit"
    
    def __init__(self, personnage, sujet):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None
        
        Presentation.__init__(self, instance_connexion, sujet)
        if personnage and sujet:
            self.construire(sujet)
    
    def __getnewargs__(self):
        return (None, None)
    
    def construire(self, sujet):
        """Construction de l'éditeur"""
        # Titre
        titre = self.ajouter_choix("titre", "t", Uniligne, sujet, "titre")
        titre.parent = self
        titre.prompt = "Titre du sujet : "
        titre.apercu = "{objet.titre}"
        titre.aide_courte = \
            "Entrez le |ent|titre|ff| du sujet d'aide ou |cmd|/|ff| pour " \
            "revenir à la fenêtre parente.\n\nTitre actuel : " \
            "|bc|{objet.titre}|ff|"
        
        # Contenu
        contenu = self.ajouter_choix("contenu", "c", Description, \
                sujet, "contenu")
        contenu.parent = self
        contenu.apercu = "{objet.contenu.paragraphes_indentes}"
        contenu.aide_courte = \
            "| |tit|" + "Contenu du sujet d'aide {}".format(sujet).ljust(76) + \
            "|ff||\n" + self.opts.separateur
        
        # Groupe
        str_groupes = sorted(
                type(self).importeur.interpreteur.groupes.nom_groupes)
        groupe = self.ajouter_choix("groupe d'utilisateurs", "o", Choix,
                sujet, "str_groupe", str_groupes)
        groupe.parent = self
        groupe.prompt = "Groupe d'utilisateurs du sujet : "
        groupe.apercu = "{objet.str_groupe}"
        groupe.aide_courte = \
            "Entrez le |ent|groupe|ff| pouvant accéder au sujet d'aide ou " \
            "|cmd|/|ff| pour revenir à la\nfenêtre parente.\n" \
            "Groupes disponibles : |ent|" + "|ff|, |ent|".join(
            str_groupes) + "|ff|.\n\n" \
            "Groupe actuel : |bc|{objet.str_groupe}|ff|"
        
        # Mots-clés
        mots_cles = self.ajouter_choix("mots-clés", "m", EdtMotscles, sujet)
        mots_cles.parent = self
        mots_cles.prompt = "Entrez un mot-clé :"
        mots_cles.apercu = "{objet.str_mots_cles}"
        mots_cles.aide_courte = \
            "Entrez un |ent|nouveau mot-clé|ff| pour l'ajouter à la liste, " \
            "un |ent|mot-clé existant|ff| pour\nle supprimer ou |cmd|/|ff| " \
            "pour revenir à la fenêtre précédente.\n" \
            "Mots-clés de ce sujet : |bc|{objet.str_mots_cles}|ff|"
        
        # Sujets liés
        lies = self.ajouter_choix("sujets liés", "l", EdtLies, sujet)
        lies.parent = self
        lies.prompt = "Entrez le nom d'un sujet :"
        lies.aide_courte = \
            "Entrez la |ent|clé|ff| d'un sujet pour l'ajouter à la liste " \
            "des sujets liés ou\nl'en supprimer ; / pour revenir à la " \
            "fenêtre précédente.\n" \
            "Sujets liés à celui-ci : |bc|{objet.str_sujets_lies}|ff|"
        
        
        # Sujets fils
        fils = self.ajouter_choix("sujets fils", "f", EdtFils, sujet)
        fils.parent = self
        fils.aide_courte = \
            "Entrez la |ent|clé|ff| d'un sujet. Si il n'est pas dans la " \
            "liste des sujets liés,\n" \
            "il y sera ajouté, sinon il en sera supprimé.\n" \
            "Options :\n" \
            " - |ent|/u <sujet fils>|ff| : déplace un sujet vers le haut de " \
            "la liste\n" \
            " - |ent|/d <sujet fils>|ff| : déplace le sujet vers le bas\n\n" \
            "{objet.tab_sujets_fils}"
        
        # Suppression
        suppression = self.ajouter_choix("supprimer", "sup", NSupprimer, \
                sujet)
        suppression.parent = self
        suppression.aide_courte = "Souhaitez-vous réellement supprimer " \
                "le sujet d'aide '{}' ?".format(sujet.titre)
        suppression.confirme = "Le sujet d'aide '{}' a bien été " \
                "supprimé.".format(sujet.titre)

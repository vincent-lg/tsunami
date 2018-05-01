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


"""Package contenant l'éditeur 'chedit'.
Si des redéfinitions de contexte-éditeur standard doivent être faites, elles
seront placées dans ce package.

Note importante : ce package contient la définition d'un éditeur, mais
celui-ci peut très bien être étendu par d'autres modules. Au quel cas,
les extensions n'apparaîtront pas ici.

"""

from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.description import Description
from primaires.interpreteur.editeur.uniligne import Uniligne
from .edt_couleur import EdtCouleur
from .edt_flags import EdtFlags

class EdtChedit(Presentation):
    
    """Classe définissant l'éditeur de canal 'chedit'.
    
    """
    
    nom = "chedit"
    
    def __init__(self, personnage, canal):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None
        
        Presentation.__init__(self, instance_connexion, canal)
        if personnage and canal:
            self.construire(canal)
    
    def __getnewargs__(self):
        return (None, None)
    
    def construire(self, canal):
        """Construction de l'éditeur"""
        # Résumé
        resume = self.ajouter_choix("resume", "r", Uniligne, canal, "resume")
        resume.parent = self
        resume.prompt = "Nouveau résumé : "
        resume.apercu = "{objet.resume}"
        resume.aide_courte = \
            "Entrez un |ent|résumé|ff| du canal ou |cmd|/|ff| pour revenir " \
            "à la fenêtre parente.\n" \
            "Le |ent|résumé|ff| est une courte aide à propos du canal, " \
            "affichée par exemple dans la\nliste des canaux.\n" \
            "Résumé actuel : |bc|{objet.resume}|ff|"
        
        # Couleur
        couleur = self.ajouter_choix("couleur", "c", EdtCouleur, canal)
        couleur.parent = self
        couleur.prompt = "Couleur du canal : "
        couleur.apercu = "{objet.clr}{objet.clr_nom}|ff|"
        couleur.aide_courte = \
            "Entrez la |ent|couleur|ff| du canal ou |cmd|/|ff| pour revenir " \
            "à la fenêtre parente.\n"
        
        # Description
        description = self.ajouter_choix("description", "d", Description, canal)
        description.parent = self
        description.apercu = "{objet.description.paragraphes_indentes}"
        description.aide_courte = \
            "| |tit|" + "Description du canal {}".format(canal).ljust(76) + \
            "|ff||\n" + self.opts.separateur
        
        # Flags
        flags = self.ajouter_choix("flags", "f", EdtFlags, canal)
        flags.parent = self
        flags.prompt = "Entrez un flag : "
        flags.aide_courte = \
            "Entrez un |ent|flag|ff| pour changer sa valeur ou |cmd|/|ff| " \
            "pour revenir à la fenêtre parente.\n"

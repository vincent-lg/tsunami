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
# pereIBILITY OF SUCH DAMAGE.


"""Ce fichier définit le contexte-éditeur 'Description'."""

from . import Editeur
from primaires.format.fonctions import *

class Description(Editeur):
    
    """Contexte-éditeur description.
    Ce contexte sert à éditer des descriptions.    
        
    """
    
    nom = "editeur:base:description"
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.opts.echp_sp_cars = False
        self.nom_attribut = "description"
        self.ajouter_option("d", self.opt_supprimer)
        self.ajouter_option("r", self.opt_remplacer)
    
    @property
    def description(self):
        """Retourne la description, attribut de self.objet"""
        return getattr(self.objet, self.nom_attribut)
    
    def get_apercu(self):
        """Aperçu de la description"""
        return self.apercu.format(objet = self.objet.description)
    
    def accueil(self):
        """Retourne l'aide"""
        description = self.description
        
        # Message d'aide
        msg = self.aide_courte.format(objet = self.objet) + "\n"
        msg += "Entrez une |tit|phrase|ff| à ajouter à la description\n" \
                "ou |cmd|/|ff| pour revenir à la fenêtre mère.\n\n" \
                "Symboles :\n" \
                "  |cmd||tab||ff| : symbolise une tabulation\n" \
                "  |cmd||nl||ff| : symbolise un saut de ligne\n\n" \
                "Options :\n" \
                "  |cmd|/d <numéro>/*|ff| : supprime un paragraphe ou " \
                "toute la description\n" \
                "  |cmd|/r <texte 1> / <texte 2>|ff| : remplace " \
                "|tit|texte 1|ff| par |tit|texte 2|ff|\n\n" \
                "Pour ajouter un paragraphe, entrez-le tout simplement.\n\n" \
                "Description existante :\n"
        
        if len(description.paragraphes) > 0:
            no_ligne = 1
            for paragraphe in description.paragraphes:
                paragraphe = description.wrap_paragraphe(paragraphe,
                        aff_sp_cars=True)
                paragraphe = paragraphe.replace("\n", "\n   ")
                msg += "\n{: 2} {}".format(no_ligne, paragraphe)
                no_ligne += 1
        else:
            msg += "  Aucune description"
        
        return msg
    
    def opt_supprimer(self, arguments):
        """Fonction appelé quand on souhaite supprimer un morceau de la
        description
        Les arguments peuvent être :
        *   le signe '*' pour supprimer toute la description        
        *   un nombre pour supprimer le paragraphe n°<nombre>
        
        """
        description = self.description
        if arguments == "*": # on supprime toute la description
            description.vider()
            self.actualiser()
        else:
            # Ce doit être un nombre
            try:
                no = int(arguments) - 1
                assert no >= 0 and no < len(description.paragraphes)
            except ValueError:
                self.pere << "|err|Numéro de ligne invalide.|ff|"
            except AssertionError:
                self.pere << "|err|Numéro de ligne inexistant.|ff|"
            else:
                description.supprimer_paragraphe(no)
                self.actualiser()
    
    def opt_remplacer(self, arguments):
        """Fonction appelé pour remplacer du texte dans la description.
        La syntaxe de remplacement est :
        <texte 1> / <texte à remplacer>
        
        """
        description = self.description
        # On commence par split au niveau du pipe
        try:
            recherche, remplacer_par = arguments.split(" / ")
        except ValueError:
            self.pere << "|err|Syntaxe invalide.|ff|"
        else:
            description.remplacer(recherche, remplacer_par)
            self.actualiser()
    
    def interpreter(self, msg):
        """Interprétation du contexte"""
        description = self.description
        description.ajouter_paragraphe(msg)
        self.actualiser()

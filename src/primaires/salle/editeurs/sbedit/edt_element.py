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


"""Ce fichier définit le contexte-éditeur 'edt_element'."""

from primaires.format.fonctions import supprimer_accents
from primaires.interpreteur.editeur import Editeur

class EdtElement(Editeur):
    
    """Contexte-éditeur d'édition d'un élément."""
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.ajouter_option("t", self.opt_editer_type)
        self.ajouter_option("o", self.opt_editer_objet)
        self.ajouter_option("c", self.opt_connecteur)
        self.ajouter_option("g", self.opt_genre)
        self.ajouter_option("e", self.opt_etat_min)
    
    def accueil(self):
        """Message d'accueil du contexte."""
        element = self.objet
        msg = "| |tit|" + "Edition de l'élément {}".format(element).ljust(76)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += "Options :\n"
        msg += " |cmd|/t <type d'objet à ajouter ou supprimer>|ff|\n"
        msg += " |cmd|/o <objet à ajouter ou supprimer>|ff|\n"
        msg += " |cmd|/c <connecteur>\n"
        msg += " |cmd|/g|ff| pour changer le genre (masculin ou " \
                "féminin)\n"
        msg += " |cmd|/e <état minimum>|ff|\n\n"
        msg += "Types admis : " + element.str_types_admis + "\n"
        msg += "Objets admis : " + element.str_objets_admis + "\n"
        msg += "Connecteur : " + element.connecteur + "\n"
        msg += "Genre : "
        if element.masculin:
            msg += "masculin"
        else:
            msg += "féminin"
        msg += "\n"
        msg += "État minimum : " + str(element.etat_min + 1) + " ("
        try:
            etat = element.prototype.etats[element.etat_min]
        except IndexError:  
            msg += "|rg|inconnu|ff|"
        else:
            msg += etat.nom_singulier
        
        return msg
    
    def opt_editer_type(self, arguments):
        """Ajoute ou retire un type admis.
        
        Syntaxe :
            /t <nom du type>
        
        """
        element = self.objet
        # Cherche le type
        nom = supprimer_accents(arguments).lower()
        if not nom:
            self.pere << "|err|Entrez un nom de type d'objet.|ff|"
            return
        
        for t_type in importeur.objet.types.values():
            if supprimer_accents(t_type.nom_type) == nom:
                element.ajouter_ou_retirer_type_admis(t_type.nom_type)
                self.actualiser()
                return
        
        self.pere << "|err|Type inconnu.|ff|"
    
    def opt_editer_objet(self, arguments):
        """Ajoute ou retire un objet admis.
        
        Syntaxe :
            /n <clé de l'objet></clé>
        
        """
        element = self.objet
        cle = arguments.lower()
        if not cle:
            self.pere << "|err|Entrez une clé de prototype d'objet.|ff|"
            return
        
        try:
            prototype = importeur.objet.prototypes[cle]
        except KeyError:
            self.pere << "|err|Ce prototype est inconnu.|ff|"
        else:
            element.ajouter_ou_retirer_objet_admis(prototype.cle)
            self.actualiser()
    
    def opt_connecteur(self, arguments):
        """Modifie le connecteur.
        
        Syntaxe :
            /c <connecteur>
        
        """
        element = self.objet
        element.connecteur = arguments.lower()
        self.actualiser()
    
    def opt_genre(self, arguments):
        """Change le genre de l'élément.
        
        Syntaxe :
            /g
        
        """
        element = self.objet
        element.masculin = not element.masculin
        self.actualiser()
    
    def opt_etat_min(self, arguments):
        """Change l'état minimum de l'élément.
        
        Syntaxe :
            /e <état minimum>
        
        """
        element = self.objet
        try:
            nb = int(arguments)
            assert nb > 0 and nb <= len(element.prototype.etats)
        except (ValueError, AssertionError):
            self.pere << "|err|Nombre invalide.|ff|"
        else:
            element.etat_min = nb - 1
            self.actualiser()

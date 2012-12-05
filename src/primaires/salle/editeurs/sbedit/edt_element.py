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
    
    def accueil(self):
        """Message d'accueil du contexte."""
        element = self.objet
        msg = "| |tit|" + "Edition de l'élément {}".format(element).ljust(76)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += "Options :\n"
        msg += " |cmd|/t <type d'objet à ajouter ou supprimer>|ff|\n"
        msg += " |cmd|/o <objet à ajouter ou supprimer>|ff|\n\n"
        msg += "Types admis : " + element.str_types_admis + "\n"
        msg += "Objets admis : " + element.str_objets_admis
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


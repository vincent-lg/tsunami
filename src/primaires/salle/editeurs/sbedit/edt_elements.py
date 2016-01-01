# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 LE GOFF Vincent
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


"""Ce fichier définit le contexte-éditeur 'edt_elements'."""

from primaires.interpreteur.editeur import Editeur
from primaires.interpreteur.editeur.env_objet import EnveloppeObjet
from .edt_element import EdtElement

class EdtElements(Editeur):
    
    """Contexte-éditeur d'édition des éléments."""
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.ajouter_option("n", self.opt_creer_element)
        self.ajouter_option("d", self.opt_supprimer_element)
    
    def accueil(self):
        """Message d'accueil du contexte"""
        prototype = self.objet
        msg = "| |tit|" + "Edition des éléments de {}".format(
                prototype).ljust(76)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += "Options :\n"
        msg += " |cmd|/n <nom singulier de l'élément à créer>|ff|\n"
        msg += " |cmd|/d <nom de l'élément à supprimer>|ff|\n\n"
        msg += "Éléments actuels :\n"
        
        # Parcours des éléments
        for nom, element in prototype.elements.items():
            msg += "\n  " + nom
        
        if not prototype.elements:
            msg += "\n  Aucun élément pour l'instant"
        
        return msg
    
    def opt_creer_element(self, arguments):
        """Crée un nouvel élément.
        
        Syntaxe:
            /n <nouveau nom d'emplacement>
        
        """
        prototype = self.objet
        element = prototype.get_element(arguments)
        if element is not None:
            self.pere << "|err|Ce nom d'élément existe déjà.|ff|"
            return
        
        prototype.ajouter_element(arguments)
        self.actualiser()
        
    def opt_supprimer_element(self, arguments):
        """Supprime un élément.
        
        Syntaxe :
            /d <nom de l'élément>
        
        """
        prototype = self.objet
        element = prototype.get_element(arguments)
        if element is None:
            self.pere << "|err|Cet élément est introuvable.|ff|"
            return
        
        prototype.supprimer_element(element.nom)
        self.actualiser()
    
    def interpreter(self, msg):
        """Interprélémention de l'éditeur."""
        prototype = self.objet
        element = prototype.get_element(msg)
        if element is None:
            self.pere << "|err|Cet élément est introuvable.|ff|"
            return
        
        enveloppe = EnveloppeObjet(EdtElement, element, None)
        enveloppe.parent = self
        contexte = enveloppe.construire(self.pere)
        self.migrer_contexte(contexte)

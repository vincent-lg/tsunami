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


"""Package contenant la commande 'eltedit'."""

from primaires.interpreteur.commande.commande import Commande
from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.uniligne import Uniligne
from secondaires.navigation.editeurs.eltedit.presentation import EdtPresentation
from primaires.interpreteur.editeur.env_objet import EnveloppeObjet

class CmdEltedit(Commande):
    
    """Commande 'eltedit'"""
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "eltedit", "eltedit")
        self.groupe = "administrateur"
        self.schema = "<ident>"
        self.nom_categorie = "batisseur"
        self.aide_courte = "ouvre l'éditeur d'élément"
        self.aide_longue = \
            "Cette commande permet d'accéder à l'éditeur d'éléments. Elle " \
            "prend en paramètre l'identifiant de l'élément (que des " \
            "minuscules, des chiffres et le signe |ent|_|ff|). Si l'élément " \
            "n'existe pas, il est créé."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        ident = dic_masques["ident"].ident
        if ident in type(self).importeur.navigation.elements:
            element = type(self).importeur.navigation.elements[ident]
            enveloppe = EnveloppeObjet(EdtPresentation, element, "")
            contexte = enveloppe.construire(personnage)
            
            personnage.contextes.ajouter(contexte)
            contexte.actualiser()
        else:
            editeur = type(self).importeur.interpreteur.construire_editeur(
                    "eltedit", personnage, ident)
            personnage.contextes.ajouter(editeur)
            editeur.actualiser()

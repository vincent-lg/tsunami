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


"""Package contenant la commande 'pedit'."""

from primaires.interpreteur.commande.commande import Commande

class CmdPedit(Commande):
    
    """Commande 'pedit'"""
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "pedit", "pedit")
        self.groupe = "administrateur"
        self.schema = "<ident>"
        self.nom_categorie = "batisseur"
        self.aide_courte = "ouvre l'éditeur de PNJ"
        self.aide_longue = \
            "Cette commande ouvre l'éditeur de PNJ permettant de créer et " \
            "éditer des prototypes de PNJ. Notez bien que vous n'éditez " \
            "pas directement le PNJ mais bien son prototype."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        ident_pnj = dic_masques["ident"].ident
        if ident_pnj in type(self).importeur.pnj.prototypes:
            prototype = type(self).importeur.pnj.prototypes[ident_pnj]
        else:
            prototype = type(self).importeur.pnj.creer_prototype(ident_pnj)
        
        editeur = type(self).importeur.interpreteur.construire_editeur(
                "pedit", personnage, prototype)
        personnage.contextes.ajouter(editeur)
        editeur.actualiser()

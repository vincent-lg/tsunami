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
# pereIBILITY OF SUCH DAMAGE.


"""Ce fichier définit le contexte-éditeur 'EdtContenu'."""

from primaires.interpreteur.editeur.description import Description
from primaires.format.fonctions import *

class EdtContenu(Description):
    
    """Contexte-éditeur EdtContenu.
    Ce contexte sert à éditer le contenu d'un message.
        
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Description.__init__(self, pere, objet, attribut)
        self.nom_attribut = "contenu"
    
    def accueil(self):
        """Retourne l'aide"""
        description = self.description
        
        # Message d'aide
        msg = self.aide_courte.format(objet = self.objet) + "\n"
        msg += "Entrez une |cmd|phrase|ff| à ajouter au corps du message " \
                "ou |ent|/|ff| pour revenir à la\nfenêtre mère.\n" \
                "Symboles :\n" \
                " - |ent||tab||ff| : symbolise une tabulation\n" \
                " - |ent||nl||ff| : symbolise un saut de ligne\n" \
                "Options :\n" \
                " - |ent|/d <numéro>/*|ff| : supprime un paragraphe ou " \
                "tout le contenu\n" \
                " - |ent|/r <texte 1> / <texte 2>|ff| : remplace " \
                "|cmd|texte 1|ff| par |cmd|texte 2|ff|\n" \
                "Pour ajouter un paragraphe, entrez-le tout simplement.\n\n" \
                "Contenu existant :\n"
        
        if len(description.paragraphes) > 0:
            no_ligne = 1
            for paragraphe in description.paragraphes:
                paragraphe = description.wrap_paragraphe(paragraphe,
                        aff_sp_cars=True)
                paragraphe = paragraphe.replace("\n", "\n   ")
                msg += "\n{: 2} {}".format(no_ligne, paragraphe)
                no_ligne += 1
        else:
            msg += "\n Aucun contenu."
        
        return msg

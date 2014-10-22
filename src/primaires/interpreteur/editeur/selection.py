# -*-coding:Utf-8 -*

# Copyright (c) 2010 DAVY Guillaume
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


"""Ce fichier définit le contexte-éditeur 'Selection'."""

from . import Editeur
from primaires.format.dictionnaires import DictSansAccent
from primaires.format.fonctions import supprimer_accents

class Selection(Editeur):
    
    """Contexte-éditeur selection.
    
    Ce contexte permet de faire sélectionner à l'utilisateur 0, 1, N ou tous
    les éléments d'une liste.
    
    """
    
    nom = "editeur:base:selection"
    
    def __init__(self, pere, objet=None, attribut=None, liste=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.liste = liste or []
    
    def accueil(self):
        """Retourne l'aide courte"""
        return self.aide_courte.format(objet = self.objet)
    
    def interpreter(self, msg):
        """Interprétation du contexte"""
        msg = supprimer_accents(msg).lower()
        if msg == "*":
            setattr(self.objet, self.attribut, ["*"])
        else:
            # On constitue un dictionnaire des données sélectionnées
            # En clé, c'est le nom de la donnée
            # En valeur, True si la clé a été sélectionné, False sinon
            selectionne = DictSansAccent((nom, False) for nom in self.liste)
            for nom in getattr(self.objet, self.attribut):
                if nom in selectionne.keys():
                    selectionne[nom] = True
            
            if msg in selectionne.cles_sa():
                selectionne[msg] = not selectionne[msg]
            else:
                self.pere << "|err|L'option {} est invalide.|ff|".format(msg)
                return
            
            selectionne = [nom for nom, val in selectionne.items() if val]
            setattr(self.objet, self.attribut, selectionne)
        
        self.actualiser()

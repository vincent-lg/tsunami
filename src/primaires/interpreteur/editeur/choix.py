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


"""Ce fichier définit le contexte-éditeur 'Choix'."""

from . import Editeur
from primaires.format.fonctions import *

class Choix(Editeur):
    
    """Contexte-éditeur choix.
    
    Ce contexte permet de faire choisir l'utilisateur une option
    parmis une liste prédéfinie à l'avance
    
    """
    
    nom = "editeur:base:choix"
    
    def __init__(self, pere, objet=None, attribut=None, liste=None):
        """Constructeur de l'éditeur."""
        Editeur.__init__(self, pere, objet, attribut)
        self.liste = liste or []
    
    @property
    def str_liste(self):
        """Retourne une chaîne représentant la liste."""
        liste = self.liste
        if not liste:
            return ""
        
        liste = [str(e) for e in liste]
        return ", ".join(liste)
    
    def accueil(self):
        """Retourne l'aide courte"""
        return self.aide_courte.format(objet=self.objet, liste=self.str_liste)
    
    def interpreter(self, msg):
        """Interprétation du contexte"""
        liste = self.liste
        liste = [supprimer_accents(e).lower() for e in self.liste]
        msg = supprimer_accents(msg).lower()
        if msg in liste:
            indice = liste.index(msg)
            setattr(self.objet, self.attribut, self.liste[indice])
            self.actualiser()
        else:
            self.pere << "|err|Ce choix n'est pas valide.|ff|"

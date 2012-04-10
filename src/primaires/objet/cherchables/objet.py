# -*-coding:Utf-8 -*

# Copyright (c) 2012 NOEL-BARON Léo
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


"""Ce fichier définit la classe Cherchable, classe abstraite de base
pour les objets de recherche (voir plus bas).

"""

from primaires.recherche.cherchables.cherchable import Cherchable

class CherchableObjet(Cherchable):
    
    """Classe cherchable pour les objets de l'univers.
    
    """
    
    nom_cherchable = "objet"
    
    def init(self):
        """Méthode d'initialisation.
        
        C'est ici que l'on ajoute réellement les filtres, avec la méthode
        dédiée.
        
        """
        self.ajouter_filtre("n", "nom", "nom_singulier", "str")
        self.ajouter_filtre("c", "cle", "cle", "str")
        self.ajouter_filtre("i", "ident", "identifiant", "str")
    
    @property
    def items(self):
        """Renvoie la liste des objets traités"""
        return list(importeur.objet.objets.values())
    
    def afficher(self, objet):
        """Méthode d'affichage des objets traités"""
        return objet.identifiant + " : " + objet.nom_singulier

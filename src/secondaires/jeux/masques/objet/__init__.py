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
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant le masque <objet_salle>."""

from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation
from primaires.format.fonctions import contient, supprimer_accents

class ObjetJeu(Masque):
    
    """Masque <objet_salle>.
    On attend le fragment d'un objet d'une salle
    
    """
    
    nom = "objet_jeu"
    
    def __init__(self):
        """Constructeur du masque"""
        Masque.__init__(self)
        self.nom_complet = "Un objet jeu"
        self.element = ""
    
    def valider(self, personnage, dic_masques, commande):
        """Validation du masque"""
        lstrip(commande)
        nom = liste_vers_chaine(commande)
        
        if not nom:
            raise ErreurValidation( \
                "Précisez un élément observable.")
        
        nom = nom.split(" ")[0]
        commande[:] = commande[len(nom):]
        
        salle = personnage.salle
        elt = None
        
        # On cherche dans les objets
        for objet in salle.objets_sol:
            nom_objet = objet.nom_singulier
            if contient(nom_objet, nom):
                elt = objet
        
        if elt is None:
            raise ErreurValidation(
                "Il n'y a rien qui ressemble à cela par ici...")
        
        if elt.nom_type != "jeu":
            raise ErreurValidation("Vous ne pouvez pas jouer à cela...")
        
        self.element = elt
        return True

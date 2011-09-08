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


"""Fichier contenant le masque <nom_joueur>."""

from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation

class Joueur(Masque):
    
    """Masque <nom_joueur>.
    On attend un nom de joueur en paramètre.
    
    """
    
    nom = "nom_joueur"
    nom_complet = "nom d'un joueur"
    
    def init(self):
        """Initialisation des attributs"""
        self.joueur = None
    
    def repartir(self, personnage, masques, commande):
        """Répartition du masque."""
        lstrip(commande)
        nom_joueur = liste_vers_chaine(commande).lower()
        if not nom_joueur:
            raise ErreurValidation(
                "Précisez un nom de joueur.")
        
        nom_joueur = nom_joueur.split(" ")[0].lower()
        commande[:] = commande[len(nom_joueur):]
        print("reste", commande)
        masques.append(self)
        self.a_interpreter = nom_joueur
        return True

    def valider(self, personnage, dic_masques):
        """Validation du masque"""
        Masque.valider(self, personnage, dic_masques)
        nom_joueur = self.a_interpreter
        
        # On cherche dans les joueurs du module connex
        joueur = None
        joueurs = type(self).importeur.connex.joueurs
        for t_joueur in joueurs:
            nom = t_joueur.nom.lower()
            if nom == nom_joueur:
                joueur = t_joueur
                break
        
        if not joueur:
            raise ErreurValidation(
                "|err|Le joueur passé en paramètre n'a pu être trouvé.|ff|")
        
        self.joueur = joueur
        
        return True

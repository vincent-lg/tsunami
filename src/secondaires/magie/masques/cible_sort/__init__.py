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


"""Fichier contenant le masque <cible_sort>."""

from primaires.format.fonctions import contient
from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation

class CibleSort(Masque):
    
    """Masque <cible_sort>.
    On attend une cible de sort en paramètre.
    
    """
    
    nom = "cible_sort"
    nom_complet = "cible"
    
    def init(self):
        """Initialisation des attributs"""
        self.cibles = None
    
    @property
    def cible(self):
        """Retourne la première cible."""
        return self.cibles[0]
    
    def repartir(self, personnage, masques, commande):
        """Répartition du masque.
        
        Le masque <cible_sort> prend tout le message.
        
        """
        cible_sort = liste_vers_chaine(commande).lstrip()
        self.a_interpreter = cible_sort
        commande[:] = []
        if not cible_sort:
            raise ErreurValidation(
                "Précisez une cible.")
        
        masques.append(self)
        return True
    
    def valider(self, personnage, dic_masques):
        """Validation du masque"""
        Masque.valider(self, personnage, dic_masques)
        nom_cible = self.a_interpreter
        persos = personnage.salle.personnages
        objets = []
        cibles = []
        for o in personnage.salle.objets_sol:
            objets.append(o)
        for o in personnage.equipement.tenus:
            objets.append(o)
        
        for p in persos:
            if p is not personnage and contient(
                    p.get_nom_pour(personnage), nom_cible):
                cibles.append(p)
        for o in objets:
            if contient(o.nom_singulier, nom_cible):
                cibles.append(o)
        
        if not cibles:
            raise ErreurValidation("|err|Cette cible est introuvable.|ff|")
        
        self.cibles = cibles
        return True

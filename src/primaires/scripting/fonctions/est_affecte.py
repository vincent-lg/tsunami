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


"""Fichier contenant la fonction est_affecte."""

from primaires.scripting.fonction import Fonction

class ClasseFonction(Fonction):
    
    """Retourne vrai si le personnage ou la salle est affecté(e)."""
    
    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.est_affecte_personnage, "Personnage", "str")
        cls.ajouter_types(cls.est_affecte_salle, "Salle", "str")
    
    @staticmethod
    def est_affecte_personnage(personnage, affection):
        """Retourne vrai si le personnage est affecté par l'affection.
        
        Cette fonction prend en paramètre le personnage à tester et la clé
        de l'affection.
        
        Exemple : si est_affecte(personnage, "alcool"):
        
        """
        cle = affection.lower()
        return cle in personnage.affections
    
    @staticmethod
    def est_affecte_salle(salle, affection):
        """Retourne vrai si la salle est affectée par l'affection.
        
        Cette fonction prend en paramètre la salle à tester et la clé
        de l'affection.
        
        Exemple : si est_affecte(salle, "neige"):
        
        """
        cle = affection.lower()
        return cle in salle.affections

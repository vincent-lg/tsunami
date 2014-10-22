# -*-coding:Utf-8 -*

# Copyright (c) 2012 AYDIN Ali-Kémal
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

"""Fichier contenant le masque <date>"""

from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation
        
class Date(Masque):

    """Masque <date>"""
    
    nom = "date"
    nom_complet = "date"
    
    def init(self):
        """Initialisation des attributs"""
        self.jour = -1
        self.mois = -1
        self.annee = -1
    
    def repartir(self, personnage, masques, commande):
        """Répartition du masque"""
        lstrip(commande)
        if not commande:
            raise ErreurValidation("Entrez une date au format JJ-MM-AAAA")
        
        str_commande = liste_vers_chaine(commande).split(" ")[0]
        try:
            jour, mois, annee = str_commande.split("-")
        except ValueError:
            raise ErreurValidation("syntaxe invalide", True)
        
        try:
            jour = int(jour)
            assert 0 < jour <= 31
        except (ValueError, AssertionError):
            raise ErreurValidation("Jour invalide", True)
        try:
            mois = int(mois)
            assert 0 < mois <= 12
        except (ValueError, AssertionError):
            raise ErreurValidation("Mois invalide", True)
        try:
            annee = int(annee)
            assert 0 < annee
        except ValueError:
            raise ErreurValidation("Année invalide", True)
        
        self.jour = jour
        self.mois = mois
        self.annee = annee
        commande[:] = commande[len(str_commande) + 1:]
        masques.append(self)
        return True

# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
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


"""Fichier contenant le masque <coordonnees>."""

import re

from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation

# Constantes
RE_COORDS = re.compile(r"^-?[0-9]+\.-?[0-9]+\.-?[0-9]+$")

class Coordonnees(Masque):
    
    """Masque <coordonnees>.
    
    On attend des coordonnées en paramètre
    sous la forme x.y.z
    
    """
    
    nom = "coordonnees"
    nom_complet = "coordonnées"
    
    def init(self):
        """Initialisation des attributs"""
        self.coordonnees = (None, None, None)
    
    def repartir(self, personnage, masques, commande):
        """Répartition du masque."""
        str_coordonnees = liste_vers_chaine(commande).lstrip()
        str_coordonnees = str_coordonnees.split(" ")[0]
        
        if not str_coordonnees:
            raise ErreurValidation(
                "Précisez des coordonnées.", False)
        
        if not RE_COORDS.search(str_coordonnees):
            raise ErreurValidation(
                "Ceci ne sont pas des coordonnées valides.", False)
        
        self.a_interpreter = str_coordonnees
        commande[:] = commande[len(str_coordonnees):]
        masques.append(self)
        return True
    
    def valider(self, personnage, dic_masques):
        """Validation du masque"""
        Masque.valider(self, personnage, dic_masques)
        coordonnees = self.a_interpreter
        coordonnees = tuple(int(e) for e in coordonnees.split("."))
        self.coordonnees = coordonnees
        return True

# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Fichier contenant le masque <végétal>."""

import re

from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation
from primaires.format.fonctions import contient, supprimer_accents

# Constantes
RE_NB = re.compile(r"^([0-9]+)\.")

class Vegetal(Masque):
    
    """Masque <végétal>.
    
    On attend le fragment d'un nom de végétal en paramètre.
    
    """
    
    nom = "vegetal"
    nom_complet = "nom d'un végétal"
    
    def init(self):
        """Initialisation des attributs"""
        self.vegetal = None
        self.nombre = 1
    
    def repartir(self, personnage, masques, commande):
        """Répartition du masque."""
        lstrip(commande)
        nom = liste_vers_chaine(commande)
        
        re_nb = RE_NB.search(nom)
        if re_nb:
            nb = re_nb.groups()[0]
            nom = nom[len(nb) + 1:]
            try:
                nb = int(nb)
                assert nb > 0
            except (ValueError, AssertionError):
                raise ErreurValidation( \
                    "Ce nombre est invalide.", False)
            else:
                self.nombre = nb
        
        if not nom:
            raise ErreurValidation( \
                "Précisez un nom de végétal.", False)
        
        commande[:] = []
        self.a_interpreter = nom
        masques.append(self)
        return True
    
    def valider(self, personnage, dic_masques):
        """Validation du masque"""
        Masque.valider(self, personnage, dic_masques)
        nom = self.a_interpreter
        nombre = self.nombre
        nb = 0
        
        salle = personnage.salle
        vegetal = None
        
        for plante in importeur.botanique.salles.get(salle, []):
            if contient(plante.nom, nom):
                nb += 1
                if nb == nombre:
                    vegetal = plante
                    break
        
        if vegetal is None:
            raise ErreurValidation(
                "Vous ne voyez pas ce végétal ici.", True)
        
        self.vegetal = vegetal
        return True

# -*-coding:Utf-8 -*

# Copyright (c) 2011 LE GOFF Vincent
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


"""Fichier contenant le masque <personnage>."""

from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation
from primaires.format.fonctions import contient

class Personnage(Masque):
    
    """Masque <personnage>.
    On attend un personnage présent en paramètre.
    
    """
    
    nom = "personnage_present"
    nom_complet = "personnage présent"
    
    def init(self):
        """Initialisation des attributs"""
        self.personnage = None
    
    def repartir(self, personnage, masques, commande):
        """Répartition du masque.
        
        Le masque <personnage> prend toute la commande.
        
        """
        chn_personnage = liste_vers_chaine(commande).lstrip()
        self.a_interpreter = chn_personnage
        commande[:] = []
        if not chn_personnage:
            raise ErreurValidation(
                "Entrez un nom ou fragment de nom d'un personnage présent.")
        
        masques.append(self)
        return True
    
    def valider(self, personnage, dic_masques):
        """Validation du masque"""
        Masque.valider(self, personnage, dic_masques)
        nom_personnage = self.a_interpreter
        for p in personnage.salle.personnages:
            if p is not personnage and contient(p.get_nom_pour(personnage),
                    nom_personnage):
                self.personnage = p
                break
        
        if self.personnage is None:
            raise ErreurValidation(
                "Le personnage '{}' est introuvable.".format(nom_personnage))
        
        return True

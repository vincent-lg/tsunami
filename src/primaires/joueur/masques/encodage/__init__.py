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


"""Fichier contenant le masque <nom_encodage>."""

from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation
from reseau.connexions.client_connecte import ENCODAGES

class Encodage(Masque):
    
    """Masque <nom_encodage>.
    On attend un nom d'encodage en paramètre.
    
    """
    
    nom = "nom_encodage"
    nom_complet = "encodage disponible"
    
    def init(self):
        """Initialisation des attributs"""
        self.encodage = ""
    
    def repartir(self, personnage, masques, commande):
        """Répartition du masque."""
        encodage = liste_vers_chaine(commande)
        
        if not encodage:
            raise ErreurValidation( \
                "Précisez un encodage disponible.")
        
        encodage = encodage.split(" ")[0].lower()
        self.a_interpreter = encodage
        commande[:] = commande[len(encodage):]
        masques.append(self)
        return True
    
    def valider(self, personnage, dic_masques):
        """Validation du masque"""
        Masque.valider(self, personnage, dic_masques)
        encodage = self.a_interpreter

        encodages = ["aucun"] + ENCODAGES
        msg_enc = "\n\nEncodages disponibles : |ent|" + "|ff|, |ent|".join(
            encodages) + "."
        if not encodage in encodages:
            raise ErreurValidation(
                "|err|L'encodage précisé n'est pas disponible.|ff|" + msg_enc)
        
        self.encodage = encodage
        
        return True

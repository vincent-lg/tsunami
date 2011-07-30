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


"""Fichier contenant le masque <nom_stat>."""

from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation

class NomStat(Masque):
    
    """Masque <nom_stat>.
    On attend un nom de stat en paramètre.
    
    """
    
    nom = "nom_stat"
    nom_complet = "nom d'une stat"
    
    def init(self):
        """Initialisation des attributs"""
        self.nom_stat = None
    
    def valider(self, personnage, dic_masques, commande):
        """Validation du masque"""
        Masque.valider(self, personnage, dic_masques, commande)
        nom_stat = liste_vers_chaine(commande).lstrip()
        nom_stat = nom_stat.split(" ")[0]
        
        if not nom_stat:
            raise ErreurValidation( \
                "De quelle stat parlez-vous ?")
        
        # nom_stat ne peut commencer par un signe souligné
        if nom_stat.startswith("_"):
            raise ErreurValidation( \
                "Cette stat n'existe pas.")
        
        # On se base sur les stats du personnage appelant
        try:
            stat = getattr(personnage.stats, "_{}".format(nom_stat))
        except AttributeError:
            raise ErreurValidation( \
                "Cette stat n'existe pas.")
        else:
            self.nom_stat = stat.nom
        
        commande[:] = commande[len(nom_stat) + 1:]
        return True

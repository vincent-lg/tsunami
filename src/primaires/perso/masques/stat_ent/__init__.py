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


"""Fichier contenant le masque <stat_ent>."""

from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.fonctions import *
from primaires.format.fonctions import supprimer_accents
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation

class StatEnt(Masque):
    
    """Masque <stat_ent>.
    
    On attend un nom de stat entraînable en paramètre.
    
    """
    
    nom = "stat_ent"
    nom_complet = "stat à entraîner"
    
    def init(self):
        """Initialisation des attributs"""
        self.stat = None
    
    def repartir(self, personnage, masques, commande):
        """Répartition du masque."""
        stat_ent = liste_vers_chaine(commande).lstrip()
        
        if not stat_ent:
            raise ErreurValidation( \
                "De quelle stat parlez-vous ?")
        
        self.a_interpreter = stat_ent
        masques.append(self)
        commande[:] = []
        return True
    
    def valider(self, personnage, dic_masques):
        """Validation du masque"""
        Masque.valider(self, personnage, dic_masques)
        stat_ent = supprimer_accents(self.a_interpreter).lower()
        if not stat_ent in importeur.perso.cfg_stats.entrainables:
            raise ErreurValidation( \
                "Stat inconnue.")
        
        self.stat_ent = stat_ent

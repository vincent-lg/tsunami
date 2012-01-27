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


"""Fichier contenant la classe Chemins, détaillée plus bas."""

from abstraits.obase import BaseObj
from primaires.vehicule.vecteur import Vecteur
from .chemin import Chemin

class Chemins(BaseObj):
    
    """Classe représentant une liste de chemins."""
    
    def __init__(self):
        """Constructeur des chemins."""
        self.chemins = []
    
    def __repr__(self):
        """Affichage des chemins."""
        chemins = [str(c) for c in self.chemins]
        return "<chemins [" + ", ".join(chemins) + "]>"
    
    def get(self, salle):
        """Retourne si trouvée le chemin dont la destination est salle.
        
        Si non trouvé retourne None.
        
        """
        for chemin in self.chemins:
            if chemin.destination is salle:
                return chemin
        
        return None
    
    @classmethod
    def salles_autour(cls, salle, rayon=15):
        """Retourne les chemins autour de salle dans un rayon donné."""
        o_chemins = cls()
        salles = {} # salle: chemin}
        
        # Fonction explorant une salle et retournant ses sorties récursivement
        def get_sorties_rec(salle, rayon=0, max=15, salles=None):
            salles = salles or {}
            chemin = salles.get(salle)
            if chemin:
                sorties = list(chemin.sorties)
            else:
                sorties = []
            for sortie in salle.sorties:
                t_salle = sortie.salle_dest
                n_chemin = Chemin()
                n_chemin.sorties.extend(sorties + [sortie])
                a_chemin = salles.get(t_salle)
                if a_chemin:
                    if a_chemin.longueur > n_chemin.longueur:
                        salles[t_salle] = n_chemin
                else:
                    salles[t_salle] = n_chemin
            
            if rayon < max:
                for sortie in salle.sorties:
                    t_salle = sortie.salle_dest
                    get_sorties_rec(t_salle, rayon + 1, max, salles)
            
            return salles
        
        sorties = get_sorties_rec(salle, max=rayon)
        for salle, chemin in sorties.items():
            # Constitution du chemin
            if chemin.origine is not chemin.destination:
                salles[salle] = chemin
        
        # Enfin, on retourne la liste obtenue
        o_chemins.chemins.extend(list(salles.values()))
        return o_chemins

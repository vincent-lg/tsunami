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


"""Fichier contenant la classe Chemin, détaillée plus bas."""

from abstraits.obase import BaseObj
from primaires.vehicule.vecteur import Vecteur

class Chemin(BaseObj):
    
    """Classe représentant un chemin reliant deux salles.
    
    Le chemin se compose des listes des sorties liant
    chaque salle.
    
    """
    
    def __init__(self):
        """Constructeur du chemin."""
        self.sorties = []
        self._construire()
    
    def __repr__(self):
        """Affichage du chemin."""
        sorties = [sortie.nom for sortie in self.sorties]
        return "De {} vers {} ({})".format(self.origine, self.destination,
                ", ".join(sorties))
    
    def __bool__(self):
        return True
    
    @property
    def longueur(self):
        """Retourne la taille du chemin.
        
        Pour connaître la taille, on parcourt chaque salle et calcul
        la somme des normes des vecteurs obtenus.
        
        """
        vecteurs = []
        for sortie in self.sorties:
            v = Vecteur(*sortie.parent.coords.tuple())
            vecteurs.append(v)
        
        v = Vecteur(*self.sorties[-1].salle_dest.coords.tuple())
        vecteurs.append(v)
        
        # Maintenant qu'on a tous les vecteurs, on cherche la norme séparant
        # chacun
        norme = 0.0
        a_v = None
        for i, v in enumerate(vecteurs):
            if a_v:
                norme += (v - a_v).norme
            a_v = v
        
        return norme
    
    @property
    def origine(self):
        return self.sorties and self.sorties[0].parent or None
    
    @property
    def destination(self):
        return self.sorties and self.sorties[-1].salle_dest or None
    
    @classmethod
    def trouver(cls, origine, destination, chaine=True, rayon=15):
        """Retourne, si trouvé, le chemin trouvé entre origine et destination.
        
        Si le chemin n'est pas trouvé, retourne None.
        
        Le paramètre chaine, à True par défaut, indique si
        la recherche doit se faire par sorties ou par coordonnées.
        Par défaut (chaine est à True), on recherche une suite
        de sorties menant de origine à destination. Si chaine est
        à False, on va plutôt chercher à trouver la liste des salles
        se trouvant logiquement sur le parcours, sachant que
        cette chaîne peut être incomplète. Par exemple, le chemin
        reliant deux salles situées sur un véhicule différent
        ne pourront pas être chaînées.
        
        """
        if chaine:
            # Algorithme 1 : path finding de salles reliées
            return origine.salles_autour(rayon).get(destination)
        else:
            # Algorithme 2 : recherche de salles sur le parcours
            return
    
    def raccourcir(self):
        """Tente de raccourcir le chemin.
        
        On raccourci un chemin en vérifiant qu'un chemin plus court
        ne peut exister en passant au-dessus d'une salle. Par exemple,
        si le chemin compte trois salles, A, B et C, on vérifie que A
        n'a pas une sortie directe vers C. Et si c'est le cas, on retire
        l'intermédiaire B.
        
        """
        sorties = []
        i = 0
        while i < len(self.sorties):
            sortie = self.sorties[i]
            if (i + 1) < len(self.sorties):
                suivante = self.sorties[i + 1]
            else:
                sorties.append(sortie)
                break
            
            a = sortie.parent
            b = sortie.salle_dest
            c = suivante.salle_dest
            trouve = False
            for t_sortie in a.sorties:
                if t_sortie.salle_dest is c:
                    sorties.append(t_sortie)
                    i += 2
                    trouve = True
                    break
            
            if not trouve:
                sorties.append(sortie)
                i += 1
        
        self.sorties = sorties

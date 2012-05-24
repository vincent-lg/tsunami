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


"""Ce fichier contient la classe Cycle, détaillée plus bas."""

from abstraits.obase import BaseObj
from corps.aleatoire import varier
from primaires.format.fonctions import supprimer_accents
from .periode import Periode

class Cycle(BaseObj):
    
    """Classe décrivant un cycle de vie d'une plante.
    
    Une plante, en fonction de sa longévité, contient plusieurs cycles
    qui marquent sa vie et son âge.
    
    """
    
    def __init__(self, nom, age, plante):
        """Constructeur du cycle."""
        BaseObj.__init__(self)
        self.nom = nom
        self.plante = plante
        self.periodes = []
        self.age = age
        self.duree = 1
        self.variation = 0
        self.visible = True
    
    def __getnewargs__(self):
        return ("", 1, None)
    
    def __repr__(self):
        return "<cycle {} ({}-{} ans>".format(self.nom, self.age, \
                self.age + self.duree)
    
    def __str__(self):
        return self.nom
    
    @property
    def fin(self):
        """Retourne la fin semie aléatoire du cycle."""
        if self.variation > 0:
            return varier(self.age + self.duree, self.variation)
        else:
            return self.age + self.duree
    
    @property
    def cycle_suivant(self):
        """Retourne, si trouve, le cycle suivant.
        
        Si aucun cycle ne vient après, retourne None.
        Si le cycle présent ne peut être trouvé dans la plante, lève une
        exception IndexError.
        
        """
        indice = self.plante.cycles.index(self)
        if indice == -1:
            raise IndexError("cycle introuvable {} dans la plante {}".format(
                    self, self.plante))
        
        try:
            return self.plante.cycles[indice + 1]
        except IndexError:
            return None
    
    def ajouter_periode(self, nom):
        """Ajoute une période et la retourne.
        
        Si la période existe (le nom est déjà pris), lève une exception
        ValueError.
        
        """
        if self.est_periode(nom):
            raise ValueError("la période {} existe déjà".format(nom))
        
        periode = Periode(nom.lower(), self)
        self.periodes.append(periode)
        return periode
    
    def est_periode(self, nom):
        """Retourne True si la période est trouvée, False sinon.
        
        La recherche ne tient pas compte des accents ou majuscules /
        minuscules.
        
        """
        nom = supprimer_accents(nom).lower()
        for periode in self.periodes:
            if supprimer_accents(periode.nom) == nom:
                return True
        
        return False
    
    def get_periode(self, nom):
        """Retourne la période si existe.
        
        Si elle n'existe pas, lève l'exception ValueError.
        
        """
        nom = supprimer_accents(nom).lower()
        for periode in self.periodes:
            if supprimer_accents(periode.nom) == nom:
                return periode
        
        raise ValueError("période {} introuvable".format(nom))
    
    def supprimer_periode(self, nom):
        """Supprime la période donnée.
        
        Si la période n'est pas trouvée, lève l'exception ValueError.
        
        """
        nom = supprimer_accents(nom).lower()
        for periode in list(self.periodes):
            if supprimer_accents(periode.nom) == nom:
                self.periodes.remove(periode)
                periode.detruire()
                return
        
        raise ValueError("période {} introuvable".format(nom))
    
    def detruire(self):
        """Destruction du cycle."""
        for periode in self.periodes:
            periode.detruire()
        
        BaseObj.detruire(self)

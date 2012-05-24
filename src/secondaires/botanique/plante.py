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


"""Ce fichier contient la classe Plante, détaillée plus bas."""

from abstraits.obase import BaseObj
from corps.aleatoire import varier

class Plante(BaseObj):
    
    """Classe représentant une plante ou un végétal quelconque.
    
    À la différence du prototype qui définit des caractéristiques
    globales propres aux végétaux construits dessus, cette classe est
    une plante (une instance par végétal). Si on trouve deux pommiers,
    l'un à Myr et l'autre à Picte, ce seront deux instances différentes.
    
    """
    
    def __init__(self, prototype, salle):
        """Constructeur de la plante."""
        BaseObj.__init__(self)
        self.prototype = prototype
        self.salle = salle
        self.n_id = -1
        self.elements = {}
        self.age = 0
        self.periode = None
        if prototype:
            self.n_id = prototype.n_id
            type(prototype).n_id += 1
            prototype.plantes.append(self)
            self.periode = prototype.cycles[0].periodes[0]
    
    def __getnewargs__(self):
        return (None, None)
    
    def __repr__(self):
        return "<plante {} (âge={})>".format(repr(self.identifiant), self.age)
    
    def __str__(self):
        return self.identifiant
    
    @property
    def cle(self):
        return self.prototype and self.prototype.cle or "inconnue"
    
    @property
    def identifiant(self):
        return self.cle + "_" + str(self.n_id)
    
    @property
    def cycle(self):
        return self.periode and self.periode.cycle or None
    
    @property
    def nom(self):
        """Retourne le nom singulier associée à la période."""
        return self.periode.nom_singulier
    
    def actualiser_elements(self):
        """Actualise les éléments en fonction de la période."""
        periode = self.periode
        n_elements = {}
        for elt in periode.elements:
            qtt = self.elements.get(elt.objet, 0)
            n_qtt = varier(elt.quantite, 3, 0)
            qtt += n_qtt
            if qtt > 0:
                n_elements[elt.objet] = qtt
        
        self.elements.clear()
        self.elements.update(n_elements)
    
    def detruire(self):
        """Destruction de la plante."""
        if self in self.prototype.plantes:
            self.prototype.plantes.remove(self)
        BaseObj.detruire(self)

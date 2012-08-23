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


"""Fichier contenant le type fléchette."""

from corps.aleatoire import *
from .base import BaseType
from .cible import Cible

class Flechette(BaseType):
    
    """Type d'objet: fléchette.
    
    """
    
    nom_type = "fléchette"
    def veut_jeter(self, personnage, sur):
        """Le personnage veut jeter l'objet sur sur."""
        if not hasattr(sur, "prototype") or not isinstance(sur.prototype,
                Cible):
            return ""
        
        return "jeter_cible"
    
    def jeter(self, personnage, elt):
        """Jète la fléchette sur un élément."""
        fact = varier(personnage.agilite, 20) / 100
        fact *= (1 - personnage.poids / personnage.poids_max)
        reussite = chance_sur(fact * 100 + varier(25, 10))
        if reussite:
            personnage << "Vous lancez {} sur {}".format(self.get_nom(), elt)
            personnage.salle.envoyer("{{}} envoie {} sur {}.".format(
                    self.get_nom(), elt), personnage)
        else:
            personnage << "Vous lancez {} mais manquez {}".format(self.get_nom(), elt)
            personnage.salle.envoyer("{{}} envoie {} mais manque {}.".format(
                    self.get_nom(), elt), personnage)
            personnage.salle.objets_sol.ajouter(self)
        
        return reussite
    
    def jeter_cible(self, personnage, cible):
        personnage << "Bien joué !"
        personnage.salle.objets_sol.ajouter(self)

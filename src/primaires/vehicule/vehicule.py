# -*-coding:Utf-8 -*

# Copyright (c) 2010 DAVY Guillaume
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


"""Fichier contenant la classe Vehicule, détaillée plus bas."""

from abstraits.id import ObjetID

from .vecteur import Vecteur
from .force import Propulsion, Frottement

class Vehicule(ObjetID):
    
    """Classe représentant un véhicule
    
    """
    
    def __init__(self):
        """Constructeur du véhicule.    
        Initialise les valeurs et crée deux forces toujours présentes,
        la propulsion qui sert à faire avancer le véhicule ainsi
        que les frottements qui servent à garantir que la vitesse
        ne pourra pas augmenter indéfiniment.
            
        """
        ObjetID.__init__(self)
        self.masse = 1
        self.position = Vecteur(0, 0, 0)
        self.vitesse = Vecteur(0, 0, 0)
        
        self.propulsion = Propulsion()
        self.frottement = Frottement(self,0.7)
        
        self.forces = [self.propulsion, self.frottement]
    
    def __getnewargs__(self):
        return ()
    
    def tourner(self, angle):
        self.propulsion._valeur.tourner_autour_z(angle)
    
    def incliner(self, angle):
        self.propulsion._valeur.incliner(angle)
    
    def avancer(self):
        """Fait avancer le véhicule"""
        # Calcul de la nouvelle position
        self.position += self.vitesse
        
        # Si on a une masse nulle, on ne peut pas continuer
        if self.masse == 0:
            raise ValueError("ce véhicule a une masse nulle")
        
        # On calcule l'accélération à partir des forces
        acceleration = Vecteur(0, 0, 0)
        for force in self.forces:
            acceleration += (1 / self.masse) * force.valeur
        
        # On calcule la nouvelle vitesse à partir de l'accélération
        self.vitesse += acceleration
        
        # On renvoie la nouvelle position
        return self.position
    
    def get_prochaine_coordonnees(self):
        """Retourne les prochaines coordonnées
        après avoir avancé à la vitesse courante.
        
        """
        return self.position + self.vitesse

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
from bases.collections.dict_valeurs_id import DictValeursID

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
        self.direction = Vecteur(1, 0, 0)
        
        self.propulsion = Propulsion()
        self.frottement = Frottement(self,0.7)
        
        self.forces = [self.propulsion, self.frottement]
        
        self.salles = DictValeursID()
        self.en_collision = False
    
    def __getnewargs__(self):
        return ()
    
    def tourner(self, angle):
        self.propulsion._valeur.tourner_autour_z(angle)
    
    def incliner(self, angle):
        self.propulsion._valeur.incliner(angle)
    
    def energie_cinetique(self):
        return self.m * self.vitesse.norme() * self.vitesse.norme()
    
    """
    Fonction qui place le véhicule à sa nouvelle position, celle après qu'il
    se soit écoulé temps seconde virtuelle
    """
    def avancer(self, temps):
        """Fait avancer le véhicule"""
        # Calcul de la nouvelle position
        if not self.en_collision:
            self.position += temps * self.vitesse
        
        # Si on a une masse nulle, on ne peut pas continuer
        if self.masse == 0:
            raise ValueError("ce véhicule a une masse nulle")
        
        # On calcule l'accélération à partir des forces
        self.acceleration = Vecteur(0, 0, 0)
        for force in self.forces:
            self.acceleration += (1 / self.masse) * force.valeur
        
        self.forces = [ force for force in self.forces if not force.desuette]
        
        # On calcule la nouvelle vitesse à partir de l'accélération
        self.vitesse += temps * self.acceleration
        
        d = -self.direction.direction()
        i = self.direction.inclinaison()
        operation = lambda v : self.position + v.tourner_autour_z(d).incliner(i)
        for (vec,salle) in self.salles.items():
            salle.coords = operation(vec.copie()).coordonnees
        
        self.en_collision = False
       
        # On renvoie la nouvelle position
        return self.position
    
    """
    Fonction appelé lorsqu'une collision se produit avec ce véhicule
    """
    
    def collision(self, impacts):
        self.en_collision = True
    
    """
    Fonction qui trouve la prochaine coordonné du véhicule après temps secondes
    virtuelles en supposant la vitesse constante
    """
    def get_prochaine_coordonnees(self, temps):
        """Retourne les prochaines coordonnées
        après avoir avancé à la vitesse courante.
        
        """
        position = self.position + temps * self.vitesse
        resultat = []
        d = -self.direction.direction()
        i = self.direction.inclinaison()
        operation = lambda v : position + v.tourner_autour_z(d).incliner(i)
        for (vec,salle) in self.salles.items():
            resultat += operation(vec.copie()).coordonnees.entier()
        return resultat

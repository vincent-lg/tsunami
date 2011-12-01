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

from .direction import Direction
from .vecteur import Vecteur
from .force import Propulsion, Frottement

class Vehicule(ObjetID):
    
    """Classe représentant un véhicule
    
    Un véhicule est un objet potentiellement enregistrable (hérité d'ObjetID)
    possédant plusieurs attributs et méthodes caractérisant le déplacement
    d'un véhicule d'un type standard en trois dimensions.
    
    Le système de déplacement est géré par des vecteurs  modélisant :
    *   La vitesse
    *   La direction
    *   Les valeurs des forces agissant sur le véhicule
    
    Un véhicule standard possède par défaut deux forces agissant sur lui :
    *   Sa propulsion (force propulsive, absente du modèle abstrait [1])
    *   Son frottement (sans quoi sa vitesse tend vers l'infini).
    
    Ce comportement peut être surchargé dans des classes filles.
    
    Attributs :
        masse -- la masse du véhicule
        position -- la position, représentée par un vecteur (X, Y, Z)
        vitesse -- la vitesse actuelle, là encore sous la forme d'un vecteur [1]
        direction -- la direction du véhicule sous la forme d'un vecteur
        frottement -- sa force de frottement
        forces -- une liste comportant les forces agissant sur le véhicule
        salles -- un dictionnaire des salles constituant le véhicule [2]
    
    [1] La force propulsive n'est pas présente directement dans cette classe.
        En effet, elle est souvent propre au type de véhicule que l'on
        souhaite créer (les navires, par exemple, n'ont pas de force
        propulsive à proprement parlé).
    
    [2] Le vecteur permet de représenter autant une direction ((1, 0, 0)
        représente un vecteur vers l'est par exemple) qu'une force (le
        vecteur (2, 0, 0) est plus long que (1, 0, 0)). Ces vecteurs
        sont donc utilisés pour représenter la direction, la vitesse
        du véhicule, mais aussi la valeur des forces s'appliquant sur lui.
    
    [3] Les salles déclarées dans ce dictionnaire sont celles du véhicule
        (son intérieur, par exemple). Toutes ces salles se déplaceront
        avec le véhicule. Le dictionnaire est sous la forme :
        {coordonnes_relatives: salle_correspondante}
        Les coordonnées relatives sont celles par rapport au centre du véhicule
        et restent donc fixes pour le véhicule. Par contre, les coordonnées
        des salles (salle_correspondante.coords) sont modifiées à chaque
        déplacement du véhicule.
    
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
        self.position = Vecteur(0, 0, 0, self)
        self.vitesse = Vecteur(0, 0, 0, self)
        self.acceleration = Vecteur(0, 0, 0, self)
        self.direction = Direction(self, 1, 0, 0)
        
        self.frottement = Frottement(self,0.7)
        
        self.forces = [self.frottement]
        
        self.salles = DictValeursID(self)
        self.en_collision = False
    
    def __getnewargs__(self):
        return ()
    
    def energie_cinetique(self):
        return self.m * self.vitesse.norme ** 2

    def maj_salles(self):
        d = self.direction.direction
        i = self.direction.inclinaison
        operation = lambda v: self.position + v.tourner_autour_z(d).incliner(i)
        for vec, salle in self.salles.items():
            vec = Vecteur(*vec)
            vec = operation(vec)
            salle.coords.x = int(vec.x)
            salle.coords.y = int(vec.y)
            salle.coords.z = int(vec.z)

    def avancer(self, temps):
        """Fait avancer le véhicule.
        
        Cette fonction place le véhicule à sa nouvelle position, celle après
        qu'il se soit écoulé temps seconde virtuelle.
        
        """
        # Calcul de la nouvelle position
        if not self.en_collision:
            self.position += temps * self.vitesse
        
        # Si on a une masse nulle, on ne peut pas continuer
        if self.masse == 0:
            raise ValueError("ce véhicule a une masse nulle")
        
        # On calcule l'accélération à partir des forces
        self.acceleration = Vecteur(0, 0, 0, self)
        for force in self.forces:
            self.acceleration += (1 / self.masse) * force.valeur
        
        self.forces = [force for force in self.forces if not force.desuette]
        
        # On calcule la nouvelle vitesse à partir de l'accélération
        self.vitesse += temps * self.acceleration
        
        # On modifie les coordonnées des salles
        self.maj_salles()
        
        self.en_collision = False
       
        # On renvoie la nouvelle position
        return self.position
    
    def collision(self, impacts):
        """Fonction appelé lorsqu'une collision se produit avec ce véhicule.
        
        La surcharger pour faire réagir un type de véhicule spécifiquement.
        
        """
        self.en_collision = True
    
    def get_prochaine_coordonnees(self, temps):
        """Retourne les prochaines coordonnées.
        
        Cette fonction trouve les prochaine coordonnées du véhicule après
        temps secondes virtuelles en supposant la vitesse constante.
        
        """
        position = self.position + temps * self.vitesse
        resultat = []
        d = self.direction.direction
        i = self.direction.inclinaison
        operation = lambda v: position + v.tourner_autour_z(d).incliner(i)
        for vec, salle in self.salles.items():
            vec = Vecteur(*vec)
            resultat += operation(vec).coordonnees.entier()
        
        return resultat

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


"""Ce fichier contient la classe Vent, détaillée plus bas."""

from abstraits.obase import BaseObj
from primaires.salle.coordonnees import Coordonnees
from primaires.vehicule.vecteur import Vecteur

# Constantes
INFLUENCE_MAX = 50

class Vent(BaseObj):
    
    """Cette classe décrit un vent influenaçant la navigation.
    
    Attributs définis :
        cle -- la clé du vent
        etendue -- l'étendue dans laquelle il est défini
        position -- la position du vent dans l'étendue (coordonnées absolues)
        vitesse -- la vitesse et la direction du vent [1]
    
    [1] La vitesse étant un vecteur, elle contient également la
        direction. La vitesse du vent est la norme du vecteur. La
        direction, en degré, du vent peut être obtenu par vitesse.direction.
    
    """
    
    enregistrer = True
    def __init__(self, etendue, x, y, z, vitesse=1, direction=0):
        """Constructeur du vent.
        
        Paramètres à préciser :
            etendue est l'étendue d'eau définie
            x, y et z sont les coordonnées de la position du vent
            vitesse est la norme du futur vecteur
            direction est la direction du futur vecteur (un angle en degré).
        
        """
        BaseObj.__init__(self)
        self.cle = "inconnue"
        self.etendue = etendue
        self.x = x
        self.y = y
        self.z = z
        self.vitesse = vitesse * Vecteur(1, 0, 0)
        self.vitesse.parent = self
        self.vitesse.orienter(direction)
        self.longueur = 20
        if etendue:
            self.cle = etendue.cle + "_" + str(
                    len(type(self).importeur.navigation.vents_par_etendue.get(
                    etendue.cle, [])) + 1)
    
    def __getnewargs__(self):
        return (None, 0, 0, 0)
    
    def __repr__(self):
        return "vent {} (étendue={}, x={}, y={}, z={}, vitesse={})".format(
                self.cle, self.etendue, self.x, self.y, self.z, self.vitesse)   
    
    @property
    def coordonnees(self):
        return Coordonnees(self.x, self.y, self.z)
    
    @property
    def position(self):
        """Retourne un vecteur représentant la position du vent."""
        return Vecteur(self.x, self.y, self.z)
    
    def changer_force(self, force):
        """"Change la force du vent.
        
        La force passée en paramètre est la norme de la nouvelle vitesse.
        
        """
        vitesse = self.vitesse
        normalise = vitesse.normalise()
        force = force * normalise
        self.vitesse.x = force.x
        self.vitesse.y = force.y
        self.vitesse.z = force.z

# -*-coding:Utf-8 -*

# Copyright (c) 2011 LE GOFF Vincent
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


"""Fichier contenant la classe Etendue, détaillée plus bas."""

from abstraits.id import ObjetID
from bases.collections.dict_valeurs_id import DictValeursID

from .coordonnees import Coordonnees

class Etendue(ObjetID):
    
    """Cette classe représente une étendue d'eau.
    
    Une étendue d'eau peut être un lac, une rivière, une mer ou un océan.
    A noter, cela est extrêmement important, qu'une étendue ne retient
    pas la position où elle se trouve, seulement ses délimiteurs.
    C'est pourquoi faire une étendue d'eau infinie est une mauvaise idée.
    
    Les étendues d'eaux peuvent être chaînées (une rivière se jète dans
    la mer).
    
    Attributs :
        obstacles -- liste des obstacles (on liste juste les coordonnées 2D)
        cotes -- un dictionnaire des côtes ({coord: salle}) [1]
        liens -- un dictionnaire des liens avec d'autres étendues
                ({coord: etendue})
    
    [1] Les côtes ici sont celles débarcables. Toutes les salles non
        débarcables sont des obstacles.
    
    """
    
    groupe = "etendue"
    sous_rep = "etendues"
    def __init__(self, cle):
        """Création de l'éttendue."""
        ObjetID.__init__(self)
        self.cle = cle
        self.altitude = 0
        self.profondeur = 4
        self.obstacles = []
        self.cotes = DictValeursID(self)
        self.liens = DictValeursID(self)
    
    def __getnewargs__(self):
        return ("", )
    
    def __str__(self):
        return self.cle
    
    def __contains__(self, coordonnees):
        """Retourne True si les coordonnées sont des côtes de l'étendue.
        
        Les coordonnées peuvent être sous la forme d'un tuple ou d'un objet
        Coordonnees.
        
        """
        coordonnees = self.convertir_coordonnees(coordonnees)
        return coordonnees in self.points.keys()
    
    def __getitem__(self, item):
        """Retourne le point correspondant aux coordonnées entrées.
        
        Les coordonnées peuvent être :
            un tuple
            un objet de type Coordonnees
        
        Le retour peut être de type :
            None : c'est un obstacle
            salle : une côte débarcable
            etendue : une étendue voisine
        
        """
        coordoonnees = self.convertir_coordonnees(coordonnees)
        return self.points[coordonnees]
    
    @property
    def points(self):
        """Constitution d'un dictionnaire des points."""
        points = dict.fromkeys(self.obstacles)
        points.update(self.cotes)
        points.update(self.liens)
        return points
    
    @staticmethod
    def convertir_coordonnees(coordonnees):
        """Retourne un tuple des coordonnées en 2D.
        
        Le type des coordonnées peut être :
            Un tuple de N dimensions (N >= 2)
            Un objet de type Coordonnees
        
        """
        if isinstance(coordonnees, tuple):
            # Les tuples sont ramenés à 2 dimensions
            coordonnees = coordonnees[:2]
        elif isinstance(coordonnees, Coordonnees):
            coordonnees = coordonnees.tuple[:2]
        else:
            raise TypeError(
                    "type de coordonnées non traité : {}".format(repr(
                    type(coordonnees))))
        
        return coordonnees
    
    def ajouter_obstacle(self, coordonnees):
        """Ajoute l'obstacle."""
        coordonnees = self.convertir_coordonnees(coordonnees)
        if coordonnees in self.points.keys:
            raise ValueError(
                    "un point de coordonnées {} existe déjà".format(
                    coordonnees))
        
        self.obstacles.append(coordonnees)
    
    def ajouter_cote(self, coordonnees, salle):
        """Ajoute la côte accostable (peut-être une île dans l'étendue)."""
        coordonnees = self.convertir_coordonnees(coordonnees)
        if coordonnees in self.points.keys:
            raise ValueError(
                    "un point de coordonnées {} existe déjà".format(
                    coordonnees))
        
        self.cotes[coordonnees] = salle
    
    def ajouter_lien(self, coordonnees, etendue):
        """Ajoute le lien vers une autre étendue.
        
        Note : un lien lie deux étendues. Par exemple, on peut dire que le
        point (3, 4) est un lien de l'étendue riviere_picte vers
        mer_sans_fin.
        
        """
        coordonnees = self.convertir_coordonnees(coordonnees)
        if coordonnees in self.points.keys:
            raise ValueError(
                    "un point de coordonnées {} existe déjà".format(
                    coordonnees))
        
        self.liens[coordonnees] = etendue


ObjetID.ajouter_groupe(Etendue)

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


"""Fichier contenant la classe Gouvernail, détaillée plus bas."""

from bases.objet.attribut import Attribut
from .base import BaseElement

class Gouvernail(BaseElement):
    
    """Classe représentant un gouvernail.
    
    """
    
    nom_type = "gouvernail"
    
    def __init__(self, cle=""):
        """Constructeur d'un type"""
        BaseElement.__init__(self, cle)
        # Attributs propres aux gouvernails
        self._attributs = {
            "orientation": Attribut(lambda: 0),
            "tenu": Attribut(lambda: None),
        }
    
    @staticmethod
    def get_description_ligne(elt, personnage):
        """Retourne la description en une ligne de l'élément."""
        if elt.orientation == 0:
            orientation = "parfaitement au centre"
        elif elt.orientation < 0:
            orientation = "incliné de {nb}° sur bâbord".format(
                    nb=-elt.orientation)
        else:
            orientation = "incliné de {nb}° sur tribord".format(
                    nb=elt.orientation)
        
        return elt.nom.capitalize() + " est " + orientation + "."
    
    @staticmethod
    def virer_babord(elt, nombre=1):
        """Vire vers bâbord."""
        elt.orientation -= nombre
        if elt.orientation < -5:
            elt.orientation = -5
    
    @staticmethod
    def virer_tribord(elt, nombre=1):
        """Vire vers tribord."""
        elt.orientation += nombre
        if elt.orientation > 5:
            elt.orientation = 5
    
    @staticmethod
    def centrer(elt):
        """Centre le gouvernail."""
        elt.orientation = 0

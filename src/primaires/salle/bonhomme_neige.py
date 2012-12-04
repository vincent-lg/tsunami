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

"""Ce fichier contient différentes classes :

BonhommeNeige -- un bonhomme de neige concret
PrototypeBonhommeNeige -- un prototype de bonhomme de neige
Etat -- un état de prototype

"""

from abstraits.obase import BaseObj
from primaires.format.description import Description
from .decor import *

class BonhommeNeige(Decor):
    
    """Cette classe représente un bonhomme de neige concret.
    
    Les bonhommes de neige sont des décors, ils apparaissent
    dans la description d'une salle et peuvent êre regardés.
    
    """
    
    def __init__(self, prototype, parent=None):
        """Constructeur de la classe"""
        Decor.__init__(self, prototype, parent)
        self.etat = -1
        self._construire()
    
    def __getnewargs__(self):
        return (None, )
    
    def __repr__(self):
        return "<bonhomme de neige {} (état={}) en {}>".format(
                self.cle_prototype, self.etat, self.parent)
    
    def get_nom(self, nombre=1):
        return self.prototype.get_nom(self.etat, nombre)
    
    def get_nom_etat(self, nombre=1):
        return self.prototype.get_nom_etat(self.etat, nombre)
    
    def regarder(self, personnage):
        """Le personnage regarde self."""
        ret = "Vous regardez {} :\n\n".format(self.get_nom())
        ret += self.prototype.get_description(self.etat).regarder(
                personnage, self)
        personnage << ret
        personnage.salle.envoyer("{{}} regarde {}.".format(self.get_nom()),
                personnage)

class PrototypeBonhommeNeige(PrototypeDecor):
    
    """Classe représentant un prototype de bonhomme de neige.
    
    Les informations comme le nom ou la description se trouvent
    dans le prototype. La classe BonhommeNeige (définie au-dessus) est une
    concrétisation du prototype dans une salle.
    
    """
    
    def __init__(self, cle):
        PrototypeDecor.__init__(self, cle)
        del self.nom_singulier
        del self.nom_pluriel
        del self.etat_singulier
        del self.etat_pluriel
        del self.description
        self.etats = [Etat(self)]
    
    def __getnewargs__(self):
        return (None, )
    
    def get_nom(self, etat, nombre):
        """Retourne le nom singulier ou pluriel."""
        if nombre <= 0:
            raise ValueError("le nombre {} est négatif ou nul".format(nombre))
        
        etat = self.etats[etat]
        if nombre == 1:
            return etat.nom_singulier
        else:
            nombre = get_nom_nombre(nombre)
            return nombre + " " + etat.nom_pluriel
    
    def get_nom_etat(self, etat, nombre):
        """Retourne le nom et l'état en fonction du nombre."""
        if nombre <= 0:
            raise ValueError("le nombre {} est négatif ou nul".format(nombre))
        
        etat = self.etats[etat]
        if nombre == 1:
            return self.get_nom(etat, 1) + " " + etat.etat_singulier
        else:
            return self.get_nom(etat, nombre) + " " + etat.etat_pluriel
    
    def get_description(self, etat):
        """Retourne la description correspondante à l'état."""
        return self.etats[etat].description
    
    def ajouter_etat(self, nom_singulier):
        """Ajoute un nouvel état."""
        etat = Etat(self)
        etat.nom_singulier = nom_singulier
        self.etats.append(etat)
        return etat
    
    def supprimer_etat(self, indice):
        """Supprime un état."""
        del self.etats[indice]


class Etat(BaseObj):
    
    """Classe représentant un état possible d'un prototype de bonhomme de neige.
    
    C'est dans cette classe qu'on trouve réellement les
    informations nom_singulier, nom_pluriel, etat_singulier,
    etat_pluriel et description.
    
    """
    
    def __init__(self, prototype):
        BaseObj.__init__(self)
        self.nom_singulier = "un bonhomme de neige"
        self.nom_pluriel = "bonhommes de neige"
        self.etat_singulier = "se tient ici"
        self.etat_pluriel = "se tiennent ici"
        self.description = Description(parent=self, scriptable=False)
        self._construire()
    
    def __getnewargs__(self):
        return (None, )
    
    def __repr__(self):
        return "<état {}>".format(self.nom_singulier)
    
    def __str__(self):
        return self.nom_singulier

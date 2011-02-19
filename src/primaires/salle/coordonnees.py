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


"""Fichier contenant la classe Coordonnees, détaillée plus bas."""

from abstraits.obase import BaseObj

class Coordonnees(BaseObj):
    
    """Cette classe représente les trois coordonnées utiles à la représentation dans l'espace (x, y et z).
    Cette classe peut être utilisée pour générer des coordonnées invalides.
    
    """
    
    def __init__(self, x=0, y=0, z=0, valide=True, parent=None):
        """Constructeur des coordonnées"""
        BaseObj.__init__(self)
        self.x = x
        self.y = y
        self.z = z
        self.valide = valide
        self.parent = parent
    
    def __getinitargs__(self):
        return ()
    
    @property
    def invalide(self):
        """Retourne le contraire de 'valide'"""
        return not self.valide
    
    def __str__(self):
        """Affiche les coordonnées plus proprement"""
        if self.valide:
            res = "C({}, {}, {})".format(self.x, self.y, self.z)
        else:
            res = "C(INVALIDE)"
        
        return res
    
    def __repr__(self):
        """Affichage des coordonnées dans un cas de debug"""
        return "Coords(x={}, y={}, z={}, valide={})".format(self.x, self.y, \
                self.z, self.valide)
    
    def __setattr__(self, attr, val):
        """Enregistre le parent si le parent est précisé"""
        anc_tuple = self.tuple_complet()
        object.__setattr__(self, attr, val)
        if hasattr(self, "parent") and self.parent:
            mod_salle = type(self.parent).importeur.salle
            mod_salle.changer_coordonnees(anc_tuple, self)
            self.parent.enregistrer()
    
    def tuple(self):
        """Retourne le tuple (x, y, z)"""
        if hasattr(self, "x") and hasattr(self, "y") and hasattr(self, "z"):
            return (self.x, self.y, self.z)
        else:
            return ()
    
    def tuple_complet(self):
        """Retourne self.tuple + self.valide"""
        if hasattr(self, "valide"):
            return self.tuple() + (self.valide, )
        else:
            return ()

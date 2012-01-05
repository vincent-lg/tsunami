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


"""Ce fichier contient la classe ConteneurObjet, détaillée plus bas."""

from abstraits.obase import BaseObj
from bases.collections.liste_id import ListeID
from .objet_non_unique import ObjetNonUnique

class ConteneurObjet(BaseObj):
    
    """Conteneur standard d'objet.
    
    Cette classe peut être héritée (le sol d'une salle par exemple est un
    conteneur d'objet hérité) ou utilisée telle qu'elle.
    
    Un objet conteneur contient lui-même d'autres objets.
    Note : le conteneur d'objet utilise deux listes en fonction de
    l'unicité ou nom des objets.
    
    Les objets uniques, la majorité, sont représentés par une instance
    pour chaque objet. Les objets non uniques, comme la monnaie, sont des
    objets représentés par leur prototype et le nombre d'objets présents.
    
    """
    
    _nom = "objet_conteneur"
    _version = 1
    def __init__(self, parent=None):
        """Constructeur du conteneur"""
        BaseObj.__init__(self)
        self._objets = ListeID(parent)
        self._non_uniques = []
        self.parent = parent
    
    def __getnewargs__(self):
        return ()
    
    def __iter__(self):
        """Itérateur"""
        liste = list(self._objets) + list(self._non_uniques)
        return iter(liste)
    
    def __str__(self):
        return str(self._objets) + str(self._non_uniques)
    
    def iter_nombres(self):
        """Parcourt les objets et quantités du conteneur."""
        for objet in self._objets:
            yield (objet, 1)
        for objet in self._non_uniques:
            yield (objet.prototype, objet.nombre)
    
    def ajouter(self, objet, nombre=1):
        """On ajoute l'objet dans le conteneur.
        
        On peut très bien ajouter un prototype si l'objet est dit non unique.
        
        """
        prototype = hasattr(objet, "prototype") and objet.prototype or objet
        if prototype.unique:
            objet.contenu = self
            if objet not in self._objets:
                self._objets.append(objet)
            else:
                raise ValueError("le conteneur {} contient déjà l'objet " \
                        "{}".format(self, objet))
        else:
            # On cherche l'objet non unique correspondant au prototype
            non_unique = None
            for objet in self._non_uniques:
                if objet.prototype == prototype:
                    non_unique = objet
                    break
            
            if non_unique:
                non_unique.nombre += nombre
            else:
                non_unique = ObjetNonUnique(prototype, nombre)
                self._non_uniques.append(non_unique)
        
        if self.parent:
            self.parent.enregistrer()
    
    def retirer(self, objet, nombre=1):
        """On retire l'objet du conteneur"""
        prototype = hasattr(objet, "prototype") and objet.prototype or objet
        if prototype.unique:
            if objet in self._objets:
                self._objets.remove(objet)
            else:
                raise ValueError("le conteneur {} ne contient pas l'objet " \
                        "{}".format(self, objet))
        else:
            non_unique = None
            for objet in self._non_uniques:
                if objet.prototype == prototype:
                    non_unique = objet
                    break
            
            if non_unique:
                non_unique.nombre -= nombre
                self.nettoyer_non_uniques()
            else:
                raise ValueError("le conteneur {} ne contient pas l'objet " \
                        "{}".format(self, objet))
        
        if self.parent:
            self.parent.enregistrer()
    
    def nettoyer_non_uniques(self):
        """Nettoie les objets non uniques présents en quantité négative."""
        self._non_uniques = [o for o in self._non_uniques if o.nombre > 0]
        if self.parent:
            self.parent.enregistrer()

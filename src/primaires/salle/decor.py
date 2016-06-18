# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 LE GOFF Vincent
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

Decor -- un décor concret
PrototypeDecor -- un prototype de décor

"""

from abstraits.obase import *
from corps.fonctions import get_nom_nombre
from primaires.format.description import Description

class Decor(BaseObj):

    """Cette classe représente un décor observable dans une salle.

    Les décors sont proches des détails mais ne sont généralement
    pas propres à une salle. Ils permettent d'ajouter, entre guillemets,
    de la couleur à une ambiance (on peut ainsi faire des guirlandes,
    des couronnes, ainsi de suite). Les décors sont visibles
    directement dans la description d'une salle et peuvent être
    regardés.

    """

    def __init__(self, prototype, parent=None):
        """Constructeur de la classe"""
        BaseObj.__init__(self)
        self.prototype = prototype
        self.parent = parent
        self._construire()

    def __getnewargs__(self):
        return (None, )

    def __repr__(self):
        return "<décoration {} en {}>".format(self.cle_prototype, self.parent)

    @property
    def cle_prototype(self):
        return self.prototype and self.prototype.cle or "aucune"

    @property
    def nom(self):
        return self.get_nom()

    def get_nom(self, nombre=1):
        return self.prototype.get_nom(nombre)

    def get_nom_etat(self, nombre=1):
        return self.prototype.get_nom_etat(nombre)

    def get_nom_pour(self, personnage):
        """Retourne le nom pour le personnage précisé."""
        return self.get_nom()

    def regarder(self, personnage):
        """Le personnage regarde self."""
        ret = "Vous regardez {} :\n\n".format(self.get_nom())
        ret += self.prototype.description.regarder(personnage, self)
        personnage << ret
        personnage.salle.envoyer("{{}} regarde {}.".format(self.get_nom()),
                personnage)

class PrototypeDecor(BaseObj):

    """Classe représentant un prototype de décor.

    Les informations comme le nom ou la description se trouvent
    dans le prototype. La classe Decor (définie au-dessus) est une
    concrétisation du prototype dans une salle.

    """

    enregistrer = True
    def __init__(self, cle):
        BaseObj.__init__(self)
        self.cle = cle
        self.nom_singulier = "une décoration"
        self.nom_pluriel = "décorations"
        self.etat_singulier = "se trouve ici"
        self.etat_pluriel = "se trouvent ici"
        self.description = Description(parent=self, scriptable=False)
        self._construire()

    def __getnewargs__(self):
        return (None, )

    def __str__(self):
        return self.cle

    def _get_nom(self):
        return self.nom_singulier
    def _set_nom(self, nom):
        pass
    nom = property(_get_nom, _set_nom)

    def get_nom(self, nombre):
        """Retourne le nom singulier ou pluriel."""
        if nombre <= 0:
            raise ValueError("le nombre {} est négatif ou nul".format(nombre))

        if nombre == 1:
            return self.nom_singulier
        else:
            nombre = get_nom_nombre(nombre)
            return nombre + " " + self.nom_pluriel

    def get_nom_etat(self, nombre):
        """Retourne le nom et l'état en fonction du nombre."""
        if nombre <= 0:
            raise ValueError("le nombre {} est négatif ou nul".format(nombre))

        if nombre == 1:
            return self.get_nom(1) + " " + self.etat_singulier
        else:
            return self.get_nom(nombre) + " " + self.etat_pluriel

    def detruire(self):
        """Destruction du décor."""
        BaseObj.detruire(self)
        self.description.detruire()

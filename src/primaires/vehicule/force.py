# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 DAVY Guillaume
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


"""Fichier contenant la classe Force, détaillée plus bas."""

from abstraits.obase import *
from math import sqrt
from .vecteur import Vecteur

class Force(BaseObj):

    """Classe représentant une force.

    """

    def __init__(self, subissant=None):
        """Constructeur de la force"""
        BaseObj.__init__(self)
        self.subissant = subissant
        self.desuette = False
        self._construire()

    def __getnewargs__(self):
        return ()

    def __str__(self):
        return str(self.calcul())

    @property
    def valeur(self):
        return self.calcul()

    def calcul(self):
        return Vecteur(0, 0, 0)

class Propulsion(Force):

    """Classe représentant une force de propulsion.

    """

    def __init__(self, valeur=None):
        """Constructeur de la force"""
        Force.__init__(self)

        if valeur:
            self._valeur = valeur
        else:
            self._valeur = Vecteur(1, 0, 0)
        self._valeur._construire()

    def calcul(self):
        return self._valeur

class Frottement(Force):

    """Classe représentant une force de frottement.

    """

    def __init__(self, subissant, coef):
        """Constructeur de la force"""
        Force.__init__(self, subissant)

        self.coef = coef

    def __getnewargs__(self):
        return (None, 1)

    def calcul(self):
        return -self.coef * self.subissant.vitesse

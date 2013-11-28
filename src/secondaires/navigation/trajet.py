# -*-coding:Utf-8 -*

# Copyright (c) 2013 LE GOFF Vincent
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


"""Fichier contenant la classe Trajet, détaillée plus bas."""

from collections import OrderedDict

from abstraits.obase import BaseObj

class Trajet(BaseObj):

    """Classe représentant un trajet maritime entre deux points.

    Un trajet est une suite de points (deux au minimum). Le premier
    est le point de départ, le dernier est l'arrivée, les points
    intermédiaires sont les points intermédiaires entre le point de
    départ et l'arrivée. Ces points doivent être sélectionnés de telle
    sorte qu'aucun obstacle prévisible (côte ou obstacle) n'empêche de
    faire la ligne directe entre deux points.

    """

    enregistrer = True
    def __init__(self, cle):
        """Constructeur du trajet."""
        BaseObj.__init__(self)
        self.cle = cle
        self.point_depart = None
        self.points = OrderedDict()

    def __getnewargs__(self):
        return ("inconnu", )

    def __repr__(self):
        return "<Trajet {}>".format(repr(self.cle))

    def __str__(self):
        return self.cle

    @property
    def point_arrivee(self):
        """Retourne le point d'arrivée."""
        return list(self.points.values())[-1]

    def ajouter_point(self, depuis, vers):
        """Ajoute le point entre depuis et vers.

        Ces deux paramètres doivent être des tuple (x, y).

        """
        if self.point_depart is None:
            raise ValueError("Ce trajet n'a aucun point de départ défini")

        self.points[depuis] = vers

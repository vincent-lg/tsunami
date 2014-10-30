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

"""Fichier décrivant la classe Race, détaillée plus bas."""

from abstraits.obase import BaseObj
from bases.collections.flags import Flags
from primaires.format.description import Description

from .stats import Stats
from .genres import Genres

class Race(BaseObj):

    """Classe définissant les races des personnages.

    """

    enregistrer = True
    def_flags = Flags()
    def_flags.ajouter("nyctalope")

    def __init__(self, nom):
        """Constructeur d'une race."""
        BaseObj.__init__(self)
        self.nom = nom
        self.description = Description(parent=self)
        self.stats = Stats(parent=self)
        self.genres = Genres(parent=self)
        self.squelette = None
        self.flags = 0
        self._construire()

    def __getnewargs__(self):
        return ("", )

    def __str__(self):
        return self.nom

    @property
    def nom_squelette(self):
        """Retourne le nom du squelette si défini"""
        res = ""
        if self.squelette:
            res = self.squelette.nom

        return res

    @property
    def cle_squelette(self):
        """Retourne la clé du squelette si défini"""
        res = ""
        if self.squelette:
            res = self.squelette.cle

        return res

    def a_flag(self, nom_flag):
        """Retourne True si la race a le flag, False sinon."""
        valeur = type(self).def_flags[nom_flag]
        return self.flags & valeur != 0

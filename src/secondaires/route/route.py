# -*-coding:Utf-8 -*

# Copyright (c) 2015 LE GOFF Vincent
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


"""Fichier contenant la classe Route, détaillée plus bas."""

from abstraits.obase import BaseObj

class Route(BaseObj):

    """Classe représentant une route.

    Une route relie deux salles (origine et destination) et
    indique les sorties intermédiaires qui doivent être prises pour
    se déplacer d'origine à destination.

    """

    enregistrer = True

    def __init__(self, origine):
        """Constructeur de la fiche."""
        BaseObj.__init__(self)
        self.origine = origine
        self.destination = destination
        self.salles = []
        self.sorties = []
        self._construire()

    def __getnewargs__(self):
        return (None, )

    def __repr__(self):
        return "<Route {}>".format(self.str_ident)

    def __str__(self):
        return self.str_ident

    @property
    def ident(self):
        origine = self.origine
        ident = []
        if origine:
            ident.append(self.origine.ident)
            if self.destination:
                ident.append(self.destination.ident)

        return tuple(ident)

    @property
    def str_ident(self):
        ident = self.ident
        if len(ident) == 2:
            return "de {} à {}".format(ident[0], ident[1])
        elif len(ident) == 1:
            return "de {} à ...".format(ident[0])
        else:
            return "inconnue"

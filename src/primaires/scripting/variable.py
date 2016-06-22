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


"""Fichier contenant la classe Variable détaillée plus bas."""

from abstraits.obase import *

class Variable(BaseObj):

    """Classe contenant une variable d'évènement.

    Une variable d'évènement contient un nom, un certain type bien entendu,
    ainsi qu'une aide.

    """

    _nom = "variable_scripting"
    _version = 1

    def __init__(self, evenement, nom, str_type=None):
        """Constructeur d'une variable"""
        BaseObj.__init__(self)
        self.evenement = evenement
        self.nom = nom
        self.nom_type = str_type
        self.aide = "non précisée"
        self._construire()

    def __getnewargs__(self):
        return (None, "")

    def _get_type(self):
        types = __import__("primaires.scripting.types").scripting.types
        builtins = __builtins__.copy()
        try:
            type = builtins[self.nom_type]
        except KeyError:
            type = getattr(types, self.nom_type)

        return type
    def _set_type(self, type):
        self.nom_type = type.__name__
    type = property(_get_type, _set_type)

    def __getstate__(self):
        attrs = self.__dict__.copy()
        if "type" in attrs:
            del attrs["type"]

        return attrs

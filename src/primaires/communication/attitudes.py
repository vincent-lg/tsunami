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


"""Ce fichier contient la classe Attitudes détaillée plus bas."""

from abstraits.obase import BaseObj
from .attitude import Attitude

class Attitudes(BaseObj):

    """Classe conteneur des attitudes sociales.
    Cette classe liste tous les items Attitude utilisables dans l'univers
    à un instant donné.

    Voir : ./attitude.py

    """

    enregistrer = True
    def __init__(self):
        """Constructeur du conteneur"""
        BaseObj.__init__(self)
        self._attitudes = {}
        self._construire()

    def __getnewargs__(self):
        return ()

    def __bool__(self):
        return bool(self._attitudes)

    def __contains__(self, cle):
        """Renvoie True si l'attitude existe, False sinon"""
        return cle in self._attitudes

    def __len__(self):
        return len(self._attitudes)

    def __getitem__(self, cle):
        """Renvoie une attitude à partir de sa clé"""
        return self._attitudes[cle]

    def __setitem__(self, cle, valeur):
        """Ajoute une attitude à la liste"""
        self._attitudes[cle] = valeur

    def __delitem__(self, cle):
        """Détruit l'attitude spécifiée"""
        del self._attitudes[cle]

    def keys(self):
        """Renvoie une liste des attitudes par clés"""
        return list(self._attitudes.keys())

    def values(self):
        """Renvoie une liste des objets Attitude"""
        return list(self._attitudes.values())

    def ajouter_ou_modifier(self, cle):
        """Ajoute une attitude ou la renvoie si existante"""
        if cle in self._attitudes:
            return self._attitudes[cle]
        else:
            attitude = Attitude(cle, self)
            self._attitudes[cle] = attitude
            return attitude

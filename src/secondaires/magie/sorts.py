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


"""Fichier contenant la classe Sorts, détaillée plus bas."""

from abstraits.obase import BaseObj
from .sort import Sort

class Sorts(BaseObj):

    """Classe-conteneur des sorts.

    Cette classe contient tous les sortilèges et autres maléfices de
    l'univers, éditables et utilisables, et offre quelques méthodes de
    manipulation.

    Voir : ./sort.py

    """

    enregistrer = True
    def __init__(self):
        """Constructeur du conteneur"""
        BaseObj.__init__(self)
        self.__sorts = {}
        self._construire()

    def __getnewargs__(self):
        return ()

    def __contains__(self, cle):
        """Renvoie True si le sort existe, False sinon"""
        return cle in self.__sorts

    def __len__(self):
        return len(self.__sorts)

    def __getitem__(self, cle):
        """Renvoie un sort à partir de sa clé"""
        return self.__sorts[cle]

    def __setitem__(self, cle, sort):
        """Ajoute un sort à la liste"""
        self._enregistrer()
        self.__sorts[cle] = sort

    def __delitem__(self, cle):
        """Détruit le sort spécifié"""
        self._enregistrer()
        del self.__sorts[cle]

    def values(self):
        return self.__sorts.values()

    def ajouter_ou_modifier(self, cle):
        """Ajoute un sort ou le renvoie si existant"""
        if cle in self.__sorts:
            return self.__sorts[cle]
        else:
            sort = Sort(cle, self)
            self.__sorts[cle] = sort
            self._enregistrer()
            return sort

    def get(self, cle, valeur=None):
        """Retourne le sort ou valeur si non présent."""
        return self.__sorts.get(cle, valeur)

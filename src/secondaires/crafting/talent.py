# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
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


"""Fichier contenant la classe Talent, détaillée plus bas."""

from abstraits.obase import BaseObj

class Talent(BaseObj):

    """Classe représentant un talent de guilde.

    Il s'agit pratiquement d'un talent standard mais avec des
    informations spécifiques aux guildes.

    """

    def __init__(self, guilde, cle):
        """Constructeur du talent."""
        BaseObj.__init__(self)
        self.guilde = guilde
        self.cle = cle
        self.nom = "talent inconnu"
        self.niveau = "profession"
        self.difficulte = 25
        self._ouvert = False
        self.ouvert_a_tous = False
        self._construire()

    def __getnewargs__(self):
        return (None, "")

    def __repr__(self):
        return "<Talent {}>".format(self.cle)

    def __str__(self):
        return self.cle

    @property
    def nom_complet(self):
        return "{:<20} : {}".format(self.cle, self.nom)

    def _get_ouvert(self):
        return self._ouvert
    def _set_ouvert(self, ouvert):
        self._ouvert = ouvert
        if ouvert:
            self.ajouter()
    ouvert = property(_get_ouvert, _set_ouvert)

    def ajouter(self):
        """Ajoute le talent dans la liste des talents."""
        importeur.perso.ajouter_talent(self.cle, self.nom,
                self.niveau, self.difficulte, self.ouvert_a_tous)

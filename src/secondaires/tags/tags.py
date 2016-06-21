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


"""Fichier contenant la classe Tags, détaillée plus bas."""

from abstraits.obase import BaseObj

class Tags(BaseObj):

    """Classe représentant les tags.

    Cette tags associe un objet (une salle, un personnage
    ou autre) à une liste de tags.

    """

    enregistrer = True

    def __init__(self):
        BaseObj.__init__(self)
        self.tags = {}
        self._construire()

    def __getnewargs__(self):
        return ()

    def __getitem__(self, objet):
        """Lecture d'un tag."""
        if objet not in self.tags:
            self.tags[objet] = Liste(objet)
            self._enregistrer()

        return self.tags[objet]

    def detruire(self):
        """Destruction de tous les tags."""
        BaseObj.detruire(self)
        for liste in self.tags.values():
            for tag in liste.tags:
                tag.detruire()


class Liste(BaseObj):

    """Liste de tags."""

    def __init__(self, objet):
        BaseObj.__init__(self)
        self.objet = objet
        self.tags = []
        self._construire()

    def __getnewargs__(self):
        return (None, )

    def __repr__(self):
        return "<listeTags pour {}>".format(repr(objet))

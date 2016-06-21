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


"""Fichier contenant la classe Tag, détaillée plus bas."""

from abstraits.obase import BaseObj
from secondaires.tags.script import ScriptTag

class Tag(BaseObj):

    """Classe représentant un tag."""

    enregistrer = True

    def __init__(self, cle, type):
        """Constructeur de la fiche."""
        BaseObj.__init__(self)
        self.cle = cle
        self.type = type
        self.script = ScriptTag(self)
        self._construire()

    def __getnewargs__(self):
        return ("inconnu", "inconnu")

    def __repr__(self):
        return "<Tag {} de type {}>".format(repr(self.cle), repr(self.type))

    def __str__(self):
        return self.cle

    def copier_evenement(self, depuis):
        """Copie l'éévènement depuis l'évènement passé en paramètre."""
        parent = self.script
        noms = depuis.nom_complet.split(".")
        for nom in noms:
            parent = parent.creer_evenement(nom)

        parent.copier_depuis(depuis)

    def detruire(self):
        """Destruction du tag."""
        BaseObj.detruire(self)
        self.script.detruire()

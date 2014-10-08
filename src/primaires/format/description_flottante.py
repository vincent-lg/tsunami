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


"""Fichier contenant la classe DescriptionFlottante, détaillée plus bas."""

from abstraits.obase import BaseObj
from primaires.format.description import Description

class DescriptionFlottante(BaseObj):

    """Classe représentant une description flottante.

    C'est principalement une description comme les autres (avec des
    paragraphes, un script, des syboles, etc) mais qui n'est par défaut
    rattaché à rien dans l'univers. Pour l'appeler il faut l'inclure
    dans une autre description, grâce à la syntaxe '@cle_flottante'. La
    gestion des descriptions dynamiques fonctionne selon un principe
    hiérarchique : si la description A inclue la description B et que
    la description finale contient '$chemin', l'évènement 'regarde.chemin'
    est recherché, d'abord dans la description A, puis dans la description
    B (incluse).

    Ses attributs sont :
        cle -- la clé identifiant la description flottante (doit être unique)
        description -- la description flottante-même
                       dans une liste)
    """

    enregistrer = True
    def __init__(self, cle):
        """Constructeur de la description flottante."""
        BaseObj.__init__(self)
        self.cle = cle
        self.description = Description(parent=self, scriptable=True)
        self._construire()

    def __getnewargs__(self):
        return ("inconnue", )

    def __repr__(self):
        return "<DescriptionFlottante {}>".format(self.cle)

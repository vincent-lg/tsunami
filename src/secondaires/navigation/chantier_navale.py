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


"""Fichier contenant la classe ChantierNavale, détaillée plus bas."""

from abstraits.obase import BaseObj
from secondaires.navigation.commande_chantier import CommandeChantierNavale

class ChantierNavale(BaseObj):

    """Classe décrivant un chantier navale.

    Un chantier navale est un ensemble de salles que l'on peut utiliser pour
    la réparation et la personnalisation d'un navire en particulier. Un
    chantier navale possède une salle d'interaction (nommée 'salle_magasin')
    et des points d'occupation qui déterminent le lieu des bassins. Si le
    navire souhaité n'est pas dans le bassin d'un chantier, le chantier ne
    pourra pas travailler dessus.

    """

    enregistrer = True
    def __init__(self, cle):
        BaseObj.__init__(self)
        self.cle = cle
        self.salle_magasin = None
        self.points = []
        self.commandes = []
        self._construire()

    def __getnewargs__(self):
        return ("inconnu", )

    def __repr__(self):
        return "<ChantierNavale {}>".format(repr(self.cle))

    def __str__(self):
        return self.cle

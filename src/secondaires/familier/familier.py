# -*-coding:Utf-8 -*

# Copyright (c) 2014 LE GOFF Vincent
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


"""Fichier contenant la classe Familier, détaillée plus bas."""

from abstraits.obase import BaseObj

class Familier(BaseObj):

    """Classe représentant un familier.

    Un familier est une sur-couche d'un PNJ, définissant certains
    attributs propres à un familier mais n'intéressant pas le PNJ.
    Par exemple, un familier, contrairement à un PNJ, a un maître.
    Cependant, un familier est toujours modelé sur un PNJ.

    Supposons par exemple que vous avez défini le prototype de PNJ
    'cheval'. Vous créez une fiche de familier de même clé : côté
    du module 'pnj', rien ne se passe. Si vous faites apparaître un
    'cheval', le PNJ sera créé. Mais aucun familier ne sera créé.
    Pour cela, un joueur devra apprivoiser le 'cheval'. À partir du
    moment où il le fait, le PNJ ne s'altère pas mais un familier
    est créé sur ce PNJ. Si le PNJ est détruit (il meurt par exemple),
    le familier est détruit. Mais le familier peut être détruit sans
    que le PNJ soit affecté, si par exemple le maître actuel du
    familier libère le libère.

    """

    enregistrer = True

    def __init__(self, pnj):
        """Constructeur du navire."""
        BaseObj.__init__(self)
        self.pnj = pnj
        self.maitre = None
        self.faim = 0
        self.soif = 0
        self.nom = "Médor"
        self.chevauche_par = None

    def __getnewargs__(self):
        return ("", )

    def __repr__(self):
        return "<Familier {} appartenant à {}>".format(
                self.cle, self.maitre)

    def __str__(self):
        return self.cle

    @property
    def cle(self):
        """Retourne la clé du PNJ."""
        return self.pnj and self.pnj.cle or "aucune"

    @property
    def fiche(self):
        """Retourne la fiche du familier."""
        return importeur.familier.fiches[self.cle]

    @property
    def identifiant(self):
        return self.pnj and self.pnj.identifiant or "aucun"

    @property
    def nom_maitre(self):
        return self.maitre and self.maitre.nom or "aucun"

    @property
    def salle(self):
        return self.pnj and self.pnj.salle or "aucune"

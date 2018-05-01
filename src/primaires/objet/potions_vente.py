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


"""Ce fichier contient la classe PotionsVente, détaillée plus bas."""

from abstraits.obase import BaseObj
from .potion_vente import PotionVente

class PotionsVente(BaseObj):

    """Classe enveloppe de toutes les potions en vente.

    Cette classe est un dictionnaire fictif contenant des PotionVente
    (voir ./potion_vente.py).

    """

    def __init__(self):
        """Constructeur de la classe"""
        BaseObj.__init__(self)
        self._construire()

    def __getnewargs__(self):
        return ()

    def __contains__(self, cle):
        """Teste si on peut vendre une clé conteneur/potion"""
        try:
            c, p = cle.split("/")
        except ValueError:
            return False
        else:
            proto = importeur.objet.prototypes
            return c in proto and proto[c].est_de_type("conteneur de potion") \
                    and p in proto and proto[p].est_de_type("potion")

    def __getitem__(self, cle):
        """Retourne un objet PotionVente"""
        try:
            c, p = cle.split("/")
        except ValueError:
            raise KeyError
        else:
            proto = importeur.objet.prototypes
            if cle in self:
                return PotionVente(proto[c], proto[p])
            raise KeyError

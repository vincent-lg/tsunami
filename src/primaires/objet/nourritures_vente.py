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


"""Ce fichier contient la classe NourrituresVente, détaillée plus bas."""

from abstraits.obase import BaseObj
from .nourriture_vente import NourritureVente

class NourrituresVente(BaseObj):

    """Classe enveloppe de la nourriture dans le commerce

    Cette classe est un dictionnaire fictif contenant des NourritureVente
    (voir ./potion_vente.py).

    """

    def __init__(self):
        """Constructeur de la classe"""
        BaseObj.__init__(self)
        self._construire()

    def __getnewargs__(self):
        return ()

    def __contains__(self, cle):
        """Teste si on peut vendre une clé conteneur/n1+n2+n3"""
        try:
            c, n = cle.split("/")
            n = n.split("+")
        except ValueError:
            return False
        else:
            proto = importeur.objet.prototypes
            return all(p in proto for p in n + [c]) \
                    and proto[c].est_de_type("conteneur de nourriture") \
                    and all(proto[p].est_de_type("nourriture") for p in n) \
                    and sum(proto[p].poids_unitaire for p in n) \
                    <= proto[c].poids_max

    def __getitem__(self, cle):
        """Retourne un objet NourritureVente"""
        try:
            c, n = cle.split("/")
            n = n.split("+")
        except ValueError:
            raise KeyError
        else:
            proto = importeur.objet.prototypes
            if cle in self:
                return NourritureVente(proto[c], [proto[p] for p in n])
            raise KeyError

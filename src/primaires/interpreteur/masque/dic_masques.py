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


"""Fichier contenant la classe DicMasques."""

from collections import OrderedDict

class DicMasques(OrderedDict):

    """Dictionnaire ordonné contenant les masques."""

    def __str__(self):
        """Affichage plus propre des masques."""
        msgs = []
        for cle, masque in self.items():
            if masque.a_interpreter:
                msg = cle + "=" + repr(masque.a_interpreter)
            else:
                msg = masque.nom_francais
            msgs.append(msg)
        
        return " ".join(msgs)
    
    def __getitem__(self, item):
        """Retourne l'item si présent ou None sinon"""
        if item not in self:
            res = None
        else:
            res = OrderedDict.__getitem__(self, item)

        return res

    @property
    def premier(self):
        """Retourne le premier élément du dictionnaire"""
        return tuple(self.values())[0]

    @property
    def dernier(self):
        """Retourne le dernier élément du dictionnaire"""
        return tuple(self.values())[-1]

    @property
    def dernier_parametre(self):
        """Retourne le dernier paramètre"""
        for masque in reversed(list(self.values())):
            if masque.est_parametre():
                return masque

        raise ValueError("aucun paramètre dans ce dictionnaire")

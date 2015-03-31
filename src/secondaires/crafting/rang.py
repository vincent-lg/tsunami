# -*-coding:Utf-8 -*

# Copyright (c) 2015 LE GOFF Vincent
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


"""Fichier contenant la classe Rang, détaillée plus bas."""

from abstraits.obase import BaseObj
from secondaires.crafting.exception import ExceptionCrafting

class Rang(BaseObj):

    """Classe représentant un rang de guilde."""

    def __init__(self, guilde, cle):
        """Constructeur de la fiche."""
        BaseObj.__init__(self)
        self.guilde = guilde
        self.cle = cle
        self.nom = "rang inconnu"
        self.points_guilde = 10
        self._construire()

    def __getnewargs__(self):
        return (None, "")

    @property
    def total_points_guilde(self):
        """Retourne les points de guilde consommés pour arriver à ce rang.

        Si le rang a des prédécesseurs, retourne la somme des
        points de guilde nécessités pour atteindre ce rang. Par
        exemple, si un membre est au rang 2, il faut additionner
        les points de guilde du rang 1 et du rang 2.

        """
        # Cherche à trouver les rangs prédécesseurs
        guilde = self.guilde
        try:
            indice = guilde.rangs.index(self)
        except ValueError:
            raise RangIntrouvable("le rang {} ne peut être trouvé " \
                    "dans la guilde {}".format(self.cle, guilde.cle))

        precedents = guilde.rangs[:indice]
        return sum(p.points_guilde for p in precedents) + self.points_guilde


class RangIntrouvable(ExceptionCrafting):

    """Exception levée si le rang de la guilde est introuvable."""

    pass

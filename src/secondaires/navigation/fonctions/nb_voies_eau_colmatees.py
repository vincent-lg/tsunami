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


"""Fichier contenant la fonction nb_voies_eau_colmatees."""

from fractions import Fraction

from primaires.scripting.fonction import Fonction
from secondaires.navigation.constantes import *

class ClasseFonction(Fonction):

    """Retourne le nombre de voies d'eau colmatées du navire.

    Cette fonction retourne le nombre de voies d'eau colmatées (c'est-à-dire
    les brèches dans la coque réparées grâce à la commande calfeutrer/seal).
    Le nombre renvoyé est au maximum égal au nombre de salles du navire
    (les salles noyables, du moins).

    """

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.nb_voies_eau_colmatees_salle, "Salle")

    @staticmethod
    def nb_voies_eau_colmatees_salle(salle):
        """Retourne le nombre de voies d'eau colmatées dans le navire."""
        if getattr(salle, "navire", None) is None:
            return 0

        navire = salle.navire
        nb = len([s for s in navire.salles.values() if \
                s.voie_eau == COQUE_COLMATEE])
        return Fraction(nb)

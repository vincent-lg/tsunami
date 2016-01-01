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


"""Fichier contenant la fonction poids_eau."""

from fractions import Fraction

from primaires.scripting.fonction import Fonction

class ClasseFonction(Fonction):

    """Retourne le pourcentage de poids d'eau d'un navire.

    Si le navire n'a embarqué aucune vague, retourne 0. Si le navire
    est sur le point de couler, retourne 100. Sinon, retourne le
    pourcentage (poids_eau_embarqué / poids_total_supporté * 100).

    Notez que le navire peut avoir embarqué beaucoup d'eau mais n'avoir
    aucune voie d'eau dans sa coque. Un membre d'équipage peut avoir
    réparé celles-ci mais le navire avoir autant d'eau qu'avant, tant
    qu'il n'a pas écopé. Notez également que cette fonction prend une
    salle en paramètre et retourne le pourcentage correspondant au navire,
    pas à la salle-même.

    """

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.poids_eau_salle, "Salle")

    @staticmethod
    def poids_eau_salle(salle):
        """Retourne le pourcentage de poids d'eau du navire.

        Si la salle ne fait pas parti d'un navire, retourne 0.

        """
        if getattr(salle, "navire", None) is None:
            return 0

        navire = salle.navire
        pourcent = navire.poids / navire.poids_max * 100
        pourcent = round(pourcent, 2)
        return Fraction(pourcent)

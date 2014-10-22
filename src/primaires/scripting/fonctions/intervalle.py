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


"""Fichier contenant la fonction intervalle."""

from fractions import Fraction

from primaires.scripting.fonction import Fonction

class ClasseFonction(Fonction):

    """Retourne une liste contenant un intervalle de valeurs entières itérable."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.intervalle, "Fraction", "Fraction")
        cls.ajouter_types(cls.intervalle_debut, "Fraction")
        cls.ajouter_types(cls.intervalle_ecart, "Fraction", "Fraction", "Fraction")

    @staticmethod
    def intervalle(valMin, valMax):
        """Retourne une liste contenant un intervalle de valeurs entières entre valMin et valMax inclus."""
        return range(int(valMin), int(valMax))
	
    @staticmethod
    def intervalle_debut(valMax):
        """Retourne une liste contenant un intervalle de valeurs entières entre 1 et valMax inclus (pratique pour itérer dans une liste)."""
        return range(1, int(valMax))
        
    @staticmethod
    def intervalle_ecart(valMin, valMax, ecart):
        """Retourne une liste contenant un intervalle de valeurs entières entre valMin et valMax inclus, avec un écart entre chaque valeur de ecart."""
        return range(int(valMin), int(valMax), int(ecart))

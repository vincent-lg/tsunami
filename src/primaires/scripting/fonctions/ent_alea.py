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


"""Fichier contenant la fonction ent_alea."""

from random import randint, random, choice
from fractions import Fraction

from primaires.scripting.fonction import Fonction

class ClasseFonction(Fonction):

    """Retourne un entier aléatoire."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.ent_alea, "Fraction")
        cls.ajouter_types(cls.ent_alea_pond, "Fraction", "Fraction")

    @staticmethod
    def ent_alea(max):
        """Retourne un entier aléatoire entre 1 et la valeur maximale précisée.

        """
        return Fraction(randint(1, int(max)))
    
    @staticmethod
    def ent_alea_pond(max, pond):
        """Retourne un entier aléatoire entre 1 et la valeur maximale,
        pondéré par la valeur précisée en deuxième argument.
        Cette fonction est utile pour calculer des dégâts en fonction
        d'un talent d'un personnage.
        
        """
        seq = []
        for i in range(100):
            for x in range(100 - abs(i - int(pond))):
                seq.append(i)            
        return Fraction(choice(seq))

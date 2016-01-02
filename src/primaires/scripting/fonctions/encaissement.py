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


"""Fichier contenant la fonction encaissement."""

from fractions import Fraction

from primaires.scripting.fonction import Fonction

class ClasseFonction(Fonction):

    """Retourne l'encaissement de dégâts pour un personnage.

    Cette fonction retourne un nombre. Elle tient compte de l'armure globale
    du personnage pour encaisser une partie des dégâts. L'armure globale d'un
    personnage est la somme de l'encaissement de toutes les armures qu'il
    équipe, pue importe leur emplacement. Les dégâts retournés sont au
    moins 50% des dégâts précisés en paramètre. Les 50% restants sont en
    partie encaissée par l'armure.

    Par exemple :

        degats = 100
        degats = encaissement(personnage, degats)
        # Si le personnage n'a aucune armure, degats contient 100
        # Si il contient plusieurs armures protégeant de 50 ou plus, retourne
        # 50 (100 / 2)

    """

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.encaissement, "Personnage", "Fraction")

    @staticmethod
    def encaissement(personnage, degats):
        """Retourne l'encaissement (entre 50 et 100% des dégâts précisés)."""
        base = degats / 2
        armure = personnage.armure
        if armure >= base:
            return base

        return base + (base - armure)

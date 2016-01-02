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


"""Fichier contenant la fonction distance."""

from fractions import Fraction

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution
from primaires.vehicule.vecteur import Vecteur

class ClasseFonction(Fonction):

    """Retourne la distance entre deux salles."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.distance, "Salle", "Salle")

    @staticmethod
    def distance(origine, destination):
        """Retourne la distance entre deux salles.

        Les deux salles doivent avoir des coordonnées valides. La
        distance retournée est le nombre de salle séparant origine et
        destination ajouté à 1. Ce calcul est absolu, c'est-à-dire que les
        deux salles origine et destination n'ont pas nécessairement besoin
        d'être reliées avec des salles intermédiaires. Deux salles
        voisines (séparées par une sortie) ont une distance de 1. Notez
        également que cette fonction peut retourner des distances avec
        virgule (si vous demandez par exemple la distance entre une salle
        de terre et une salle de navire).

        Paramètres à préciser :

          * origine : la salle d'origine
          * destination : la salle de destination

        Exemples d'utilisation :

          origine = salle("depart:1")
          destination = salle("depart:5")
          distance = distance(origine, destination)

        """
        if origine is destination:
            return Fraction(0)

        if not origine.coords.valide:
            raise ErreurExecution("{} n'a pas de coordonnées valides".format(
                    origine))

        if not destination.coords.valide:
            raise ErreurExecution("{} n'a pas de coordonnées valides".format(
                    destination))

        o_x, o_y, o_z = origine.coords.tuple()
        d_x, d_y, d_z = destination.coords.tuple()
        vecteur = Vecteur(d_x - o_x, d_y - o_y, d_z - o_z)
        sortie = origine.get_sortie(vecteur, destination)
        return Fraction(sortie.longueur)

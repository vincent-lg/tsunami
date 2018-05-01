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


"""Fichier contenant la fonction nb_plantes."""

from fractions import Fraction

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Retourne le nombre de plantes."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.nb_plantes_proto, "str")
        cls.ajouter_types(cls.nb_plantes_salle, "Salle", "str")

    @staticmethod
    def nb_plantes_proto(cle_plante):
        """Retourne le nombre de plantes du végétal indiqué.

        Paramètres à préciser :

          * cle_plante : la clé du végétal à rechercher.

        Si le prototype de végétal n'existe pas, une alerte est créée.

        Exemple d'utilisation :

          nb = nb_plantes("pommier_sauvage")

        """
        cle_plante = cle_plante.lower()
        prototype = importeur.botanique.prototypes.get(cle_plante)
        if prototype is None:
            raise ErreurExecution("le végétal {} est introuvable".format(
                    repr(cle_plante)))

        return Fraction(len(prototype.plantes))

    @staticmethod
    def nb_plantes_salle(salle, cle_plante):
        """Retourne le nombre de plantes dans la salle.

        Paramètres à préciser :

          * salle : la salle dans laquelle se trouve les plantes
          * cle_plante : la clé du végétal à rechercher.

        Si le prototype de végétal n'existe pas, une alerte est créée.

        Exemple d'utilisation :

          nb = nb_plantes(salle, "pommier_sauvage")

        """
        cle_plante = cle_plante.lower()
        prototype = importeur.botanique.prototypes.get(cle_plante)
        if prototype is None:
            raise ErreurExecution("le végétal {} est introuvable".format(
                    repr(cle_plante)))

        plantes = importeur.botanique.salles.get(salle, [])
        plantes = [p for p in plantes if p.cle == cle_plante]
        return Fraction(len(plantes))

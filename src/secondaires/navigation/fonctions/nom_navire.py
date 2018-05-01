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


"""Fichier contenant la fonction nom_navire."""

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Retourne le nom du navire."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.nom_navire_salle, "Salle")

    @staticmethod
    def nom_navire_salle(salle):
        """Retourne le nom du navire à laquelle la salle appartient.

        Paramètres à préciser :

          * salle : la salle à préciser.

        Si la salle ne fait pas parti d'un navire, crée une alerte.

        Exemple d'utilisation :

          # On sait que la variable 'salle' contient une salle de navire
          nom = nom_navire(salle)
          # Si le navire n'a aucun nom, la chaîne sera vide
          si nom:
              # Le navire a bien un nom
          sinon:
              # Le navire n'a pas de nom

        """
        if not hasattr(salle, "navire") or salle.navire is None or \
                salle.navire.etendue is None:
            raise ErreurExecution("la salle {} n'est pas une salle de " \
                    "navire".format(salle))

        return salle.navire.nom_personnalise

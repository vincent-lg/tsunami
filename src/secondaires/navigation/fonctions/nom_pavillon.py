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


"""Fichier contenant la fonction nom_pavillon."""

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Retourne le nom du pavillon."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.nom_pavillon_salle, "Salle")

    @staticmethod
    def nom_pavillon_salle(salle):
        """Retourne le nom du pavillon du navire.

        Paramètres à préciser :

          * salle : la salle de navire

        Si la salle ne fait pas parti du navire, crée une alerte.
        Le nom singulier du pavillon est retourné dans le cas contraire.
        Si le navire n'a pas de pavillon hissé, retourne une chaîne vide.

        Exemple d'utilisation :

          # On sait que la variable 'salle' contient une salle de navire
          nom = nom_pavillon(salle)
          # Si le navire n'a pas de pavillon, la chaîne sera vide
          si nom:
              # Le navire a un pavillon hissé
          sinon:
              # Le navire n'a pas de pavillon hissé

        """
        if not hasattr(salle, "navire") or salle.navire is None or \
                salle.navire.etendue is None:
            raise ErreurExecution("la salle {} n'est pas une salle de " \
                    "navire".format(salle))

        navire = salle.navire
        if navire.pavillon is None:
            return ""

        return navire.pavillon.nom_singulier

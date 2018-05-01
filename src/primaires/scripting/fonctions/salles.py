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


"""Fichier contenant la fonction salles."""

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Retourne une liste de salles."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.salles)
        cls.ajouter_types(cls.salles, "str")

    @staticmethod
    def salles(nom_zone="*"):
        """Retourne toutes les salles.

        Si le nom de la zone est passé en paramètre, ne retourne
        que les salles de la zone indiquée.

        Paramètres à préciser :

          * nom_zone : le nom de la zone (une chaîne)

        Si la zone n'est pas précisée, retourne toutes les salles
        de l'univers.

        Exemples d'utilisation :

          # Capture toutes les salles dans une liste
          salles = salles()
          # Capture seulement les salles de la zone 'depart'
          salles = salles("depart")

        """
        if nom_zone == "*":
            return list(importeur.salle._salles.values())
        else:
            nom_zone = nom_zone.lower()
            try:
                zone = importeur.salle.zones[nom_zone]
            except KeyError:
                raise ErreurExecution("zone {} inconnue".format(repr(nom_zone)))

            return list(zone.salles)

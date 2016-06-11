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


"""Fichier contenant la fonction diligences."""

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Retourne les diligences (salle d'entrée)."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.toutes_diligences)

    @staticmethod
    def toutes_diligences():
        """Retourne toutes les diligences de l'univers.

        Cette fonction retourne toutes les diligences sous la forme
        d'une liste. Cette liste contient des salles. Les fonctions
        et actions manipulant les diligencs attendent une salle
        comme paramètre : les salles retournées sont les salles
        d'entrées (celles de mnémonique "1"). La diligence possède
        normalement une sortie "bas" menant vers la salle permettant
        d'accéder à la diligence.

        Cette fonction n'attend aucun paramètre.

        Exemple d'utilisation :

          diligences = diligences()
          pour chaque entree dans diligences:
              exterieur = destination(entree, "bas")
              # exterieur contient la salle à l'extérieur de la diligence
          fait

        """
        zones = importeur.diligence.zones
        entrees = []
        for zone in zones:
            salle = importeur.salle.salles.get("{}:1".format(zone.cle))
            if salle:
                entrees.append(salle)

        return entrees

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


"""Fichier contenant la fonction PNJ1."""

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Retourne le premier PNJ."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.PNJ1_salle, "Salle")
        cls.ajouter_types(cls.PNJ1_salle, "Salle", "str")
        cls.ajouter_types(cls.tous_PNJ1, "str")

    @staticmethod
    def PNJ1_salle(salle, cle=""):
        """Retourne le premier PNJ présent dans la salle.

        Cette fonction retourne le premier PNJ présent, pas le joueur,
        ou une valeur nulle si il n'y a aucun PNJ.

        Paramètres à préciser :

          * salle : la salle dans laquelle trouver le PNJ
          * cle (optionnel) : la clé de prototype de PNJ

        Exemple d'utilisation :

          # En admettant qu'une salle est contenue dans la variable salle
          # Capture le premier PNJ présent dans la salle
          pnj = PNJ1(salle)
          si pnj:
              dire pnj "Tu es le premier."
          finsi
          # Capture seulement le premier PNJ de prototype 'souris'
          pnj = PNJ1(salle, "souris")
          si pnj:
              ...
          finsi

        """
        pnj = salle.PNJ
        if cle:
            pnj = [p for p in pnj if p.cle == cle]

        return pnj and pnj[0] or None

    @staticmethod
    def tous_PNJ1(cle_prototype):
        """Retourne le premier PNJ du prototype.

        Paramètres à préciser :

          * cle_prototype : la clé du prototype de PNJ

        Vous devez préciser la clé du prototype sous la
        forme d'une chaîne. Le premier PNJ de ce prototype sera
        retourné (le plus ancien) ou une valeur nulle si il n'y a
        aucun PNJ de ce prototype.

        Exemple d'utilisation :

          pnj = PNJ1("marchand_myr")
          si pnj:
              salle = salle(pnj)
              # salle contient la salle du PNJ1 parcouru

        """
        try:
            prototype = importeur.pnj.prototypes[cle_prototype.lower()]
        except KeyError:
            raise ErreurExecution("prototype inconnu {}".format(
                    repr(cle_prototype)))

        liste = list(prototype.pnj)
        return liste and liste[0] or None

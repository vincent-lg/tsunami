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


"""Fichier contenant l'action changer_puissance."""

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Change la puissance d'un feu dans une salle."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.changer_puissance, "Salle", "Fraction")

    @staticmethod
    def changer_puissance(salle, puissance):
        """Change la puissance du feu dans la salle.

        La puissance doit être entre 1 et 100. Une puissance inférieure
        à 5 donnera une durée de vie au feu très courte. Une puissance
        supérieure à 50 créera un incendie dans la salle qui se propagera.

        N'utilisez pas une puissance nulle ou négative pour supprimer
        un feu. Préférez l'action 'eteindre_feu'.

        """
        if salle.ident not in importeur.salle.feux:
            raise ErreurExecution("aucunf eu n'est allumé dans cette salle")

        if int(puissance) <= 0:
            raise ErreurExecution("la puissance fournie est négative ou nulle")

        feu = importeur.salle.feux[salle.ident]
        feu.puissance = int(puissance)

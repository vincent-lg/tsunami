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


"""Fichier contenant l'action allumer_feu."""

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Allume un feu dans une salle."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.allumer_feu, "Salle", "Fraction")

    @staticmethod
    def allumer_feu(salle, puissance):
        """Allume le feu dans la salle avec la puissance indiquée.

        La puissance doit être entre 1 et 100 : une puissance entre
        1 et 5 ne donnera une durée de vie au feu que très courte. Une
        puissance supérieure à 50 déclenchera un incendie qui se
        propagera de salle en salle.

        NOTE : aucun feu ne doit être allumé dans la salle. Utilisez la
        fonction 'feu_existe' pour le vérifier avant tout et, si vous voulez
        faire varier la puissance d'un feu existant, utiliser l'action
        'changer_puissance'.

        Enfin, cette action allume un feu dans la salle sans besoin de
        combustible. Si vous souhaitez utiliser du combustible, utiliser
        l'action 'allumer_feu_avec_combustible'.

        """
        if salle.ident in importeur.salle.feux:
            raise ErreurExecution("un feu est déjà allumé dans cette salle")

        importeur.salle.allumer_feu(salle, int(puissance))

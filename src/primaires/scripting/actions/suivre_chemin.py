# -*-coding:Utf-8 -*

# Copyright (c) 2013 LE GOFF Vincent
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


"""Fichier contenant l'action suivre_chemin."""

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Demande à un PNJ de suivre un chemin.

    Cette action demande à un PNJ de suivre un chemin indiqué. Notez
    qu'après l'appel à cette action, le personnage aura fait le premier
    pas dans le chemin spécifié (franchi la première sortie) mais le
    script se poursuivera avant que le chemin n'ait été entièrement
    parcouru. Si vous souhaitez effectuer des actions précises quand le
    chemin a été parcouru en entier, utilisez un autre évènement.

    """

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.suivre_chemin, "PNJ", "Fraction", "str")

    @staticmethod
    def suivre_chemin(pnj, temps, cle_chemin):
        """Demande au PNJ de suivre le chemin indiqué.

        Paramètres à préciser :

          * pnj : la variable contenant le PNJ
          * temps : le temps (en secondes) entre chaque déplacement
          * cle_chemin : la clé du chemin.

        Si vous souhaitez que le PNJ prenne le cheimn précisé en arrière
        (cela n'est pas toujours possible, vérifiez que votre chemin
        fonctionne bien dans les deux sens), précisez un point
        d'exclammation avant la clé du chemin.

        Exemple :

          suivre_chemin pnj 2 "!boutique_maison"

        """
        avant = True
        if cle_chemin.startswith("!"):
            cle_chemin = cle_chemin[1:]
            avant = False

        try:
            chemin = importeur.pnj.chemins[cle_chemin]
        except KeyError:
            raise ErreurExecution("Chemin {} introuvable".format(
                    repr(cle_chemin)))

        importeur.pnj.suivre_chemin(pnj, temps, chemin, avant)

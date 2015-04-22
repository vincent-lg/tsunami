# -*-coding:Utf-8 -*

# Copyright (c) 2015 LE GOFF Vincent
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


"""Fichier contenant l'action creer_alarme."""

from primaires.scripting.action import Action

class ClasseAction(Action):

    """Met en place une alarme pour un temps déterminé.

    Cette action est semblable à 'attendre' car elle demande d'attendre
    un temps précis avant de continuer l'exécution du script.
    Mais elle est plus précise, car elle crée une véritable
    alarme que l'on peut supprimer (empêchant ainsi le script
    de s'exécuter). Ce peut être le cas si vous voulez mettre
    en pause le script initial pendant un temps, mais qu'un
    autre script veuille interrompre ce temps d'attente.

    """

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.creer_alarme, "Fraction", "Personnage", "str")

    @staticmethod
    def creer_alarme(temps, personnage, cle_alarme):
        """Attend le nombre de secondes spécifiées et crée une alarme.

        L'alarme peut être supprimée dans l'intervalle grâce à
        l'action 'supprimer_alarme'.

        Paramètres à préciser :

          * temps : le temps d'attente (comme 'attendre')
          * personnage : le personnage devant posséder l'alarme
          * cle_alarme : la clé unique d'alarme

        Exemple d'utilisation :

          # Dans le script 1
          creer_alarme 5 personnage "pause"
          # Le script 1 va se mettre en pause pendant 5 secondes,
          # et une alarme "pause" sera créée dans le personnage.
          # Script 2 peut donc interrompre l'alarme :
          supprimer_alarme personnage "pause"

        """
        importeur.scripting.ecrire_alarme(personnage, cle_alarme)
        return (temps, personnage, cle_alarme)

    @property
    def code_python(self):
        return "yield " + Action.code_python.__get__(self)

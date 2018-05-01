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


"""Fichier contenant la fonction reussir_recette."""

from primaires.format.fonctions import supprimer_accents
from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Fait progresser un membre de guilde dans son rang."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.reussir_recette, "Personnage", "str", "str")

    @staticmethod
    def reussir_recette(personnage, cle_guilde, cle_recette):
        """Fait progresser le personnage dans le rang de la guilde.

        La recette est la clé du prototype d'objet d'une recette de
        rang. En fonction du nombre nécessaire, le personnage progresse
        dans le rang. Si par exemple il doit faire 3 epee_courte,
        il progressera les trois premières fois. Après, il ne
        progressera plus dans le rang (il aura fait cet objet 3 fois).
        Cette action est donc à mettre dans le cas où le personnage
        réussit l'objet de rang.

        Si la guilde n'est pas trouvée, crée une alerte. En revanche,
        si la recette n'est pas trouvée dans le rang, ne lève aucune
        alerte et ne fait rien (passe à la ligne suivante du script).

        Cette fonction retourne vrai si le personnage a bel et bien
        progressé dans son rang, faux sinon. Cela permet de faire
        différentes actions en fonction de la progression du
        personnage.

        Paramètres à préciser :

          * personnage : le personnage membre de la guilde
          * cle_guilde : la clé de guilde (une chaîne)
          * cle_recette : la clé de la recette (une chaîne)

        Exemple d'utilisation :

          si reussir_recette personnage "forgerons" "epee_courte":
              # Le personnage a réussit et progressé
          sinon:
            # Le personnage a réussit mais n'a pas progressé

        """
        cle_guilde = cle_guilde.lower()
        if cle_guilde not in importeur.crafting.guildes:
            raise ErreurExecution("La guilde {} n'existe pas".format(
                    repr(cle_guilde)))

        guilde = importeur.crafting.guildes[cle_guilde]

        if personnage not in guilde.membres:
            return False

        progression = guilde.membres[personnage]
        try:
            return progression.reussir_recette(cle_recette.lower())
        except ValueError:
            return False

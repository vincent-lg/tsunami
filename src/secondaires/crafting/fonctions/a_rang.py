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


"""Fichier contenant la fonction a_rang."""

from primaires.format.fonctions import supprimer_accents
from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Retourne vrai si le personnage a le rang indiqué dans la guilde."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.a_rang, "Personnage", "str")
        cls.ajouter_types(cls.a_rang, "Personnage", "str", "str")

    @staticmethod
    def a_rang(personnage, cle_guilde, cle_rang=""):
        """Retourne vrai si le personnage est du rang indiqué.

        Vous pouvez ne préciser que le personnage et la clé de la
        guilde pour savoir si le personnage est membre de la guilde,
        à quelque rang que ce soit. Consultez les exemples
        ci-dessous. Si vous précisez une clé de rang en troisième
        paramètre, cette fonction retourne vrai si le personnage est
        de ce rang ou de rang supérieur.

        Paramètres à préciser :

          * personnage : le personnage (membre ou non)
          * cle_guilde : la clé de la guilde (une chaîne)
          * cle_rang (optionnel) : la clé de rang (une chaîne)

        Exemples d'utilisation :

          # On admet une guilde 'forgerons' avec les rangs suivants :
          # - apprenti
          # - compagnon
          # - maitre
          si a_rang(personnage, "forgerons"):
              # personnage est membre de la guilde
          sinon:
              # personnage n'est ni apprenti, ni compagnon, ni maître
          finsi
          si a_rang(personnage, "forgerons", "compagnon"):
              # personnage est soit compagnon soit maitre
              ...
          finsi

        """
        cle_guilde = cle_guilde.lower()
        if cle_guilde not in importeur.crafting.guildes:
            raise ErreurExecution("La guilde {} n'existe pas".format(
                    repr(cle_guilde)))

        guilde = importeur.crafting.guildes[cle_guilde]

        if personnage not in guilde.membres:
            return False

        if cle_rang == "":
            return personnage in guilde.membres

        rang = guilde.get_rang(cle_rang)
        à_rang = guilde.membres[personnage].rang
        return rang in p_rang.rangs_parents

# -*-coding:Utf-8 -*

# Copyright (c) 2014 LE GOFF Vincent
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


"""Fichier contenant la fonction maitre."""

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Retourne le maître d'un familier PNJ."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.maitre, "Personnage")

    @staticmethod
    def maitre(pnj):
        """Retourne le maître d'un familier précisé.

        Paramètres à préciser :

          * pnj : le PNJ familier

        Si le PNJ précisé n'est pas un familier, envoie une alerte
        au système. Il est donc plus judicieux de vérifier auparavant
        que le PNJ est bien un familier :

          si est_familier(pnj):
              maitre = maitre(pnj)

        Vérifiez également que le maître est bien un personnage
        (le familier peut n'avoir aucun maître, même si ce cas de
        figure est rare).

          maitre = maitre(pnj)
          si maitre:
              # ... c'est bon, c'est un personnage

        """
        identifiant = getattr(pnj, "identifiant", None)
        if identifiant not in importeur.familier.familiers:
            raise ErreurExecution("le PNJ {} n'est pas un familier".format(
                    repr(identifiant)))

        familier = importeur.familier.familiers[identifiant]
        return familier.maitre

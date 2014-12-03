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


"""Fichier contenant la fonction est_allume."""

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Retourne vrai si est allumé."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.est_allume, "Objet")
        cls.ajouter_types(cls.prototype_est_allume, "PrototypeObjet")

    @staticmethod
    def est_allume(objet):
        """Retourne vrai si l'objet lumière est allumé, faux sinon.

        Paramètres à préciser :

          * objet : l'objet (type objet lumière)

        Cette fonction retourne vrai si l'objet lumière est allumé, faux sinon.

        Exemple d'utilisation :

          si est_allume(objet):

        """
        if not objet.est_de_type("lumière"):
            raise ErreurExecution("L'objet {} n'est pas une lumière.".format(
                    objet.identifiant))

        return objet.allumee_depuis is not None

    @staticmethod
    def prototype_est_allume(prototype):
        """Retourne invariablement faux.

        Cette fonction est simplement utilisée pour la compatibilité
        avec l'objet. Quand on examine le prototype, la lumière doit
        être éteinte.

        """
        return False

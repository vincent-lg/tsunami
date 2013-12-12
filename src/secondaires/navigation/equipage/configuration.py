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


"""Fichier contenant la classe Configuration, détaillée plus bas."""

from abstraits.obase import BaseObj
from secondaires.navigation.equipage.donnees.base import donnees

class Configuration(BaseObj):

    """Classe définissant la configuration d'un équipage.

    Cette classe définie les différentes données de configuration
    (comment les afficher, comment les modifier).

    """

    def __init__(self, equipage):
        """Constructeur du matelot."""
        BaseObj.__init__(self)
        self.equipage = equipage
        self.donnees = {}
        self._construire()

    def __getnewargs__(self):
        return (None, )

    def __repr__(self):
        return "<Configuration de l'équipage {}>".format(self.equipage)

    def __str__(self):
        msg = "Données de configuration {"
        for cle, donnee in sorted(self.donnees.items()):
            msg += "\n    " + cle + " : " + str(donnee)

        msg += "\n}"
        return msg

    def get(self, cle):
        """Retourne une donnée de configuration.

        Si la donnée de configuration n'est pas définie, retourne
        la valeur par défaut.

        """
        if cle not in donnees:
            raise ValueError("Donnée de configuration inconnue : ".format(
                    repr(cle)))

        if cle in self.donnees:
            return self.donnees[cle].valeur()

        return donnees[cle].defaut()

    def ecrire_donnee(self, donnee):
        """Écrit la donnée de configuration précisée."""
        self.donnees[donnee.cle] = donnee

    def ecrire_chaine(self, chaine):
        """Essaye d'écrire la chaîne en configuration."""
        for cls in donnees.values():
            arguments = cls.tester(chaine)
            if isinstance(arguments, tuple):
                donnee = cls(*arguments)
                self.ecrire_donnee(donnee)
                return

        raise ValueError("Impossible de trouver la donnée de " \
                "configuration correspondante")

    def supprimer_configuration(self, cle):
        """Supprime la configuration."""
        del self.donnees[cle]

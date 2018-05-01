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


"""Module définissant une classe statique pour tester le scripting."""

from contextlib import contextmanager

class ManipulationScripting:

    """Classe utilisée pour éditer du script dans les tests unitaires."""

    @staticmethod
    @contextmanager
    def scripter(objet, evenement, test=None):
        """Retourne un objet EditeurTest que l'on peut utilisé avec with.

        Exemple :

        with self.scripter(salle, "dire") as test:
            test.ecrire('deplacer personnage "porte"')

        Après la fermeture du bloc, le script est automatiquement
        effacé.

        """
        script = objet.script
        for nom in evenement.split("."):
            script = script[nom]

        if test is None:
            script.creer_sinon()
            test = script.sinon
        else:
            test = script.ajouter_test(test)

        # Création du context manager
        yield test

        # Suppression du test
        while test.instructions:
            test.supprimer_instruction(0)

        if test in test.evenement.tests:
            indice = test.evenement.tests.index(test)
            test.evenement.supprimer_test(indice)

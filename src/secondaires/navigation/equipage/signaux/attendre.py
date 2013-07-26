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


"""Fichier contenant la classe SignalAttendre."""

from secondaires.navigation.equipage.signaux.base import Signal

class SignalAttendre(Signal):

    """Signal utilisé pour attendre la fin de l'exécution d'un ordre.

    Cette classe est utilisée pour signaler à un ordre parent que
    le signal actuel attend l'exécution d'ordre enfant. Par exemple,
    l'ordre de se déplacer de plusieurs salles ne s'exécute pas
    instantanément : il fait une légère pause entre chaque déplacement.
    Si l'ordre de déplacement multiple est utilisé comme sous-ordre,
    alors quand le déplacement commence le déplacement multiple informe
    le script parent qu'il doit se mettre en pause le temps que
    l'action s'exécute.

    Ce signal prend en paramètre l'ordre dont on attend l'exécution.

    """

    def __init__(self, generateur_enfant):
        Signal.__init__(self)
        self.attendre = True
        self.generateur_enfant = generateur_enfant

    def __repr__(self):
        return "<signal attendre>"

    def traiter(self, generateur, profondeur):
        """Traite le générateur."""
        ordre = generateur.ordre
        matelot = ordre.matelot
        differe = self.generateur_enfant
        differe.ordre.volonte = ordre.volonte
        differe.parent = generateur
        matelot.executer_generateur(differe, profondeur + 1)

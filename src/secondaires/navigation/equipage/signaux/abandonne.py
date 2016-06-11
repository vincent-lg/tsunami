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


"""Fichier contenant la classe SignalAbandonner."""

from secondaires.navigation.equipage.signaux.termine import SignalTermine

class SignalAbandonne(SignalTermine):

    """Signal utilisé pour dire que l'ordre ne peut s'exécuter.

    La raison est précisée dans le constructeur. Elle est transmise à tout
    le navire si transmettre est à True.

    """

    def __init__(self, raison, transmettre=False):
        SignalTermine.__init__(self)
        self.raison = raison
        self.transmettre = transmettre

    def __repr__(self):
        return "<signal abandonné {}>".format(repr(self.raison))

    def traiter(self, generateur, profondeur):
        """Traite le générateur."""
        ordre = generateur.ordre
        matelot = ordre.matelot
        matelot.ordres[:] = []
        SignalTermine.traiter(self, generateur, profondeur)
        volonte = ordre.volonte
        personnage = matelot.personnage
        navire = matelot.equipage.navire
        if self.transmettre:
            navire.envoyer("{} s'écrie : {}".format(
                    personnage.distinction_audible, self.raison))

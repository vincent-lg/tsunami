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


"""Fichier contenant la classe SignalRepete."""

from secondaires.navigation.equipage.signaux.base import Signal

class SignalRepete(Signal):

    """Signal utilisé pour répéter le même ordre dans X secondes.

    Ce signal est très utile pour demander à un ordre de boucler
    (c'est-à-dire de s'exécuter régulièrement). C'est souvent utile
    pour des ordres de vérification.

    À la différence d'une simple pause dans l'ordre, ce signal demande
    de reprendre l'ordre du début (techniquement parlant, il ne garde
    pas trace du générateur créé par l'ordre).

    Ce signal prend en paramètre la longueur de la pause, ens econdes,
    avant que l'ordre ne soit répété.

    """

    def __init__(self, pause):
        Signal.__init__(self)
        self.pause = pause

    def __repr__(self):
        return "<signal répété dans {} seconde(s)>".format(self.pause)

    def traiter(self, generateur, profondeur):
        """Traite le générateur."""
        ordre = generateur.ordre
        matelot = ordre.matelot
        nouveau_generateur = ordre.creer_generateur()
        tps = self.pause

        # On ajoute l'action différée
        nom = "ordres_{}".format(id(nouveau_generateur))
        importeur.diffact.ajouter_action(nom, tps,
                matelot.executer_generateur, nouveau_generateur,
                profondeur)

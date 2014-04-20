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


"""Ce fichier définit la classe GuidePar, détaillée plus bas."""

from primaires.perso.templates.etat import Etat

class GuidePar(Etat):

    """Classe représentant l'état guide_par."""

    cle = "guide_par"
    msg_refus = "Vous êtes guidé."
    act_autorisees = ["regarder", "parler", "poser", "ingerer", \
            "lancersort", "geste", "bouger"]
    sauvegarder_au_reboot = True

    def __init__(self, personnage, guide=None, laisse=None):
        """Constructeur de l'état."""
        Etat.__init__(self, personnage)
        self.guide = guide
        self.laisse = laisse

    @property
    def arguments(self):
        return (self.cle, self.guide, self.laisse)

    def message_visible(self):
        """Retourne le message pour les autres."""
        msg = "est guidé{e} ici"
        e = "e" if self.personnage.est_feminin() else ""
        return msg.format(e=e)

    def supprimer(self):
        """L'état se supprime du personnage."""
        if self.guide:
            personnage = self.guide
            if "guide" in personnage.etats:
                personnage.etats.retirer("guide")

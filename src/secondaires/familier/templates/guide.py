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


"""Ce fichier définit la classe Guide, détaillée plus bas."""

from primaires.perso.templates.etat import Etat

class Guide(Etat):

    """Classe représentant l'état guide."""

    cle = "guide"
    msg_refus = "Vous êtes en train de guider un familier."
    act_autorisees = ["regarder", "parler", "poser", "ingerer", \
            "lancersort", "geste", "bouger", "relacherfamilier"]
    sauvegarder_au_reboot = True

    def __init__(self, personnage, familier=None, laisse=None):
        """Constructeur de l'état."""
        Etat.__init__(self, personnage)
        self.familier = familier
        self.laisse = laisse

    @property
    def arguments(self):
        return (self.cle, self.familier, self.laisse)

    def message_visible(self):
        """Retourne le message pour les autres."""
        msg = "guide"
        if self.familier:
            msg += " " + self.familier.pnj.nom_singulier
        msg += " ici"

        return msg

    def supprimer(self):
        """L'état se supprime du personnage."""
        if self.familier and self.familier.pnj:
            pnj = self.familier.pnj
            if "guide_par" in pnj.etats:
                pnj.etats.retirer("guide_par")

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


"""Ce fichier contient l'éditeur EdtSupport, détaillé plus bas."""

from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.uniligne import Uniligne
from primaires.interpreteur.editeur.flottant import Flottant

class EdtSupport(Presentation):

    """Ce contexte permet d'éditer la partie support d'un détail."""

    def __init__(self, pere, detail=None, attribut=None):
        """Constructeur de l'éditeur"""
        Presentation.__init__(self, pere, detail, attribut, False)
        if pere and detail:
            self.construire(detail)

    def construire(self, detail):
        """Construction de l'éditeur"""
        # Peut supporter
        supporter = self.ajouter_choix("peut supporter", "u", Flottant,
                detail, "peut_supporter")
        supporter.parent = self
        supporter.prompt = "Entrez le poids que le détail peut supporter : "
        supporter.aide_courte = \
            "Entrez le |ent|poids que le détail peut supporter|ff| " \
            "ou\n|cmd|/|ff| pour revenir à la fenêtre parente.\n" \
            "Ce poids détermine ce que le détail peut supporter\n" \
            "(ce que vous pouvez y installer en objet de décoration).\n" \
            "Si vous précisez un poids de |cmd|0|ff|, on ne pourra " \
            "rien y installer.\n\nPoids supporté actuel : " \
            "{objet.peut_supporter} kg"

        # Message supporte
        msg_supporte = self.ajouter_choix("message du support", "m",
                Uniligne, detail, "message_supporte")
        msg_supporte.parent = self
        msg_supporte.prompt = "Message du support du détail : "
        msg_supporte.apercu = "{objet.message_supporte}"
        msg_supporte.aide_courte = \
            "Entrez le |ent|message du support|ff| du détail ou " \
            "|cmd|/|ff| pour\nrevenir à la fenêtre parente.\n\nMessage " \
            "actuel : |bc|{objet.message_supporte}|ff|"

        # Message d'installation
        msg_installation = self.ajouter_choix("message d'installation", "i",
                Uniligne, detail, "message_installation")
        msg_installation.parent = self
        msg_installation.prompt = "Message d'installation du détail : "
        msg_installation.apercu = "{objet.message_installation}"
        msg_installation.aide_courte = \
            "Entrez le |ent|message d'installation|ff| du détail ou " \
            "|cmd|/|ff| pour\nrevenir à la fenêtre parente.\n\nVous pouvez " \
            "utiliser |cmd|%objet|ff| qui sera remplacé par le nom de\n" \
            "l'objet et |cmd|%detail|ff| qui sera remplacé par le titre " \
            "du détail.\n\nMessage actuel : " \
            "|bc|{objet.message_installation}|ff|"

        # Message de désinstallation
        msg_desinstallation = self.ajouter_choix("message de " \
                "désinstallation", "d", Uniligne, detail,
                "message_desinstallation")
        msg_desinstallation.parent = self
        msg_desinstallation.prompt = "Message de désinstallation du détail : "
        msg_desinstallation.apercu = "{objet.message_desinstallation}"
        msg_desinstallation.aide_courte = \
            "Entrez le |ent|message de désinstallation|ff| du détail ou " \
            "|cmd|/|ff| pour\nrevenir à la fenêtre parente.\n\nVous pouvez " \
            "utiliser |cmd|%objet|ff| qui sera remplacé par le nom de\n" \
            "l'objet et |cmd|%detail|ff| qui sera remplacé par le titre " \
            "du détail.\n\nMessage actuel : " \
            "|bc|{objet.message_desinstallation}|ff|"

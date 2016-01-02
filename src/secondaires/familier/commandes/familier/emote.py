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
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT master OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant le paramètre 'emote' de la commande 'familier'."""

from primaires.format.constantes import ponctuations_finales
from primaires.format.fonctions import echapper_accolades
from primaires.interpreteur.masque.parametre import Parametre

class PrmEmote(Parametre):

    """Commande 'familier emote'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "emote", "emote")
        self.schema = "<nom_familier> <message>"
        self.aide_courte = "fait agir votre familier"
        self.aide_longue = \
            "Cette commande est identique à la commande %emote% mais " \
            "pour votre familier : elle vous permet de donner un ordre, " \
            "comme si le familier faisait un %emote%. Les mêmes règles " \
            "de RP et de réalisme qui s'appliquent à la commande " \
            "%emote% s'appliquent ici."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        # On récupère le familier et le message
        familier = dic_masques["nom_familier"].familier
        message = dic_masques["message"].message
        pnj = familier.pnj
        message = message.rstrip(" \n")
        pnj.agir("geste")
        if not message[-1] in ponctuations_finales:
            message += "."
        message = echapper_accolades(message)
        personnage << "Vous donnez un ordre à {}.".format(familier.nom)
        personnage.salle.envoyer("{{}} {}".format(message), pnj)

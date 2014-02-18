# -*-coding:Utf-8 -*

# Copyright (c) 2010 LE GOFF Vincent
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


"""Package contenant la commande 'emote'.

"""

from primaires.format.constantes import ponctuations_finales
from primaires.format.fonctions import echapper_accolades

from primaires.interpreteur.commande.commande import Commande

class CmdEmote(Commande):

    """Commande 'emote'.

    """

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "emote", "emote")
        self.nom_categorie = "parler"
        self.schema = "<message>"
        self.aide_courte = "joue une emote dans la salle"
        self.aide_longue = \
            "Cette commande permet de jouer une action RP dans la salle oé " \
            "vous vous trouvez. Tous les personnages présents dans " \
            "la salle vous verront. Par exemple, vous pouvez faire " \
            "|ent|emote sifflote un air mélodieux|ff| ou |ent|emote " \
            "sourit|ff|."

    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande"""
        personnage.agir("geste")
        message = dic_masques["message"].message
        message = message.rstrip(" \n")
        if not message[-1] in ponctuations_finales:
            message += "."
        message = echapper_accolades(message)
        personnage.envoyer("{{}} {}".format(message), personnage)
        personnage.salle.envoyer("{{}} {}".format(message), personnage)
        importeur.communication.rapporter_conversation("emote",
                personnage, message)

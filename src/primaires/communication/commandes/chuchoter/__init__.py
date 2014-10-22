# -*-coding:Utf-8 -*

# Copyright (c) 2011 EILERS Christoff
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


"""Package contenant la commande 'chuchoter'.

"""

from primaires.format.fonctions import echapper_accolades
from primaires.interpreteur.commande.commande import Commande

class CmdChuchoter(Commande):

    """Commande 'chuchoter'.

    """

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "chuchoter", "whisper")
        self.nom_categorie = "parler"
        self.schema = "<message> a/to <personnage_present>"
        self.aide_courte = "chuchote une phrase à un personnage"
        self.aide_longue = \
            "Cette commande permet de parler à un autre joueur ou à un PNJ " \
            "présent dans la même salle. Ce mode de communication est " \
            "RP et soumis aux mêmes règles que la commande %dire%."

    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande"""
        personnage.agir("parler")
        cible = dic_masques["personnage_present"].personnage
        message = dic_masques["message"].message
        message = echapper_accolades(message)
        if personnage is cible:
            personnage << "|att|Hem... Vous parlez tout seul.|ff|"
            return

        if "alcool" in personnage.affections:
            affection = personnage.affections["alcool"]
            message = affection.affection.deformer_message(affection, message)

        personnage.envoyer("Vous chuchotez à {{}} : {}".format(
                message), cible)
        cible.envoyer("{{}} vous chuchote : {}".format(message),
                personnage)
        personnage.salle.envoyer("{} chuchote quelque chose à " \
                "l'oreille de {}.", personnage, cible)
        importeur.communication.rapporter_conversation("chuchoter",
                personnage, message)
        importeur.communication.enregistrer_conversation("chuchoter",
                cible, personnage, message)

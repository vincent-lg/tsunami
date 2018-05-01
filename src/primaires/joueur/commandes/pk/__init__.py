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


"""Package contenant la commande 'pk'"""

from primaires.interpreteur.commande.commande import Commande

class CmdPK(Commande):

    """Commande 'pk'.

    """

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "pk", "pk")
        self.groupe = "joueur"
        self.schema = "<etat>"
        self.aide_courte = "change le flag PK"
        self.aide_longue = \
            "Cette commande est utile pour changer la valeur du flag PK " \
            "(Player Kill). Par défaut, quand votre joueur est créé, " \
            "ce flag est désactivé : cela signifie que les autres " \
            "joueurs ne peuvent pas vous attaquer mais que vous ne " \
            "pouvez pas les attaquer non plus. Si vous souhaitez le " \
            "réactiver, utilisez cette commande, mais vous ne pourrez " \
            "pas le désactiver après. Si ce flag est actif, vous pourrez " \
            "tuer les autres joueurs et eux pourront vous tuer en " \
            "retour, dans les limites RP habituelles. Utilisez " \
            "%pk%|cmd| on|ff| pour activer ce flag et gardez à l'esprit " \
            "que vous ne pourrez pas le désactiver."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        etat = dic_masques["etat"].flag
        if etat:
            if personnage.pk:
                personnage << "|err|Vous avez déjà activé ce flag.|ff|"
            else:
                personnage.pk = True
                personnage << "|att|Vous avez activé le flag PK.\n" \
                    "Vous ne pourrez plus le désactiver pour ce joueur.|ff|"
        else:
            if personnage.pk:
                personnage << "|err|Vous ne pouvez pas désactiver ce flag.|ff|"
            else:
                personnage << "Ce flag est déjà désactivé pour ce joueur."

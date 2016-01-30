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


"""Package contenant le paramètre 'créer' de la commande 'tags'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmCreer(Parametre):

    """Commande 'tags créer'"""

    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "créer", "create")
        self.schema = "<type:cle> <cle>"
        self.aide_courte = "crée un nouveau tag"
        self.aide_longue = \
            "Cette commande permet de créer un nouveau tag. Vous devez " \
            "préciser en premier paramètre le type de tag (comme " \
            "pnj, objet ou autre) et en second paramètre, la clé du " \
            "tag à créer. Par exemple : %tags% %tags:créer%|cmd|pnj " \
            "marchand|ff|. Types de tag disponibles : " + ", ".join(
            importeur.tags.types) + "."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        type = dic_masques["type"].cle
        cle = dic_masques["cle"].cle

        if type not in importeur.tags.types:
            personnage << "|err|Type de tag {} inconnu.|ff|".format(type)
            return

        if cle in importeur.tags.tags:
            personnage << "|err|Cette clé de tag est déjà utilisée.|ff|"
            return

        tag = importeur.tags.creer_tag(cle, type)
        personnage << "Le tag {} de type {} a bien été créé.".format(
                cle, type)

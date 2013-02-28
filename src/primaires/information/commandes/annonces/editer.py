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


"""Fichier contenant le paramètre 'editer' de la commande 'annonces'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmEditer(Parametre):

    """Commande 'annonces editer'.

    """

    def __init__(self):
        """Constructeur du paramètre"""

        Parametre.__init__(self, "editer", "edit")
        self.groupe = "administrateur"
        self.schema = "<nombre> <message>"
        self.aide_courte = "édite une annonce"
        self.aide_longue = \
            "Cette sous-commande prend en paramètre l'id d'une annonce " \
            "ainsi qu'un message, et remplace le contenu de l'annonce en " \
            "question par le message précisé."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""

        id = dic_masques["nombre"].nombre
        modif = dic_masques["message"].message
        annonces = type(self).importeur.information.annonces

        if id > len(annonces):
            personnage << "|err|Aucune annonce ne correspond à l'id " \
                    "spécifiée.|ff|"
        else:
            id -= 1
            annonces[id] = modif
            personnage << "|att|L'annonce a bien été éditée.|ff|"

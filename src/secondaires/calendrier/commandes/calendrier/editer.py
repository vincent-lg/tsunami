# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 AYDIN Ali-Kémal
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

"""Module contenant le paramètre 'editer'de la commande 'calendrier'"""

from primaires.interpreteur.masque.parametre import Parametre

class PrmEditer(Parametre):

    """Commande calendrier editer'"""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "éditer", "edit")
        self.schema = "<nombre>"
        self.aide_courte = "Edite un évènement"
        self.aide_longue = \
            "Cette commande permet d'éditer un évènement. Si l'ID " \
            "entrée est valide, l'évènement correspondant est édité " \
            "au travers d'un éditeur."

    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande"""
        id = dic_masques["nombre"].nombre

        try:
            evenement = type(self).importeur.calendrier.evenements[id]
        except KeyError:
            personnage << "|err|L'ID entrée n'est pas valide|ff|"
        else:
            if personnage not in evenement.responsables:
                personnage << "|err|Vous n'êtes pas responsable de cet évènement.|ff|"
                return

            editeur = importeur.interpreteur.construire_editeur(
                        "evedit", personnage, evenement)
            personnage.contextes.ajouter(editeur)
            editeur.actualiser()

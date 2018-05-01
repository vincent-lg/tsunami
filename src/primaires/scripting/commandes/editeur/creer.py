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


"""Package contenant le paramètre 'créer' de la commande 'éditeur'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmCreer(Parametre):

    """Paramètre 'créer de la commande 'éditeur'."""

    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "créer", "create")
        self.schema = "<cle>"
        self.aide_courte = "crée l'éditeur personnalisé"
        self.aide_longue = \
            "Cette commande permet de créer l'éditeur personnalisé " \
            "lié à une structure. Vous devez passer en paramètre la " \
            "clé de l'éditeur à créer, qui est également la clé " \
            "de la structure liée."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        cle = dic_masques["cle"].cle

        if cle in importeur.scripting.editeurs:
            personnage << "|err|L'éditeur {} existe déjà.|ff|".format(
                    repr(cle))
            return

        editeur = importeur.scripting.creer_editeur(cle)
        editeur = importeur.interpreteur.construire_editeur("editeur",
                personnage, editeur)
        personnage.contextes.ajouter(editeur)
        editeur.actualiser()

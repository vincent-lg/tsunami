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


"""Package contenant le paramètre 'créer' de la commande 'affection'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmCreer(Parametre):

    """Commande 'affection créer'"""

    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "créer", "create")
        self.schema = "<type:cle> <cle>"
        self.aide_courte = "crée une nouvelle affection"
        self.aide_longue = \
            "Cette commande permet de créer une nouvelle affection. " \
            "Vous devez préciser en premier paramètre le type de " \
            "l'affection (soit |cmd|personnage|ff|, soit |cmd|salle|ff|) et " \
            "après la clé de l'affection. Si l'affection peut être " \
            "créée, vous serez redirigé vers l'éditeur d'affection."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        a_type = dic_masques["type"].cle.lower()
        if a_type not in ("personnage", "salle"):
            personnage << "|err|Ce type d'affection {} est " \
                    "invalide.|ff|".format(a_type)
            return

        cle = dic_masques["cle"].cle
        if importeur.affection.affection_existe(a_type, cle):
            personnage << "|err|Une affection de cette clé existe déjà.|ff|"
            return

        affection = importeur.affection.creer_affection(a_type, cle)
        editeur = importeur.interpreteur.construire_editeur("affedit",
                personnage, affection)
        personnage.contextes.ajouter(editeur)
        editeur.actualiser()

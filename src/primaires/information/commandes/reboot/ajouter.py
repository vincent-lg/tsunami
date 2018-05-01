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


"""Fichier contenant le paramètre 'ajouter' de la commande 'reboot'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmAjouter(Parametre):

    """Commande 'reboot ajouter'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "ajouter", "add")
        self.schema = "<texte_libre>"
        self.aide_courte = "ajoute une version différeée"
        self.aide_longue = \
            "Cette sous-commande ajoute une version différée au " \
            "reboot programmé. Vous pouvez utiliser cette commande " \
            "avant avoir programmé le reboot (%reboot%|ent| <minutes>|ff|) " \
            "ou après l'avoir fait. Tant que le MUD n'a pas encore " \
            "rebooté, les versions différées seront correctement " \
            "ajoutées."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        modification = dic_masques["texte_libre"].texte
        importeur.information.get_reboot().versions.append(modification)
        personnage << "Votre version différée a bien été ajoutée."

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


"""Fichier contenant le paramètre 'propriétaire' de la commande 'navire'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmProprietaire(Parametre):

    """Commande 'navire proprietaire'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "propriétaire", "owner")
        self.schema = "<cle_navire> <nom_joueur>"
        self.aide_courte = "change le propriétaire du navire"
        self.aide_longue = \
            "Cette commande permet de changer le propriétaire du navire. " \
            "Vous devez préciser d'abord la clé du navire et ensuite le " \
            "nom du joueur qui deviendra le nouveau propriétaire."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        # On récupère le navire et le propriétaire
        navire = dic_masques["cle_navire"].navire
        proprietaire = dic_masques["nom_joueur"].joueur
        navire.proprietaire = proprietaire
        personnage << "Le propriétaire du navire {} a bien été changé pour " \
                "{}.".format(navire.cle, proprietaire.nom)

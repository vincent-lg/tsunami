# -*-coding:Utf-8 -*

# Copyright (c) 2014 LE GOFF Vincent
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
# * Neither the rename of the copyright holder nor the renames of its contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT master OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant le paramètre 'renommer' de la commande 'familier'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmRenommer(Parametre):

    """Commande 'familier renommer'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "renommer", "rename")
        self.tronquer = True
        self.schema = "<ancien:nom_familier> <nouveau:nom_familier>"
        self.aide_courte = "change le nom d'un familier"
        self.aide_longue = \
            "Cette commande permet de changer le nom d'un familer. Ce " \
            "nom est important, puisqu'il s'agit du nom que vous " \
            "utiliserez pour manipuler le familier, lui donner des " \
            "ordres et celui que vous verrez dans la salle. Ce " \
            "nom doit être unique entre vos familiers, c'est-à-dire que " \
            "deux familiers que vous possédez ne peuvent pas avoir le " \
            "même nom. Précisez en premier paramètre le nom actuel " \
            "du familier et en second paramètre son nouveau nom. Vous " \
            "pouvez utiliser cette commande même si le familier ne " \
            "se trouve pas dans la même salle que vous."

    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        ancien = self.noeud.get_masque("nouveau")
        ancien.proprietes["salle_identique"] = "False"
        nouveau = self.noeud.get_masque("nouveau")
        nouveau.proprietes["nouveau"] = "True"
        nouveau.proprietes["salle_identique"] = "False"

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        familier = dic_masques["ancien"].familier
        ancien_nom = familier.nom
        nouveau_nom = dic_masques["nouveau"].nom_familier.capitalize()
        familier.nom = nouveau_nom
        personnage << "{} s'appelle désormais {}.".format(ancien_nom,
                nouveau_nom)

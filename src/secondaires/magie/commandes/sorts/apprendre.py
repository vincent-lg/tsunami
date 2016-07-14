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


"""Package contenant la commande 'sort apprendre'."""

from primaires.interpreteur.masque.parametre import Parametre
from primaires.format.fonctions import contient

class PrmApprendre(Parametre):

    """Commande 'sort apprendre'.

    """

    def __init__(self):
        """Constructeur de la commande"""
        Parametre.__init__(self, "apprendre", "learn")
        self.groupe = "administrateur"
        self.schema = "<nombre> <cle>"
        self.aide_courte = "apprend un sort"
        self.aide_longue = \
            "Cette commande force l'apprentissage d'un sort. " \
            "Vous devez préciser en premier paramètre le nombre " \
            "auquel vous voulez apprendre le sort et, en second " \
            "paramètre, la clé du sort. Précisez un nombre de |cmd|0|ff| " \
            "pour oublier le sort."

    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        nombre = self.noeud.get_masque("nombre")
        nombre.proprietes["limite_inf"] = "0"
        nombre.proprietes["limite_sup"] = "100"

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        niveau = dic_masques["nombre"].nombre
        if niveau < 0 or niveau > 100:
            personnage << "|err|Spécifiez un niveau de maîtrise entre 0 et " \
                    "100.|ff|"
            return

        cle = dic_masques["cle"].cle
        try:
            sort = importeur.magie.sorts[cle]
        except KeyError:
            personnage << "|err|Le sort '{}' est " \
                    "introuvable.|ff|".format(cle)
        else:
            if niveau > 0:
                personnage.sorts[cle] = niveau
                personnage << "Vous avez bien appris le sort {} à " \
                        "{}%.".format(sort.nom, niveau)
            else:
                if cle in personnage.sorts:
                    del personnage.sorts[cle]
                    personnage << "Vous avez bien oublié le sort {}.".format(
                            sort.nom)
                else:
                    personnage << "|err|Vous ne connaissez pas ce sort.|ff|"

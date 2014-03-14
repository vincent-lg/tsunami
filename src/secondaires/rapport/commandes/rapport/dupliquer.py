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


"""Package contenant le paramètre 'dupliquer' de la commande 'rapport'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmDupliquer(Parametre):

    """Commande 'rapport dupliquer'"""

    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "dupliquer", "duplicate")
        self.nom_groupe = "administrateur"
        self.schema = "<nombre> <depuis:nombre>"
        self.aide_courte = "marque un rapport comme dupliqué"
        self.aide_longue = \
            "Cette commande est un raccourci pour indiquer qu'un rapport " \
            "est une duplication d'un autre rapport. Il attend deux " \
            "numéros de rapport : le premier est le rapport dupliqué (à " \
            "fermer), le second est le rapport depuis lequel il est " \
            "dupliqué. Si on veut noter par exemple que le rapport " \
            "|ent|100|ff| est une copie du rapport |ent|56|ff|, on entre " \
            "%rapport% %rapport:dupliquer%|cmd| 100 56|ff|. Il est plus " \
            "courant de laisser les rapports anciens ouverts et de " \
            "dupliquer les nouveaux, ce qui fait que le premier nombre " \
            "est souvent plus élevé que le second, pour mémoire."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        id = dic_masques["nombre"].nombre
        depuis = dic_masques["depuis"].nombre
        try:
            rapport = importeur.rapport.rapports[id]
        except KeyError:
            personnage << "|err|Le rapport {} n'existe pas.|ff|".format(id)
            return

        try:
            depuis = importeur.rapport.rapports[depuis]
        except KeyError:
            personnage << "|err|Le rapport {} n'existe pas.|ff|".format(depuis)
            return

        if not rapport.ouvert:
            personnage << "|err|Le rapport {} est déjà fermé.|ff|".format(id)
            return

        rapport.description.ajouter_paragraphe(
                "|att|Ce rapport est une duplication du rapport " \
                "{}.|ff|".format(depuis.id))
        rapport.statut = "dupliqué"
        personnage << "Le rapport #{} est noté comme dupliqué de #{}.".format(
                rapport.id, depuis.id)

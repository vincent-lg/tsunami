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
# ARE DISCLAIMED. IN NO Etags SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant le paramètre 'liste' de la commande 'tags'."""

from primaires.format.tableau import Tableau, DROITE
from primaires.interpreteur.masque.parametre import Parametre

class PrmListe(Parametre):

    """Commande 'tags liste'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "liste", "list")
        self.aide_courte = "liste les tags existants"
        self.aide_longue = \
            "Cette commande liste les tags existants, groupés par "\
            "type. La première colonne est le type de tag. La seconde " \
            "est sa clé. La troisième est le nombre de lignes " \
            "scripting définies dans ce tag."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        tags = tuple(importeur.tags.tags.values())
        groupes = {}
        for tag in tags:
            if tag.type not in groupes:
                groupes[tag.type] = []

            groupe = groupes[tag.type]
            groupe.append(tag)
            groupe.sort(key=lambda t: t.cle)

        if len(tags) == 0:
            personnage << "|att|Aucun tag défini.|ff|"
            return

        tableau = Tableau("Tags définis")
        tableau.ajouter_colonne("Type")
        tableau.ajouter_colonne("Clé")
        tableau.ajouter_colonne("Lignes", DROITE)

        for cle, groupe in sorted(groupes.items()):
            for tag in groupe:
                nb_lignes = sum(e.nb_lignes for e in \
                        tag.script.evenements.values())
                tableau.ajouter_ligne(tag.type, tag.cle, nb_lignes)

        personnage << tableau.afficher()

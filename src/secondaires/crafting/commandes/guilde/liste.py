# -*-coding:Utf-8 -*

# Copyright (c) 2015 LE GOFF Vincent
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
# ARE DISCLAIMED. IN NO Eguilde SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant le paramètre 'liste' de la commande 'guilde'."""

from primaires.format.tableau import Tableau, DROITE
from primaires.interpreteur.masque.parametre import Parametre

class PrmListe(Parametre):

    """Commande 'guilde liste'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "liste", "list")
        self.aide_courte = "liste les guildes existantes"
        self.aide_longue = \
            "Cette commande liste les guildes existantes. Le tableau " \
            "retourne la clé de la guilde, son nom, son nombre " \
            "d'ateliers actuels et son nombre de membres."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        guildes = tuple(importeur.crafting.guildes.values())
        guildes = sorted([g for g in guildes], key=lambda g: g.cle)

        if len(guildes) == 0:
            personnage << "|att|Aucune guilde définie.|ff|"
            return

        tableau = Tableau()
        tableau.ajouter_colonne("Clé")
        tableau.ajouter_colonne("Nom")
        tableau.ajouter_colonne("Ateliers", DROITE)
        tableau.ajouter_colonne("Membres", DROITE)

        for guilde in guildes:
            tableau.ajouter_ligne(guilde.cle, guilde.nom,
                    len(guilde.ateliers), len(guilde.membres))

        personnage << tableau.afficher()

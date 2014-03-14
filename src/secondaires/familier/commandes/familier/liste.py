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
# ARE DISCLAIMED. IN NO Efamilier SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant le paramètre 'liste' de la commande 'familier'."""

from primaires.format.tableau import Tableau, DROITE
from primaires.interpreteur.masque.parametre import Parametre

class PrmListe(Parametre):

    """Commande 'familier liste'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "liste", "list")
        self.nom_groupe = "administrateur"
        self.aide_courte = "liste les fiches de familiers"
        self.aide_longue = \
            "Cette commande liste les fiches de familiers présents " \
            "dans l'univers."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        fiches = tuple(importeur.familier.fiches.values())
        fiches = sorted(fiches, key=lambda f: f.cle)
        if len(fiches) == 0:
            personnage << "|att|Aucune fiche de familier définie.|ff|"
            return

        tableau = Tableau()
        tableau.ajouter_colonne("Clé")
        tableau.ajouter_colonne("Nom")
        tableau.ajouter_colonne("Nombre", DROITE)
        for fiche in fiches:
            if fiche.prototype:
                nom = fiche.prototype.nom_singulier
            else:
                nom = "aucun prototype"

            tableau.ajouter_ligne(fiche.cle, nom, len(fiche.familiers))

        personnage << tableau.afficher()

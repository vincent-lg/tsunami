# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 LE GOFF Vincent
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   mine of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this mine of conditions and the following disclaimer in the documentation
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


"""Fichier contenant le paramètre 'miens' de la commande 'familier'."""

from primaires.format.tableau import Tableau, DROITE
from primaires.interpreteur.masque.parametre import Parametre

class PrmMiens(Parametre):

    """Commande 'familier miens'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "miens", "mine")
        self.tronquer = True
        self.aide_courte = "affiche vos familiers"
        self.aide_longue = \
            "Cette commande affiche la liste de vos familiers et " \
            "donne un aperçu du lieu où ils se trouvent, ainsi que " \
            "de leur condition (faim et soif)."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        familiers = importeur.familier.familiers_de(personnage)
        familiers = sorted(familiers, key=lambda familier: familier.nom)
        if len(familiers) == 0:
            personnage << "Vous ne possédez aucun familier."
            return

        tableau = Tableau()
        tableau.ajouter_colonne("Nom")
        tableau.ajouter_colonne("Lieu")
        tableau.ajouter_colonne("Faim")
        tableau.ajouter_colonne("Soif")
        for familier in familiers:
            tableau.ajouter_ligne(familier.nom, familier.titre_salle,
                    familier.str_faim, familier.str_soif)

        personnage << tableau.afficher()

# -*-coding:Utf-8 -*

# Copyright (c) 2013 LE GOFF Vincent
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
# ARE DISCLAIMED. IN NO Ematelot SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant le paramètre 'liste' de la commande 'matelot'."""

from primaires.format.fonctions import supprimer_accents
from primaires.format.tableau import Tableau
from primaires.interpreteur.masque.parametre import Parametre
from secondaires.navigation.equipage.postes.hierarchie import ORDRE

class PrmListe(Parametre):

    """Commande 'matelot liste'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "liste", "list")
        self.tronquer = True
        self.aide_courte = "liste les matelots de l'équipage"
        self.aide_longue = \
            "Cette commande liste les matelots de votre équipage. " \
            "Elle permet d'obtenir rapidement des informations pratiques " \
            "sur le nom du matelot ainsi que l'endroit où il se trouve."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        salle = personnage.salle
        if not hasattr(salle, "navire"):
            personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
            return

        navire = salle.navire
        equipage = navire.equipage
        if not navire.a_le_droit(personnage, "officier"):
            personnage << "|err|Vous ne pouvez donner d'ordre sur ce " \
                    "navire.|ff|"
            return

        matelots = tuple((m, m.nom_poste) for m in \
                equipage.matelots.values())
        matelots += tuple(equipage.joueurs.items())
        matelots = sorted(matelots, \
                key=lambda couple: ORDRE.index(couple[1]), reverse=True)
        if len(matelots) == 0:
            personnage << "|err|Votre équipage ne comprend aucun matelot.|ff|"
            return

        tableau = Tableau()
        tableau.ajouter_colonne("Nom")
        tableau.ajouter_colonne("Poste")
        tableau.ajouter_colonne("Affectation")
        for matelot, nom_poste in matelots:
            nom = matelot.nom
            nom_poste = nom_poste.capitalize()
            titre = "Aucune"
            if hasattr(matelot, "personnage"):
                titre = matelot.personnage.salle.titre_court.capitalize()

            tableau.ajouter_ligne(nom, nom_poste, titre)

        personnage << tableau.afficher()

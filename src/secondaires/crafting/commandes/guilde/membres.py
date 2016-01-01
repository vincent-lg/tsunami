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


"""Fichier contenant le paramètre 'membres' de la commande 'guilde'."""

from primaires.format.tableau import Tableau, DROITE
from primaires.interpreteur.masque.parametre import Parametre

class PrmMembres(Parametre):

    """Commande 'guilde membres'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "membres", "members")
        self.tronquer = True
        self.schema = "<cle>"
        self.aide_courte = "affiche les membres d'une guilde"
        self.aide_longue = \
                "Cette commande vous permet de consulter la liste " \
                "des membres d'une guilde, de connaître leur rang " \
                "et leur avancement en pourcentage. Seuls les joueurs " \
                "sont affichés dans ce tableau, les PNJ ne sont pas " \
                "présents."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        cle = dic_masques["cle"].cle
        if cle not in importeur.crafting.guildes:
            personnage << "|err|La guilde {} n'existe " \
                    "pas.|ff|".format(cle)
            return

        guilde = importeur.crafting.guildes[cle]
        membres = []
        for rang in guilde.rangs:
            membres_du_rang = []
            progressions = [p for p in guilde.membres.values()
                    if p.rang is rang and not hasattr(p.membre,
                    "prototype")]
            for progression in progressions:
                membres_du_rang.append((progression.membre.nom, rang.nom,
                        progression.progression))
            
            membres_du_rang.sort(key=lambda c: c[2])
            membres.extend(membres_du_rang)
        
        tableau = Tableau()
        tableau.ajouter_colonne("Nom")
        tableau.ajouter_colonne("Rang")
        tableau.ajouter_colonne("Avancement", DROITE)
        for nom, rang, avancement in membres:
            tableau.ajouter_ligne(nom, rang, "{}%".format(avancement))
        
        personnage << tableau.afficher()

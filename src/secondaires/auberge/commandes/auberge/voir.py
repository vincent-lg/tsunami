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


"""Fichier contenant le paramètre 'voir' de la commande 'auberge'."""

from primaires.format.tableau import Tableau, DROITE
from primaires.interpreteur.masque.parametre import Parametre

class PrmVoir(Parametre):

    """Commande 'auberge voir'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "voir", "view")
        self.schema = "<cle>"
        self.aide_courte = "affiche le détail d'une auberge"
        self.aide_longue = \
                "Cette commande permet d'obtenir plus de détail sur " \
                "une auberge dont la clé est précisée en paramètre. " \
                "Par exemple : %auberge% %auberge:voir%|ent| " \
                "CLEDELAUBERGE|ff|."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        cle = dic_masques["cle"].cle
        if cle not in importeur.auberge.auberges:
            personnage << "|err|L'auberge {} n'existe pas.|ff|".format(cle)
            return

        auberge = importeur.auberge.auberges[cle]

        # Créqation du tableau
        msg = "Informations sur l'auberge {} :".format(auberge.cle)
        msg += "\n  Nom : {}".format(auberge.titre)
        msg += "\n  Comptoir : {}".format(auberge.comptoir)
        msg += "\n  Aubergiste : {}".format(auberge.cle_aubergiste)
        if auberge.aubergiste:
            msg += " (présent)"
        else:
            msg += " |att|(absent)|ff|"
        msg += "\n  Nombre de chambres : {} ({} salles)".format(
                len(auberge.chambres), len(auberge.salles))
        msg += "\n  Pourcentage d'occupation : {}%".format(
                auberge.pct_occupation)

        # Tableau des chambres
        tableau = Tableau("Chambres de l'auberge")
        tableau.ajouter_colonne("Numéro")
        tableau.ajouter_colonne("Salle")
        tableau.ajouter_colonne("Prix", DROITE)
        tableau.ajouter_colonne("Propriétaire")
        tableau.ajouter_colonne("Expire")
        chambres = sorted(list(auberge.chambres.values()),
                key=lambda c: c.numero)
        for chambre in chambres:
            numero = chambre.numero
            salle = chambre.salle
            prix = chambre.prix_par_jour
            if chambre.proprietaire:
                proprietaire = chambre.proprietaire.nom
                date = chambre.expire_a
                annee = date.year
                mois = date.month
                jour = date.day
                heure = date.hour
                minute = date.minute
                expire = "{}-{:>02}-{:>02} {:>02}:{:>02}".format(
                        annee, mois, jour, heure, minute)
            else:
                proprietaire = "Aucun"
                expire = ""

            tableau.ajouter_ligne(numero, salle, prix, proprietaire, expire)

        msg += "\n\n" + tableau.afficher()
        personnage << msg

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
from primaires.interpreteur.masque.parametre import Parametre

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
            personnage << "|err|Vous n'êtes pas sur un navire."
            return

        navire = salle.navire
        equipage = navire.equipage
        if navire.proprietaire and navire.proprietaire is not personnage and \
                not personnage.est_immortel():
            personnage << "|err|Vous ne pouvez donner d'ordre sur ce " \
                    "navire.|ff|"
            return

        matelots = tuple(equipage.matelots.values())
        matelots = sorted(matelots, \
                key=lambda m: supprimer_accents(m.nom).lower())
        if len(matelots) == 0:
            personnage << "|err|Votre équipage ne comprend aucun matelot.|ff|"
            return

        taille_nom = 12
        taille_poste = 20
        taille_salle = 30
        cadre = "+-" + taille_nom * "-" + "-+-" + taille_poste * "-" + \
                "-+-" + taille_salle * "-" + "-+"
        lignes = [
            cadre,
            "| {} | {} | {} |".format("Nom".ljust(taille_nom),
                    "Poste".ljust(taille_poste),
                    "Affectation".format(taille_salle)),
            cadre,
        ]
        for matelot in matelots:
            nom = matelot.nom.ljust(taille_nom)
            nom_poste = matelot.nom_poste.capitalize()
            if len(nom_poste) > taille_poste:
                nom_poste = nom_poste[:taille_poste - 3] + "..."
            else:
                nom_poste = nom_poste.ljust(taille_poste)
            titre_salle = matelot.personnage.salle.titre_court.capitalize()
            if len(titre_salle) > taille_salle:
                titre_salle = titre_salle[:taille_salle - 3] + "..."
            else:
                titre_salle = titre_salle.ljust(taille_salle)
            lignes.append("| {} | {} | {} |".format(nom, nom_poste,
                        titre_salle))
        lignes.append(cadre)

        personnage << "\n".join(lignes)

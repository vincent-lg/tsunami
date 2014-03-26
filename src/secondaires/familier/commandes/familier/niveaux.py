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
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT master OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant le paramètre 'niveaux' de la commande 'familier'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmNiveaux(Parametre):

    """Commande 'familier niveaux'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "niveaux", "levels")
        self.tronquer = True
        self.schema = "<nom_familier>"
        self.aide_courte = "affiche les niveaux du familier"
        self.aide_longue = \
            "Cette commande affiche les niveaux et expériences du " \
            "familier (niveau principal et niveaux secondaires)."

    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        familier = self.noeud.get_masque("nom_familier")
        familier.proprietes["salle_identique"] = "False"

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        # On récupère le familier
        familier = dic_masques["nom_familier"].familier
        fiche = familier.fiche
        pnj = familier.pnj
        grille = [(0, 1)] + list(importeur.perso.gen_niveaux.grille_xp)
        xp = pnj.xp
        niveau = pnj.niveau
        xp_total = grille[niveau][1]
        pourcentage = int(xp / xp_total * 100)
        msg = \
            "+-----------------+-----+-------------------+------+\n" \
            "| {:<15} | {:>3} | {:>8}/{:>8} | {:>3}% |\n".format(
            "Principal", niveau, xp, xp_total, pourcentage)

        niveaux = sorted([(cle, nb) for cle, nb in pnj.niveaux.items()],
                key=lambda e: e[1], reverse=True)
        for cle, nb in niveaux:
            nom = importeur.perso.niveaux[cle].nom.capitalize()
            xp = pnj.xps[cle]
            niveau = pnj.niveaux[cle]
            if niveau == 0:
                continue

            xp_total = grille[niveau][1]
            pourcentage = int(xp / xp_total * 100)
            msg += \
                    "\n| {:<15} | {:>3} | {:>8}/{:>8} | {:>3}% |\n".format(
                    nom, niveau, xp, xp_total, pourcentage)

        msg += \
            "\n+-----------------+-----+-------------------+------+"
        personnage << msg

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
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Package contenant la commande 'scruter'.

"""

from random import random

from primaires.interpreteur.commande.commande import Commande

class CmdScruter(Commande):

    """Commande 'scruter'.

    """

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "scruter", "scan")
        self.nom_categorie = "combat"
        self.aide_courte = "cherche les personnages alentours"
        self.aide_longue = \
            "Cette commande vous fait scruter les alentours à la " \
            "recherche de personnages."

    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande"""
        personnage.agir("regarder")
        salle = personnage.salle
        rayon = 2 + round(personnage.stats.sensibilite / 40)
        chemins = salle.trouver_chemins_droits(rayon)
        chemins = [c for c in chemins if all(not s.cachee for s in c.sorties)]
        chemins = sorted(chemins, key=lambda chemin: chemin.longueur)
        savoir = personnage.pratiquer_talent("scruter", 10)

        personnage << "Vous regardez autour de vous."
        personnage.etats.ajouter("scruter")
        yield 2
        if "scruter" not in personnage.etats:
            return

        personnage.etats.retirer("scruter")

        # 0.25 <= sens < 0.92
        sens = 0.25 + personnage.stats.sensibilite / 300 + savoir / 300
        cibles = []
        for chemin in chemins:
            if chemin.destination.a_flag("invisible à distance"):
                continue

            tmp_sens = sens - (chemin.longueur - 1) * 0.04
            for autre in chemin.destination.personnages:
                if not autre.super_invisible and random() < tmp_sens:
                    cibles.append((chemin, autre))
                    personnage.pratiquer_talent("scruter", 5)

        if cibles:
            importeur.combat.cibles[personnage] = cibles
            lignes = []
            for i, (chemin, cible) in enumerate(cibles):
                sortie = chemin.sorties[0].nom_complet
                lignes.append("  {:>2}  {:<20} vers {}".format(
                        i + 1, cible.get_nom_pour(personnage), sortie))

            personnage << "Vous voyez autour de vous :\n\n" + "\n".join(lignes)
        else:
            personnage << "Vous ne voyez personne autour de vous."

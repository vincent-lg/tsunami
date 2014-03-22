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
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Package contenant la commande 'apprivoiser'."""

from random import randint

from primaires.interpreteur.commande.commande import Commande

class CmdApprivoiser(Commande):

    """Commande 'apprivoiser'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "apprivoiser", "tame")
        self.nom_categorie = "familier"
        self.schema = "<personnage_present>"
        self.aide_courte = "apprivoise un familier"
        self.aide_longue = \
            "Cette commande permet d'apprivoiser un familier. Elle attend " \
            "en paramètre un fragment du nom du familier (un personnage " \
            "présent dans la même salle que vous). Cette commande se " \
            "base sur votre charisme et votre talent d'apprivoisement : " \
            "certains familiers sont plus difficiles à apprivoiser que " \
            "d'autres, et certains peuvent avoir des réactions violentes " \
            "si vous n'arrivez pas à les apprivoiser."

    def peut_executer(self, personnage):
        """On ne eut exécuter la commande si on a pas apprivoisement."""
        return "apprivoisement" in personnage.talents

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        salle = personnage.salle
        pnj = dic_masques["personnage_present"].personnage

        cle = getattr(pnj, "cle")
        identifiant = getattr(pnj, "identifiant", "")

        # On vérifie que le PNJ peut être, potentiellement, un familier
        try:
            fiche = importeur.familier.fiches[cle]
        except KeyError:
            personnage.envoyer("|err|{} ne peut être apprivoisé.|ff|", pnj)
            return

        # On vérifie que le PNJ n'est pas déjà un familier apprivoisé
        try:
            familier = importeur.familier.familiers[identifiant]
        except KeyError:
            pass
        else:
            personnage.envoyer("|err|{} a déjà été apprivoisé.|ff|", pnj)
            return

        if len(importeur.familier.familiers_de(personnage)) > 4:
            personnage << "|err|Vous ne pouvez apprivoiser un familier de " \
                    "plus.|ff|"
            return

        # On essaye d'apprivoiser le familier
        min_appr = personnage.talents.get("apprivoisement", 1)
        max_appr = min_appr + int(personnage.stats.charisme / 2)
        appr = max_appr
        if min_appr != max_appr:
            appr = randint(min_appr, max_appr)

        min_diff = fiche.difficulte_apprivoisement
        max_diff = min_diff + int(min_diff * 0.5)
        diff = max_diff
        if min_diff != max_diff:
            diff = randint(min_diff, max_diff)

        personnage.envoyer("Vous prononcez quelques paroles douces et " \
                "tentez d'apprivoiser {}.", pnj)

        if fiche.difficulte_apprivoisement <= 100 and appr >= diff:
            familier = importeur.familier.creer_familier(pnj)
            familier.maitre = personnage
            familier.trouver_nom()
            personnage.envoyer("Vous parvenez à apprivoiser {}.", pnj)
            personnage.salle.envoyer("{} prononce quelques paroles douces " \
                    "et s'approche de {}.", personnage, pnj)
            fiche.script["apprivoiser"]["réussir"].executer(familier=pnj,
                    personnage=personnage)
        else:
            personnage.envoyer("Vous n'arrivez de toute évidence pas à " \
                    "apprivoiser {}", pnj)
            fiche.script["apprivoiser"]["echoue"].executer(familier=pnj,
                    personnage=personnage)

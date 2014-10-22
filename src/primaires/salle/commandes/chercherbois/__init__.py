# -*-coding:Utf-8 -*

# Copyright (c) 2012 NOEL-BARON Léo
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


"""Package contenant la commande 'chercherbois'."""

from random import random, randint, choice
from math import sqrt

from primaires.interpreteur.commande.commande import Commande
from primaires.perso.exceptions.stat import DepassementStat

class CmdChercherBois(Commande):

    """Commande 'chercherbois'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "chercherbois", "gatherwood")
        self.nom_categorie = "objets"
        self.aide_courte = "permet de chercher du bois"
        self.aide_longue = \
            "Cette commande permet de chercher du combustible dans la salle " \
            "où vous vous trouvez."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        salle = personnage.salle
        if salle.interieur:
            personnage << "|err|Vous ne pouvez chercher du combustible " \
                    "ici.|ff|"
            return

        personnage.agir("chercherbois")
        prototypes = importeur.objet.prototypes.values()
        prototypes = [p for p in prototypes if p.est_de_type("combustible")]
        combustibles = []
        choix = None
        for proto in prototypes:
            if personnage.salle.terrain.nom in proto.terrains:
                combustibles.append((proto.rarete, proto))
        combustibles = sorted(combustibles, key=lambda combu: combu[0])
        if not combustibles:
            personnage << "|err|Il n'y a rien qui puisse brûler par ici.|ff|"
        else:
            niveau = sqrt(personnage.get_talent("collecte_bois") / 100)
            if not niveau:
                niveau = 0.1
            proba_trouver = round(random(), 1)
            if proba_trouver <= niveau: # on trouve du bois
                possibles = []
                for proba, combustible in combustibles:
                    if 2 * proba_trouver >= (proba - 1) / 10:
                        for i in range(int(10 / proba)):
                            possibles.append(combustible)
                nb_obj = randint(int(proba_trouver * 10), int(niveau * 10)) + 1
                if possibles:
                    choix = choice(possibles)
                    somme_qualites = 0
                    end = int(choix.poids_unitaire * nb_obj / 2)
                    try:
                        personnage.stats.endurance -= end
                    except DepassementStat:
                        personnage << "|err|Vous êtes trop fatigué pour " \
                                "cela.|ff|"
                        return
            try:
                personnage.stats.endurance -= 3
            except DepassementStat:
                personnage << "|err|Vous êtes trop fatigué pour cela.|ff|"
                return
            # On cherche le bois
            personnage.etats.ajouter("collecte_bois")
            personnage << "Vous vous penchez et commencez à chercher du bois."
            personnage.salle.envoyer(
                    "{} se met à chercher quelque chose par terre.",
                    personnage)
            yield 5
            if "collecte_bois" not in personnage.etats:
                return

            if choix:
                for i in range(nb_obj):
                    objet = importeur.objet.creer_objet(choix)
                    personnage.salle.objets_sol.ajouter(objet)
                    somme_qualites += objet.qualite
                personnage << "Vous trouvez {} " \
                        "et vous relevez.".format(choix.get_nom(nb_obj))
                personnage.salle.envoyer("{} se relève, l'air satisfait.",
                        personnage)
                personnage.pratiquer_talent("collecte_bois")
                personnage.gagner_xp("survie", somme_qualites * 2)
            else:
                personnage << "Vous vous redressez sans avoir rien trouvé."
                personnage.salle.envoyer("{} se relève, l'air dépité.",
                        personnage)
                personnage.pratiquer_talent("collecte_bois", 4)

            personnage.etats.retirer("collecte_bois")

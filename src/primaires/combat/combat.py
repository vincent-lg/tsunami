# -*-coding:Utf-8 -*

# Copyright (c) 2011 LE GOFF Vincent
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


"""Fichier contenant la classe Combat, détaillée plus bas."""

from random import choice, randint

from corps.aleatoire import varier, chance_sur
from primaires.perso.exceptions.stat import DepassementStat
from .attaque import Coup

# Constantes
CLE_TALENT_ESQUIVE = "esquive"
CLE_TALENT_PARADE = "parade"
CLE_TALENT_MAINS_NUES = "combat_mains_nues"
ARMES_PARADE = ["épée", "hache", "masse"]

class Combat:

    """Classe représentant un combat dans une salle.

    Un combat est constitué :
        combattants -- D'une liste de combattants
        combattus -- d'un dictionnaire combattant: combattu

    A chaque tour (appelle à la méthode tour), les combattants combattent
    selon des règles définies dans ce module. Voir la méthode 'tour'
    pour plus d'informations.

    """

    enregistrer = True
    def __init__(self, salle):
        """Constructeur d'un combat."""
        self.salle = salle
        self.__combattants = []
        self.__combattus = {}

    @property
    def combattants(self):
        """Retourne une liste déréférencée des combattants."""
        return list(self.__combattants)

    @property
    def combattus(self):
        """Retourne un dictionnaire déréférencé des combattus."""
        return dict(self.__combattus)

    def ajouter_combattants(self, combattant, combattu):
        """Ajoute les combattants."""
        combattant.selectionner_prompt("combat")
        combattu.selectionner_prompt("combat")
        if combattant not in self.__combattants:
            self.__combattants.append(combattant)
            self.__combattus[combattant] = combattu

        if combattu not in self.__combattants:
            self.__combattants.append(combattu)
            self.__combattus[combattu] = combattant

    def supprimer_combattant(self, combattant):
        """Supprime le personnage des combattants / combattus."""
        combattant.deselectionner_prompt("combat")
        if combattant in self.__combattants:
            self.__combattants.remove(combattant)

        if combattant in self.__combattus.keys():
            del self.__combattus[combattant]

        cles = [cle for cle, valeur in self.__combattus.items() if \
                valeur is combattant]
        for cle in cles:
            self.__combattus[cle] = None

        self.verifier_combattants()

    def verifier_combattants(self):
        """Vérifie que tous les combattants sont bien dans la salle."""
        for combattant in list(self.combattants):
            if combattant is None or combattant.salle is not self.salle or \
                    combattant.est_mort():
                self.__combattants.remove(combattant)
                if combattant:
                    combattant.deselectionner_prompt("combat")

        for combattant, combattu in list(self.combattus.items()):
            if combattant and combattant.salle is not self.salle:
                del self.__combattus[combattant]
            elif combattu and combattu.salle is not self.salle:
                self.__combattus[combattant] = None

        # Les combattants ne combattant personne essayent de trouver une
        # autre cible
        for combattant, combattu in self.combattus.items():
            if combattu is None:
                # On liste les cibles possibles du combattant
                # (ceux qui le combattent)
                cibles = [cbt for cbt, cbu in self.combattus.items() if \
                        cbu is combattant]
                if cibles:
                    cible = choice(cibles)
                    self.__combattus[combattant] = cible
                else:
                    combattant.etats.retirer("combat")
                    del self.__combattus[combattant]
                    combattant.deselectionner_prompt("combat")

        # On reforme la liste des combattants
        self.__combattants = [p for p in self.__combattus.keys()]
        self.__combattants += [p for p in self.__combattus.values() if \
                p not in self.__combattants]

    def get_attaques(self, personnage):
        """Retourne les attaques du personnage."""
        return (Coup(personnage), )

    def defendre(self, combattant, combattu, attaque, membre, degats, arme):
        """combattu tente de se défendre.

        Retourne les dégâts finalement infligés.

        Si la défense est totale, retourne 0.

        """
        armes_def = combattu.get_armes()
        poids_combattant = combattant.poids / combattant.poids_max
        poids_combattu = combattu.poids / combattu.poids_max
        diff = (poids_combattant - poids_combattu) * 30
        # esquive
        if varier(combattu.pratiquer_talent(CLE_TALENT_ESQUIVE), 15) + diff >= \
                varier(90, 10):
            attaque.envoyer_msg_tentative(combattant, combattu, membre, arme)
            combattant.envoyer("{} esquive votre coup.", combattu)
            combattu.envoyer("Vous esquivez le coup porté par {}.",
                    combattant)
            combattant.salle.envoyer("{} esquive le coup porté par {}.",
                    combattu, combattant)
            return 0
        # parade
        armes_parade = [a for a in armes_def if a.nom_type in ARMES_PARADE]
        if len(armes_parade) > 0:
            # Les chances maximum (avec tous les talents concernés à 100%)
            # de parade dépendent du nombre d'armes pouvant parer et du talent
            # de l'attaquant au maniement de son arme.
            chances_max = 40
            if arme:
                chances_max -= \
                        15 * 0.01 * combattant.get_talent(arme.cle_talent)
            chances_max = chances_max * (1 + 0.4 * (len(armes_parade) -1)) \
                    / len(armes_parade)
            talent_parade = 0.01 * combattu.pratiquer_talent(CLE_TALENT_PARADE)
            for arme_parade in armes_parade:
                talent_arme = 0.01 * combattu.get_talent(arme_parade.cle_talent)
                if chance_sur(chances_max * talent_parade * talent_arme):
                    attaque.envoyer_msg_tentative(combattant, combattu, membre,
                            arme)
                    combattant.envoyer()(
                            "{} pare votre coup avec {}.",
                            combattu, arme_parade)
                    combattu.envoyer(
                            "Vous parez le coup porté par {} avec {}.",
                            combattant, arme_parade)
                    combattant.salle.envoyer(
                            "{} pare le coup porté par {}.",
                            combattu, combattant)
                    return 0
        # infliger le coup s'il a porté
        if membre:
            objets = len(membre.equipe) and membre.equipe or []
            for objet in objets:
                if objet and objet.est_de_type("armure"):
                    encaisse = objet.encaisser(combattu, arme, degats)
                    degats -= encaisse

        return degats

    def tour(self, importeur):
        """Un tour de combat."""
        self.verifier_combattants()
        if not self.combattants:
            importeur.combat.supprimer_combat(self.salle.ident)
            return

        for combattant, combattu in self.combattus.items():
            if combattant.est_mort():
                continue

            membre = None
            armes = combattant.get_armes()
            armes = armes if armes else [None]
            for arme in armes:
                if combattu is None or combattu.est_mort():
                    continue

                attaques = self.get_attaques(combattant)
                attaque = choice(attaques)
                membre = attaque.get_membre(combattant, combattu, arme)
                if attaque.essayer(combattant, combattu, arme):
                    degats = attaque.calculer_degats(combattant, combattu,
                            membre, arme)

                    # Défense
                    degats = self.defendre(combattant, combattu, attaque,
                            membre, degats, arme)
                    if degats:
                        attaque.envoyer_msg_reussite(combattant, combattu,
                                membre, degats, arme)

                        try:
                            combattu.vitalite -= degats
                        except DepassementStat:
                            combattu.envoyer("|att|C'en est trop ! Vous " \
                                    "plongez dans l'inconscience.|ff|")
                            combattu.salle.envoyer("{} s'écroule sur le sol, " \
                                    "baignant dans son sang.", combattu)
                            combattant.tuer(combattu)
                            combattu.mourir(adversaire=combattant)
                else:
                    attaque.envoyer_msg_tentative(combattant, combattu,
                            membre, arme)

        self.verifier_combattants()
        importeur.diffact.ajouter_action(
            "combat:{}".format(self.salle.ident), 3, self.tour, importeur)

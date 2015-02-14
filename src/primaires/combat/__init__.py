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


"""Fichier contenant le module secondaire combat."""

from abstraits.module import *
from . import commandes
from . import types
from .combat import *
from .prompt import PromptCombat
from .types.arme import Arme

class Module(BaseModule):

    """Module gérant le combat rapproché.

    Ce module gère le combat rapproché et les extensions nécessaires aux
    personnages et PNJ. Il gère également les talents et niveaux liés
    ainsi, naturellement, que les commandes.

    """

    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "combat", "primaire")
        self.combats = {}
        self.cibles = {}
        self.cible = {}

    def config(self):
        """Méthode de configuration du module"""
        importeur.hook.ajouter_hook("pnj:attaque",
                "Hook appelé quand un PNJ est attaqué")

        # Ajout de l'état combat
        etat = self.importeur.perso.ajouter_etat("combat")
        etat.msg_refus = "Vous êtes en train de combattre."
        etat.msg_visible = "combat ici"
        etat.act_interdites = ["tuer", "bouger", "prendre", "poser",
                "chercherbois", "ouvrir", "fermer", "jouer", "porter",
                "retirer", "ingerer"]

        # État scruter
        etat = self.importeur.perso.ajouter_etat("scruter")
        etat.msg_refus = "Vous êtes un peu occupé."
        etat.msg_visible = "se trouve ici"

        # État charger
        etat = self.importeur.perso.ajouter_etat("charger")
        etat.msg_refus = "Vous êtes un peu occupé."
        etat.msg_visible = "se trouve ici"
        etat.act_autorisees = ["regarder", "parler"]

        BaseModule.config(self)

    def init(self):
        """Initialisation du module."""
        # Ajout du prompt
        importeur.perso.ajouter_prompt(PromptCombat)

        # Ajout du niveau combat
        ajouter_niveau = self.importeur.perso.ajouter_niveau
        ajouter_niveau("combat", "combat")

        # Ajout des talents
        ajouter_talent = self.importeur.perso.ajouter_talent
        for type in Arme.types.values():
            if not type.cle_talent:
                continue

            if not (type.nom_talent and type.niveau_talent and \
                    type.difficulte_talent):
                raise ValueError("la définition du talent lié au type " \
                        "d'arme {} est incomplète".format(type.nom_type))

            ajouter_talent(type.cle_talent, type.nom_talent,
                    type.niveau_talent, type.difficulte_talent)

        ajouter_talent(CLE_TALENT_ESQUIVE, "esquive", "combat", 0.25)
        ajouter_talent(CLE_TALENT_PARADE, "parade", "combat", 0.20)
        ajouter_talent(CLE_TALENT_MAINS_NUES, "combat à mains nues", "combat",
                0.20)
        ajouter_talent("scruter", "détection des ennemis", "art_pisteur",
                0.23)

        BaseModule.init(self)

    def ajouter_commandes(self):
        """Ajout des commandes dans l'interpréteur"""
        self.commandes = [
            commandes.bander.CmdBander(),
            commandes.degainer.CmdDegainer(),
            commandes.paix.CmdPaix(),
            commandes.rengainer.CmdRengainer(),
            commandes.scruter.CmdScruter(),
            commandes.tirer.CmdTirer(),
            commandes.tuer.CmdTuer(),
            commandes.viser.CmdViser(),
        ]

        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)

    def get_combat_depuis_salle(self, salle):
        """Retourne le combat correspondant à la salle ou None."""
        return self.combats.get(salle.ident)

    def creer_combat(self, salle, attaquant, attaque):
        """Crée un combat ou met à jour celui existant.

        Les paramètres à préciser sont :
            salle -- la salle dans lequel va se dérouler l'action
            attaquant -- celui qui attaque
            attaque -- celui qui est attaqué

        """
        combat = self.combats.get(salle.ident) or Combat(salle)
        combat.ajouter_combattants(attaquant, attaque)
        if salle.ident not in self.combats:
            self.combats[salle.ident] = combat
            self.importeur.diffact.ajouter_action(
                "combat:{}".format(salle.ident), 3, combat.tour, self.importeur)

    def supprimer_combat(self, ident):
        """Supprime un combat."""
        if ident in self.combats:
            combat = self.combats[ident]
            del self.combats[ident]
            self.importeur.diffact.retirer_action(
                "combat:{}".format(ident), warning=False)
            for personnage in combat.combattants:
                personnage.deselectionner_prompt("combat")
                if "combat" in personnage.etats:
                    personnage.etats.retirer("combat")

    def verifier_cible(self, personnage):
        """Vérifie et efface éventuellement la cible."""
        cible = self.cible.get(personnage)
        if cible and cible.est_mort():
            del self.cible[personnage]

    def detruire(self):
        """Destruction du module."""
        for combat in self.combats.values():
            for combattant in combat.combattants:
                combattant.etats.retirer("combat")

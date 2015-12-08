# -*-coding:Utf-8 -*

# Copyright (c) 2010 LE GOFF Vincent
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


"""Fichier contenant le module primaire pnj."""

from abstraits.module import *
from primaires.perso.exceptions.action import ExceptionAction
from primaires.pnj.chemin import CheminPNJ
from .prototype import Prototype
from .pnj import PNJ
from . import cherchables
from . import commandes
from . import masques
from .editeurs.pedit import EdtPedit

# Constantes
NB_TICKS = 20

class Module(BaseModule):

    """Cette classe contient les informations du module primaire pnj.

    Comme son nom l'indique, ce module gère les PNJ de l'univers,
    personnages non joueurs, hérités de Personnage mais distincts des
    joueurs dans le sens où ils sont animés par l'univers et non par
    des joueurs connectés.

    Ce module gère également les prototypes de PNJ. Plusieurs PNJ peuvent
    être modelés sur le même prototype (être du même nom, de la même race,
    avoir le même équipement, par exemple deux gardes d'une Cité).

    """

    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "pnj", "primaire")
        self._PNJ = {}
        self._prototypes = {}
        self.ticks = {}
        self.chemins = {}
        for no in range(1, NB_TICKS + 1):
            self.ticks[no] = []

        type(importeur).espace["prototypes_pnj"] = self._prototypes
        type(importeur).espace["PNJ"] = self._PNJ

    def config(self):
        """Méthode de configuration du module"""
        importeur.hook.ajouter_hook("pnj:arrive",
                "Hook appelé quand un personnage arrive près du PNJ")
        importeur.hook.ajouter_hook("pnj:meurt",
                "Hook appelé quand un PNJ meurt")
        importeur.hook.ajouter_hook("pnj:détruit",
                "Hook appelé quand le PNJ est détruit pour X raison")
        importeur.hook.ajouter_hook("pnj:nom",
                "Hook appelé pour changer le nom d'un PNJ")
        importeur.hook.ajouter_hook("pnj:doit_afficher",
                "Hook appelé quand on regarde la salle.")
        importeur.hook.ajouter_hook("pnj:tick",
                "Hook appelé quand le PNJ se tick")
        importeur.hook.ajouter_hook("pnj:gagner_xp",
                "Hook appelé quand un PNJ gagne de l'XP")

        # Ajout des états
        depece = importeur.perso.ajouter_etat("depece")
        depece.msg_refus = "Vous êtes en train de dépecer un cadavre."
        depece.msg_visible = "dépèce un cadavre ici"
        depece.act_autorisees = ["regarder", "parler"]

        BaseModule.config(self)

    def init(self):
        """Initialisation du module"""
        prototypes = self.importeur.supenr.charger_groupe(Prototype)
        for prototype in prototypes:
            self._prototypes[prototype.cle] = prototype

        pnjs = self.importeur.supenr.charger_groupe(PNJ)
        pnjs = [p for p in pnjs if hasattr(p, "identifiant") and \
                p.prototype]
        for pnj in pnjs:
            self._PNJ[pnj.identifiant] = pnj

        chemins = self.importeur.supenr.charger_groupe(CheminPNJ)
        chemins = self.importeur.supenr.charger_groupe(CheminPNJ)
        for chemin in chemins:
            self.ajouter_chemin(chemin)

        # Ajout des actions différées pour chaque tick
        intervalle = 60 / NB_TICKS
        for no in self.ticks.keys():
            self.importeur.diffact.ajouter_action("ntick_{}".format(no),
                    intervalle * no, self.tick, no)

        importeur.perso.ajouter_talent("depecage", "dépeçage", "survie", 0.25)

        # On relie l'hook pnj:attaque
        self.importeur.hook["pnj:attaque"].ajouter_evenement(
                self.repondre_attaque)

        BaseModule.init(self)

    def ajouter_commandes(self):
        """Ajout des commandes dans l'interpréteur"""
        self.commandes = [
            commandes.chemin.CmdChemin(),
            commandes.controler.CmdControler(),
            commandes.depecer.CmdDepecer(),
            commandes.pedit.CmdPedit(),
            commandes.plist.CmdPlist(),
            commandes.ppurge.CmdPpurge(),
            commandes.pspawn.CmdPspawn(),
        ]

        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)

        # Ajout de l'éditeur 'redit'
        self.importeur.interpreteur.ajouter_editeur(EdtPedit)

    def preparer(self):
        """Préparation du module."""
        for p in self._prototypes.values():
            p.pnj = []

        for pnj in self._PNJ.values():
            pnj.prototype.pnj.append(pnj)
            pnj.script["repop"].executer(pnj=pnj)


            # Ajout des affections à diffact
            for affection in pnj.affections.values():
                affection.prevoir_tick()

    @property
    def PNJ(self):
        """Retourne un dictionnaire déréférencé des PNJ."""
        return dict(self._PNJ)

    @property
    def prototypes(self):
        """Retourne un dictionnaire déréférencé des prototypes."""
        return dict(self._prototypes)

    def creer_prototype(self, cle):
        """Crée un prototype et l'ajoute aux prototypes existants"""
        if cle in self._prototypes:
            raise ValueError("la clé {} est déjà utilisée comme " \
                    "prototype".format(cle))

        prototype = Prototype(cle)
        self.ajouter_prototype(prototype)
        return prototype

    def ajouter_prototype(self, prototype):
        """Ajoute un prototype au dictionnaire des prototypes"""
        if prototype.cle in self._prototypes:
            raise ValueError("la clé {} est déjà utilisée comme " \
                    "prototype".format(prototype.cle))

        self._prototypes[prototype.cle] = prototype

    def supprimer_prototype(self, cle):
        """Supprime le prototype cle"""
        prototype = self._prototypes[cle]
        del self._prototypes[cle]
        prototype.detruire()

    def creer_PNJ(self, prototype, salle=None):
        """Crée un PNJ depuis le prototype prototype.

        Le PNJ est ensuite ajouté à la liste des PNJ existants.

        """
        pnj = PNJ(prototype, salle)
        self.ajouter_PNJ(pnj)
        return pnj

    def ajouter_PNJ(self, pnj):
        """Ajoute le PNJ à la liste des PNJ"""
        if pnj.identifiant in self._PNJ:
            raise ValueError("l'identifiant {} est déjà utilisé comme " \
                    "PNJ".format(pnj.identifiant))

        self._PNJ[pnj.identifiant] = pnj

    def supprimer_PNJ(self, identifiant):
        """Supprime le PNJ de la liste des PNJ."""
        pnj = self._PNJ[identifiant]
        self.importeur.hook["pnj:détruit"].executer(pnj)
        del self._PNJ[identifiant]
        pnj.detruire()

    def creer_chemin(self, cle):
        """Crée le chemin dont la clé est spécifiée."""
        if cle in self.chemins:
            raise ValueError("le chemin avec la clé {} existe déjà".format(
                    cle))

        chemin = CheminPNJ(cle)
        self.ajouter_chemin(chemin)
        return chemin

    def ajouter_chemin(self, chemin):
        """Ajoute le chemin précisé."""
        if chemin.cle in self.chemins:
            raise ValueError("le chemin avec la clé {} existe déjà".format(
                    cle))

        self.chemins[chemin.cle] = chemin

    def supprimer_chemin(self, cle):
        """Supprime le chemin."""
        self.chemins.pop(cle).detruire()

    def tick(self, no):
        """Exécute un tick."""
        self.importeur.diffact.ajouter_action("ntick_{}".format(no),
                60, self.tick, no)

        # On sélectionne les PNJ à tick
        pnj = list(self._PNJ.values())
        tick = []
        i = no - 1
        while i < len(pnj):
            try:
                p = pnj[i]
            except IndexError:
                pass
            else:
                tick.append(p)
            i += NB_TICKS

        for p in tick:
            p.tick()

    def suivre_chemin(self, pnj, temps, chemin, avant=True):
        """Fait suivre le chemin spécifié au PNJ.

        Concrètement, cette méthode doit :

          * Faire avancer le PNJ d'une salle si possible
          * Relancer la méthode en action différée si nécessaire.

        Le paramètre 'avant' précise dans quel sens le chemin doit
        être suivi : si avant est True (par défaut), suit le chemin
        dans le sens d'origine. Sinon, essaye de suivre le chemin dans
        le sens contraire (tous les chemins ne peuvent pas être
        suivis dans les deux sens).

        """
        salles = {}
        if avant:
            salles = chemin.salles
        elif not chemin.a_flag("ne peut pas être pris à l'envers"):
            salles = chemin.salles_retour

        salle = pnj.salle
        direction = salles.get(salle)
        derniere = chemin.destination if avant else chemin.origine
        if direction is None:
            return
        elif derniere is salle and not chemin.a_flag("circulaire"):
            return

        nom_action = str(id(chemin)) + str(id(pnj))
        importeur.diffact.ajouter_action(nom_action, temps,
                self.suivre_chemin, pnj, temps, chemin, avant)
        sortie = salle.sorties.get(direction)
        verrou = False
        if sortie.porte and sortie.porte.verrouillee:
            sortie.porte.verrouillee = False
            verrou = True

        pnj.deplacer_vers(sortie.nom)
        if verrou:
            sortie.porte.verrouillee = True

    def repondre_attaque(self, pnj, personnage):
        """Répond à l'attaque."""
        if personnage.salle is pnj.salle and not pnj.est_en_combat():
            try:
                pnj.agir("tuer")
            except ExceptionAction:
                return
            else:
                pnj.attaquer(personnage)

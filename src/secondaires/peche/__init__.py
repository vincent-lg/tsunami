# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Fichier contenant le module secondaire napeche."""

import random

from abstraits.module import *
from corps.aleatoire import *
from corps.fonctions import valider_cle
from .banc import Banc
from . import commandes
from .editeurs.schooledit import EdtSchooledit
from . import types

# Constantes
TERRAINS_PECHE = ("rive", )

class Module(BaseModule):

    """Module secondaire définissant la pêche."""

    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "peche", "secondaire")
        self.commandes = []
        self.bancs = {}

    def config(self):
        """Configuration du module."""
        pecher = self.importeur.perso.ajouter_etat("pecher")
        pecher.msg_refus = "Vous êtes en train de pêcher"
        pecher.msg_visible = "pêche ici"
        pecher.act_autorisees = ["regarder", "parler", "geste"]

        BaseModule.config(self)

    def init(self):
        """Chargement des bancs de poisson."""
        importeur.perso.ajouter_talent("peche_terre", "pêche à quai",
                "survie", 0.45)
        importeur.perso.ajouter_talent("peche_mer", "pêche embarquée",
                "survie", 0.42)

        bancs = self.importeur.supenr.charger_groupe(Banc)
        for banc in bancs:
            self.bancs[banc.cle] = banc

        importeur.diffact.ajouter_action("bancs", 60,
                self.tick_bancs)

        BaseModule.init(self)

    def ajouter_commandes(self):
        """Ajout des commandes dans l'interpréteur"""
        self.commandes = [
            commandes.appater.CmdAppater(),
            commandes.banc.CmdBanc(),
            commandes.pecher.CmdPecher(),
        ]

        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)

        # Ajout des éditeurs
        self.importeur.interpreteur.ajouter_editeur(EdtSchooledit)

    def creer_banc(self, cle):
        """Crée un banc de poisson et l'ajoute dans le dictionnaire.

        Retourne le banc créé.

        Lève une exception KeyError si le banc existe déjà.

        """
        valider_cle(cle)
        if cle in self.bancs:
            raise KeyError("le banc de poisson '{}' existe déjà".format(cle))

        banc = Banc(cle)
        self.ajouter_banc(banc)
        return banc

    def ajouter_banc(self, banc):
        """Ajoute le banc de poisson dans le dictionnaire."""
        self.bancs[banc.cle] = banc

    def supprimer_banc(self, cle):
        """Supprime le banc de poisson portant la clé passée en paramètre."""
        if cle not in self.bancs:
            raise KeyError("le banc de poisson '{}' est inconnue".format(
                    cle))

        banc = self.bancs[cle]
        del self.bancs[cle]
        banc.detruire()

    def tick_bancs(self):
        """Tick les bancs."""
        importeur.diffact.ajouter_action("bancs", 60,
                self.tick_bancs)
        for banc in self.bancs.values():
            banc.tick()

    def get_banc_pour(self, salle):
        """Retourne le banc de poisson pour la salle ou None.

        Si la salle a une étendue définie et que cette étendue a
        un banc de poisson, retourne ce banc. Si la salle est dans un des
        terrains pêches, retourne (si trouvé) le banc 'base'.

        """
        etendue = salle.get_etendue()
        if etendue:
            for banc in self.bancs.values():
                if banc.etendue is etendue:
                    return banc
            return self.bancs.get("base")

        if salle.nom_terrain not in TERRAINS_PECHE:
            return None

        # Si le banc n'est toujours pas trouvé, cherche dans les bancs
        for banc in self.bancs.values():
            if salle in banc.salles:
                return banc

        return self.bancs.get("base")

    def get_talent_peche(self, salle):
        """Retourne la clé du talent de pêche correspondant à la salle."""
        if hasattr(salle, "navire") and salle.navire:
            return "peche_mer"

        return "peche_terre"

    def attendre_pecher(self, personnage, canne):
        """Le personnage pêche."""
        banc = self.get_banc_pour(personnage.salle)
        talent = self.get_talent_peche(personnage.salle)
        if personnage.cle_etat != "pecher":
            return

        if canne.appat is None:
            personnage.cle_etat = ""

        personnage.pratiquer_talent(talent, 5)
        if chance_sur(5) and banc.abondance_actuelle > 0:
            personnage.sans_prompt()
            personnage << "Votre ligne frémit légèrement, comme " \
                    "sensiblement effleurée."
            importeur.diffact.ajouter_action("pecher:" + personnage.nom, 10,
                    self.touche, personnage, canne)
        else:
            importeur.diffact.ajouter_action("pecher:" + personnage.nom, 12,
                    self.attendre_pecher, personnage, canne)
            personnage.sans_prompt()
            personnage << "Votre ligne est toujours aussi immobile..."

    def touche(self, personnage, canne):
        """Une touche se transforme ou non en prise."""
        banc = self.get_banc_pour(personnage.salle)
        talent = self.get_talent_peche(personnage.salle)
        if personnage.cle_etat != "pecher":
            return

        if canne.appat is None:
            personnage.cle_etat = ""

        connaissance = personnage.pratiquer_talent(talent, 3)
        qualite = varier(canne.appat.qualite, 2)
        qualite /= 21
        abondance = banc.abondance_actuelle
        qualite += connaissance / 400 + abondance / 400
        if banc.poissons and random.random() < qualite:
            # On choisit le poisson
            poissons = list(banc.poissons.keys())
            poids = list(banc.poissons.values())
            poisson = choix_probable_liste(poissons, poids)
            tps = varier(int(poisson.poids), 4, 1, 15)
            personnage.sans_prompt()
            personnage << "Une violente secousse agite votre ligne !"
            personnage << "Vous rejetez votre canne en arrière..."
            personnage.salle.envoyer("{} rejète sa canne en arrière...",
                    personnage, prompt=False)
            importeur.diffact.ajouter_action("pecher:" + personnage.nom, tps,
                    self.pecher, personnage, canne, poisson)
        else:
            importeur.diffact.ajouter_action("pecher:" + personnage.nom, 15,
                    self.attendre_pecher, personnage, canne)

    def pecher(self, personnage, canne, poisson):
        """Pêche le poisson."""
        banc = self.get_banc_pour(personnage.salle)
        talent = self.get_talent_peche(personnage.salle)
        if personnage.cle_etat != "pecher":
            return

        if canne.appat is None:
            personnage.cle_etat = ""

        personnage.pratiquer_talent(talent)

        if canne.tension_max < poisson.poids:
            personnage << "Dans un craquement brutal, votre canne à " \
                    "pêche se brise !"
            personnage.salle.envoyer_lisser("Dans un craquement brutal, " \
                    "la canne à pêche de {} se brise !", personnage)
            importeur.objet.supprimer_objet(canne.appat.identifiant)
            canne.contenu.retirer(canne)
            importeur.objet.supprimer_objet(canne.identifiant)
            return

        poisson = importeur.objet.creer_objet(poisson)
        banc.pecher(poisson)
        personnage.salle.objets_sol.ajouter(poisson)
        personnage << "{} décrit un arc dans les airs et tombe à vos " \
                "pieds !".format(poisson.get_nom())
        personnage.salle.envoyer_lisser("{} décrit un arc dans les airs " \
                "et tombe aux pieds de {{}}.".format(poisson.get_nom()),
                personnage)
        personnage.cle_etat = ""
        importeur.objet.supprimer_objet(canne.appat.identifiant)
        canne.appat = None

        # Gain d'XP
        p_niveau = personnage.niveaux.get("survie", 1)
        if p_niveau <= 5:
            fact = 0.2
        elif p_niveau <= 10:
            fact = 0.1
        elif p_niveau <= 20:
            fact = 0.07
        elif p_niveau <= 50:
            fact = 0.05
        else:
            fact = 0.01

        personnage.gagner_xp_rel(poisson.niveau_peche, fact * 100, "survie")

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


"""Fichier contenant le module primaire perso."""

from collections import namedtuple

from abstraits.module import *
from primaires.format.fonctions import supprimer_accents

from . import commandes
from . import masques
from .editeurs.skedit import EdtSkedit
from .editeurs.raedit import EdtRaedit
from .cfg_stats import cfg_stats
from .cfg_niveaux import cfg_niveaux
from .cfg_talents import cfg_talents
from .race import Race
from .stats import *
from .squelette import Squelette
from .niveaux import Niveaux
from .templates.niveau import Niveau
from .templates.talent import Talent
from .templates.etat import Etat
from .templates.position import Position
from .templates.allonge import Allonge
from .templates.assis import Assis
from .prompt import prompts
from .prompt.defaut import PromptDefaut

class Module(BaseModule):

    """Module gérant la classe Personnage qui sera héritée pour construire
    des joueurs et PNJs. Les mécanismes propres au personnage (c'est-à-dire
    indépendants de la connexion et liés à l'univers) seront gérés ici.

    En revanche, les contextes de connexion ou de création d'un personnage
    ne se trouvent pas ici (il s'agit d'informations propres à un joueur, non
    à un PNJ).

    """

    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "perso", "primaire")
        self.cfg_stats = None
        self.cfg_niveaux = None
        self.cfg_talents = None
        self.modele_stats = None
        self.commandes = []
        self.squelettes = {}
        self.races = []
        self.gen_niveaux = None
        self.niveaux = {}
        self.talents = {}
        self.etats = {}
        self.positions = {}
        self.prompts = prompts

    def config(self):
        """Méthode de configuration.

        On récupère les fichiers de configuration correspondant au module.

        """
        self.cfg_stats = conf_stats = type(self.importeur).anaconf.get_config(
                "stats", "perso/stats.cfg", "modele stats", cfg_stats)
        conf_stats._set_globales({
            "I0":I0,
            "IE0":IE0,
            "SM":SM,
            "SEM":SEM,
        })

        self.modele_stats = Stats()

        self.cfg_niveaux = type(self.importeur).anaconf.get_config(
                "niveaux", "perso/niveaux.cfg", "modele niveaux", cfg_niveaux)

        self.cfg_talents = type(self.importeur).anaconf.get_config(
                "talents", "perso/talents.cfg", "modele talents", cfg_talents)

        self.ajouter_niveau("art_pisteur", "art du pisteur")

        # Ajout des états (assis et allongé)
        assis = self.ajouter_etat("assis", Assis)
        assis.msg_refus = "Vous êtes assis."
        assis.msg_visible = "est assis là"
        assis.act_autorisees = ["regarder", "poser", "parler", "ingerer",
                "lancersort", "lever", "geste", "allonger", "pecher", "ramer"]
        allonge = self.ajouter_etat("allonge", Allonge)
        allonge.msg_refus = "Vous êtes allongé."
        allonge.msg_visible = "est allongé là"
        allonge.act_autorisees = ["regarder", "parler", "ingerer",
                "lever", "geste", "asseoir"]

        mort = self.ajouter_etat("mort")
        mort.msg_refus = "Vous êtes inconscient."
        mort.msg_visible = "est inconscient ici"
        paralyse = self.ajouter_etat("paralyse")
        paralyse.msg_refus = "Vous ne pouvez bouger un muscle."
        paralyse.msg_visible = "se tient, rigide, à cet endroit"
        paralyse.peut_etre_attaque = False
        paralyse.sauvegarder_au_reboot = True

        entraine = self.ajouter_etat("entrainer")
        entraine.msg_refus = "Vous êtes en train de vous entraîner."
        entraine.msg_visible = "s'entraîne ici"
        entraine.act_autorisees = ["regarder", "parler"]

        recherche = self.ajouter_etat("recherche")
        recherche.msg_refus = "Vous êtes un peu occupé."
        recherche.msg_visible = "cherche quelque chose ici"
        recherche.act_autorisees = ["parler"]

        # Ajout des hooks
        importeur.hook.ajouter_hook("personnage:peut_deplacer",
                "Hook appelé quand un personnage veut se déplacer.")
        importeur.hook.ajouter_hook("personnage:calculer_endurance",
                "Hook appelé pour calculer l'endurance de déplacement.")
        importeur.hook.ajouter_hook("personnage:deplacer",
                "Hook appelé quand un personnage se déplace.")
        importeur.hook.ajouter_hook("personnage:verbe_deplacer",
                "Hook appelé pour retourner le verbe de déplacement.")
        importeur.hook.ajouter_hook("personnage:verbe_arriver",
                "Hook appelé pour retourner le verbe d'arriver.")

        BaseModule.config(self)

    def init(self):
        """Initialisation du module"""
        # Ajout du prompt
        self.ajouter_prompt(PromptDefaut)

        # On construit le niveau
        niveaux = Niveaux
        niveaux.nb_niveaux = self.cfg_niveaux.nb_niveaux
        niveaux.xp_min = self.cfg_niveaux.xp_min
        niveaux.xp_max = self.cfg_niveaux.xp_max
        niveaux.points_entrainement_fixes = \
                self.cfg_niveaux.points_entrainement_fixes
        niveaux.points_entrainement_paliers = \
                self.cfg_niveaux.points_entrainement_paliers
        niveaux.stats_entrainables = self.cfg_stats.entrainables
        niveaux.calculer_grille()
        self.gen_niveaux = niveaux

        # On récupère les squelettes
        squelettes = self.importeur.supenr.charger_groupe(Squelette)
        for squelette in squelettes:
            self.ajouter_squelette(squelette)

        # On récupère les races
        races = self.importeur.supenr.charger_groupe(Race)
        for race in races:
            self.ajouter_race(race)

        # Positions
        self.ajouter_position("assis", "est assis", "est assise")
        self.ajouter_position("allonge", "est allongé", "est allongée")

        self.ajouter_talent("escalade", "escalade", "survie", 0.31)
        self.ajouter_talent("nage", "nage", "survie", 0.25)

        BaseModule.init(self)

    def ajouter_commandes(self):
        """Ajout des commandes dans l'interpréteur"""
        self.commandes = [
            commandes.allonger.CmdAllonger(),
            commandes.asseoir.CmdAsseoir(),
            commandes.chercher.CmdChercher(),
            commandes.commande.CmdCommande(),
            commandes.d.CmdD(),
            commandes.equipement.CmdEquipement(),
            commandes.lever.CmdLever(),
            commandes.m.CmdM(),
            commandes.niveaux.CmdNiveaux(),
            commandes.prompt.CmdPrompt(),
            commandes.quete.CmdQuete(),
            commandes.qui.CmdQui(),
            commandes.raedit.CmdRaedit(),
            commandes.score.CmdScore(),
            commandes.skedit.CmdSkedit(),
            commandes.sklist.CmdSklist(),
            commandes.talents.CmdTalents(),
            commandes.v.CmdV(),
        ]

        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)

        # Ajout des éditeurs
        self.importeur.interpreteur.ajouter_editeur(EdtRaedit)
        self.importeur.interpreteur.ajouter_editeur(EdtSkedit)

    def preparer(self):
        """Préparation des personnages."""
        personnages = list(importeur.joueur.joueurs.values()) + list(
                importeur.pnj.PNJ.values())
        for personnage in personnages:
            personnage.etats.reinitialiser()
            if personnage.salle and personnage.salle.nom_terrain == \
                    "subaquatique" and not personnage.est_immortel():
                personnage.plonger()

    def get_niveau_par_nom(self, nom):
        """Retourne le niveau dont le nom est donné."""
        nom = supprimer_accents(nom).lower()
        for niveau in self.niveaux.values():
            if supprimer_accents(niveau.nom).lower() == nom:
                return niveau

        raise ValueError("niveau inconnu {}".format(nom))

    def creer_squelette(self, cle):
        """Création d'un squelette"""
        squelette = Squelette(cle)
        self.ajouter_squelette(squelette)
        return squelette

    def ajouter_squelette(self, squelette):
        """Ajoute le squelette aux squelettes existants"""
        self.squelettes[squelette.cle] = squelette

    def supprimer_squelette(self, cle):
        """Supprime le squelette existant"""
        squelette = self.squelettes[cle]
        del self.squelettes[cle]
        squelette.detruire()

    def creer_race(self, nom):
        """Crée la race du nom indiqué"""
        race = Race(nom)
        self.ajouter_race(race)
        return race

    def ajouter_race(self, race):
        """Ajout de la race au dictionnaire des races existantes"""
        self.races.append(race)

    def supprimer_race(self, nom):
        """Suppression de la race 'nom'"""
        race = None
        indice = None
        for i, t_race in enumerate(self.races):
            if t_race.nom.lower() == nom.lower():
                race = t_race
                indice = i

        if indice is None:
            raise KeyError("ce nom de race est introuvable")

        del self.races[indice]
        race.detruire()

    def race_est_utilisee(self, race):
        """Contrôle si la race est déjà utilisée ou non.

        La race peut être utilisée :
        -   par un joueur
        -   par un prototype de PNJ

        """
        a_tester = list(self.importeur.connex.joueurs)
        a_tester += list(self.importeur.pnj.prototypes.values())
        for test in a_tester:
            if test.race is race:
                return True

        return False

    def stats_symboles(self):
        """Retourne un tuple nommé contenant les stats et leur symbole.

        Par exemple :
        >>> nt = importeur.perso.stats_symboles()
        >>> nt.force
        'f'

        """
        NTStats = namedtuple("NTStats",
                [stat.nom for stat in self.modele_stats])
        stats_symboles = dict(((stat.nom, "%{}".format(stat.symbole)) \
                for stat in self.modele_stats))
        ntstats = NTStats(**stats_symboles)
        return ntstats

    def ajouter_niveau(self, cle, nom):
        """Ajoute un niveau au dictionnaire des niveaux."""
        if cle in self.niveaux:
            raise ValueError("la clé {} est déjà utilisée comme clé " \
                    "de niveau".format(repr(cle)))

        niveau = Niveau(cle, nom)
        self.niveaux[cle] = niveau

    def ajouter_talent(self, cle, nom, niveau, difficulte):
        """Ajoute un talent."""
        if cle in self.talents:
            raise ValueError("un talent de clé {} existe déjà".format(cle))

        talent = Talent(self.niveaux, cle, nom, niveau, difficulte)
        self.talents[cle] = talent

    def ajouter_etat(self, cle, classe=None):
        """Ajoute un état dans le dictionnaire."""
        if classe is None:
            classe = type("Etat{}".format(cle.capitalize()), (Etat, ), {})
            classe.cle = cle
        if cle in self.etats:
            raise ValueError("l'état {} existe déjà".format(cle))

        self.etats[cle] = classe

        return classe

    def ajouter_position(self, cle, etat_m, etat_f):
        """Ajoute une position."""
        position = Position(cle, etat_m, etat_f)
        self.positions[cle] = position
        return position

    def ajouter_prompt(self, prompt):
        """Ajoute un prompt.

        Cette méthode attend en paramètre une classe héritée de Prompt.

        """
        self.prompts[prompt.nom] = prompt

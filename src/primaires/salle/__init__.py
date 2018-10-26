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


"""Fichier contenant le module primaire salle."""

from datetime import datetime
from fractions import Fraction
from math import sqrt
import re
from random import random, randint

from abstraits.module import *
from primaires.format.fonctions import format_nb, supprimer_accents
from primaires.vehicule.vecteur import Vecteur
from .bonhomme_neige import *
from .config import cfg_salle
from .coordonnees import Coordonnees
from .decor import PrototypeDecor
from .etendue import Etendue
from .obstacle import Obstacle
from .porte import Porte
from .salle import Salle, ZONE_VALIDE, MNEMONIC_VALIDE
from .feu import Feu
from .sortie import Sortie
from .sorties import NOMS_SORTIES
from .zone import Zone
from .templates.terrain import Terrain
from .editeurs.aedit import EdtAedit
from .editeurs.decedit import EdtDecedit
from .editeurs.redit import EdtRedit
from .editeurs.sbedit import EdtSbedit
from .editeurs.zedit import EdtZedit
from . import cherchables
from . import commandes
from . import masques
from . import types

# Constantes
NB_MIN_NETTOYAGE = 20
NB_TICKS = 20

class Module(BaseModule):

    """Classe utilisée pour gérer des salles.

    Dans la terminologie des MUDs, les salles sont des "cases" avec une
    description et une liste de sorties possibles, que le joueur peut
    emprunter. L'ensemble des salles consiste l'univers, auquel il faut
    naturellement rajouter des PNJ et objets pour qu'il soit riche un minimum.

    Pour plus d'informations, consultez le fichier
    src/primaires/salle/salle.py contenant la classe Salle.

    """

    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "salle", "primaire")
        self._salles = {} # ident:salle
        self.feux = {} # ident:feu
        self._zones = {} # cle:zone
        self._coords = {} # coordonnee:salle
        self.commandes = []
        self.salle_arrivee = ""
        self.salle_retour = ""
        self.p_nettoyer = True
        self.aliases = {
            "e": "est",
            "se": "sud-est",
            "s": "sud",
            "so": "sud-ouest",
            "o": "ouest",
            "no": "nord-ouest",
            "n": "nord",
            "ne": "nord-est",
            "b": "bas",
            "h": "haut",
            "s-e": "sud-est",
            "s-o": "sud-ouest",
            "n-o": "nord-ouest",
            "n-e": "nord-est",
        }

        self.logger = importeur.man_logs.creer_logger( \
                "salles", "salles")
        self.terrains = {}
        self.etendues = {}
        self.obstacles = {}
        self.ch_minute = []
        self.ch_heure = []
        self.ch_jour = []
        self.ch_mois = []
        self.ch_annee = []

        # Liste des méthodes ajoutant des salles éventuelles à cartographier
        # Par exemple, un éventuel module secondaire de navigation ajoute à
        # cette liste une fonction retournant les bateaux. Cette fonction
        # doit impérativement retourner une liste de salles sous la forme
        # d'un tuple (nom, interieur, (x, y)) (interieur est un booléen).
        self.salles_a_cartographier = []
        self.graph = {}
        self.details_dynamiques = []
        self.decors = {}
        self.bonhommes_neige = {}
        self.a_renouveler = {}
        self.magasins_a_ouvrir = {}
        self.magasins_a_fermer = {}

        # Constantes
        self.TERRAINS_SANS_FEU = ("ville", "désert", "route", "aquatique",
                "subaquatique", "rive")

        # Ticks
        self.ticks = {}
        for no in range(1, NB_TICKS + 1):
            self.ticks[no] = []

        type(importeur).espace["salles"] = self._salles
        type(importeur).espace["zones"] = self._zones

    @property
    def salles(self):
        """Retourne un dictionnaire déréférencé des salles."""
        return dict(self._salles)

    @property
    def zones(self):
        """Retourne un dictionnaire déréférencé des zones."""
        return dict(self._zones)

    def config(self):
        """Méthode de configuration du module"""
        importeur.anaconf.get_config("salle", \
            "salle/salle.cfg", "config salle", cfg_salle)
        importeur.hook.ajouter_hook("salle:regarder",
                "Hook appelé dès qu'on regarde une salle.")
        importeur.hook.ajouter_hook("salle:trouver_chemins_droits",
                "Hook appelé quand on recherche les chemins droits " \
                "d'une salle.")

        # Ajout des terrain
        self.ajouter_terrain("ville", "quelques maisons")
        self.ajouter_terrain("route", "une route")
        self.ajouter_terrain("forêt", "des forêts denses")
        self.ajouter_terrain("plaine", "des plaines verdoyantes")
        self.ajouter_terrain("rive", "une rive basse")
        des = self.ajouter_terrain("désert", "des terres désertiques")
        des.perte_endurance_dep = 4
        self.ajouter_terrain("caverne", "une muraille de roches")
        self.ajouter_terrain("aquatique", "des terres flottantes")
        self.ajouter_terrain("subaquatique", "des terres sous-marines")
        self.ajouter_terrain("quai de bois", "des quais de bois")
        self.ajouter_terrain("quai de pierre", "des quais de pierre")
        self.ajouter_terrain("falaise", "de hautes falaises")
        self.ajouter_terrain("montagne", "de hautes montagnes")
        self.ajouter_terrain("plage de sable blanc",
                "des plages de sable blanc")
        self.ajouter_terrain("plage de sable noir",
                "des plages de sable noir")
        self.ajouter_terrain("rocher", "un rocher à demi immergé")
        self.ajouter_terrain("rempart", "un haut mur fortifié")
        self.ajouter_terrain("récif", "une ligne de récifs")
        self.ajouter_terrain("rapide", "de dangereux rapides")
        self.ajouter_terrain("banc de sable",
                "un banc de sable à demi immergé")
        self.ajouter_terrain("corail", "une barrière de corail")

        # On ajoute les niveaux
        importeur.perso.ajouter_niveau("survie", "survie")

        # On ajoute de l'état
        etat = importeur.perso.ajouter_etat("collecte_bois")
        etat.msg_refus = "Vous êtes en train de ramasser du bois."
        etat.msg_visible = "ramasse du bois"
        etat.act_autorisees = ["regarder", "parler"]

        etat = importeur.perso.ajouter_etat("bonhomme_neige")
        etat.msg_refus = "Vous êtes en train de fabriquer un bonhomme de neige."
        etat.msg_visible = "fabrique un bonhomme de neige"
        etat.act_autorisees = ["regarder", "parler"]

        BaseModule.config(self)

    def init(self):
        """Méthode d'initialisation du module"""
        # On récupère les salles
        salles = importeur.supenr.charger_groupe(Salle)
        for salle in salles:
            self.ajouter_salle(salle)

        nb_salles = len(self._salles)
        self.logger.info(format_nb(nb_salles, "{nb} salle{s} récupérée{s}", \
                fem=True))

        # On récupère les étendues
        etendues = self.importeur.supenr.charger_groupe(Etendue)
        for etendue in etendues:
            self.ajouter_etendue(etendue)

        nb_etendues = len(self.etendues)
        self.logger.info(format_nb(nb_etendues, "{nb} étendue{s} " \
                "d'eau{x} récupérée{s}", fem=True))

        # On récupère les obstacles
        obstacles = self.importeur.supenr.charger_groupe(Obstacle)
        for obstacle in obstacles:
            self.ajouter_obstacle(obstacle)

        # On récupère les décors
        decors = importeur.supenr.charger_groupe(PrototypeDecor)
        for decor in decors:
            self.ajouter_decor(decor)

        nb_decors = len(self.decors)
        self.logger.info(format_nb(nb_decors, "{nb} décor{s} récupéré{s}"))

        # On récupère les bonhommes de neige
        bonhommes = importeur.supenr.charger_groupe(PrototypeBonhommeNeige)
        for bonhomme in bonhommes:
            self.ajouter_bonhomme_neige(bonhomme)

        nb_bonhommes = len(self.bonhommes_neige)
        self.logger.info(format_nb(nb_bonhommes, "{nb} prototype{s} " \
                "de bonhomme de neige récupéré{s}"))

        # On récupère les feux
        feux = importeur.supenr.charger_groupe(Feu)
        for feu in feux:
            self.feux[feu.salle.ident] = feu
        # On implémente le hook correspondant
        self.importeur.hook["salle:regarder"].ajouter_evenement(
                self.feu_present)

        # On récupère les zones
        zones = importeur.supenr.charger_groupe(Zone)
        for zone in zones:
            self._zones[zone.cle] = zone

        nb_zones = len(self._zones)
        self.logger.info(format_nb(nb_zones, "{nb} zone{s} récupérée{s}", \
                fem=True))

        importeur.diffact.ajouter_action("net_salles", 300,
                self.nettoyer_salles)
        importeur.diffact.ajouter_action("repop_salles", 900,
                self.repop_salles)
        importeur.diffact.ajouter_action("repop_feux", 5, Feu.repop)

        # On ajoute les talents
        importeur.perso.ajouter_talent("collecte_bois", "collecte de bois",
                "survie", 0.55)
        importeur.perso.ajouter_talent("feu_camp", "feu de camp", "survie",
                0.23)

        # Ajout des actions différées pour chaque tick
        intervalle = 60 / NB_TICKS
        for no in self.ticks.keys():
            self.importeur.diffact.ajouter_action("stick_{}".format(no),
                    intervalle * no, self.tick, no)

        # Ajout des hooks de changement de temps
        self.importeur.hook["temps:minute"].ajouter_evenement(
                self.changer_minute)
        self.importeur.hook["temps:heure"].ajouter_evenement(
                self.changer_heure)
        self.importeur.hook["temps:jour"].ajouter_evenement(
                self.changer_jour)
        self.importeur.hook["temps:mois"].ajouter_evenement(
                self.changer_mois)
        self.importeur.hook["temps:annee"].ajouter_evenement(
                self.changer_annee)

        BaseModule.init(self)

    def ajouter_commandes(self):
        """Ajout des commandes dans l'interpréteur"""
        self.commandes = [
            commandes.addroom.CmdAddroom(),
            commandes.carte.CmdCarte(),
            commandes.chercherbois.CmdChercherBois(),
            commandes.chsortie.CmdChsortie(),
            commandes.decor.CmdDecor(),
            commandes.deverrouiller.CmdDeverrouiller(),
            commandes.escalader.CmdEscalader(),
            commandes.etendue.CmdEtendue(),
            commandes.fermer.CmdFermer(),
            commandes.goto.CmdGoto(),
            commandes.mettrefeu.CmdMettreFeu(),
            commandes.nager.CmdNager(),
            commandes.neige.CmdNeige(),
            commandes.ouvrir.CmdOuvrir(),
            commandes.redit.CmdRedit(),
            commandes.regarder.CmdRegarder(),
                        commandes.sorties.CmdSorties(),
            commandes.supsortie.CmdSupsortie(),
            commandes.verrouiller.CmdVerrouiller(),
            commandes.zone.CmdZone(),
        ]

        for cmd in self.commandes:
            importeur.interpreteur.ajouter_commande(cmd)

        # Ajout des éditeurs 'decedit', 'redit' et 'zedit'
        importeur.interpreteur.ajouter_editeur(EdtAedit)
        importeur.interpreteur.ajouter_editeur(EdtDecedit)
        importeur.interpreteur.ajouter_editeur(EdtRedit)
        importeur.interpreteur.ajouter_editeur(EdtSbedit)
        importeur.interpreteur.ajouter_editeur(EdtZedit)

    def preparer(self):
        """Préparation du module.

        On vérifie que :
        -   Les salles de retour et d'arrivée sont bien créés (sinon,
            on les recrée)
        -   On recrée le lien entre sorties et salles
        -   Les personnages présents dans self._personnages soient
            toujours là
        -   Chaque salle est dans une zone
        -   Chaque terrain a sa réciproque en obstacle
        -   Les étendues ont toutes un contour défini
        -   Les étendues détemrinent leurs segments de liens

        """
        # On récupère la configuration
        conf_salle = importeur.anaconf.get_config("salle")
        salle_arrivee = conf_salle.salle_arrivee
        salle_retour = conf_salle.salle_retour

        if salle_arrivee not in self:
            # On crée la salle d'arrivée
            zone, mnemonic = salle_arrivee.split(":")
            salle_arrivee = self.creer_salle(zone, mnemonic, valide=False)
            salle_arrivee.titre = "La salle d'arrivée"
            salle_arrivee = salle_arrivee.ident

        if salle_retour not in self:
            # On crée la salle de retour
            zone, mnemonic = salle_retour.split(":")
            salle_retour = self.creer_salle(zone, mnemonic, valide=False)
            salle_retour.titre = "La salle de retour"
            salle_retour = salle_retour.ident

        self.salle_arrivee = salle_arrivee
        self.salle_retour = salle_retour

        # On prépare les sorties
        for salle in self.salles.values():
            if salle.magasin:
                magasin = salle.magasin
                if magasin.renouveler_ouverture:
                    liste = self.a_renouveler.get(magasin.ouverture, [])
                    liste.append(magasin)
                    self.a_renouveler[magasin.ouverture] = liste
                if magasin.renouveler_fermeture:
                    liste = self.a_renouveler.get(magasin.fermeture, [])
                    liste.append(magasin)
                    self.a_renouveler[magasin.ouverture] = liste

                liste = self.magasins_a_ouvrir.get(magasin.ouverture, [])
                liste.append(magasin)
                self.magasins_a_ouvrir[magasin.ouverture] = liste
                liste = self.magasins_a_fermer.get(magasin.fermeture, [])
                liste.append(magasin)
                self.magasins_a_fermer[magasin.fermeture] = liste

            for sortie in list(salle.sorties):
                try:
                    salle_dest = self.salles[sortie.salle_dest]
                except KeyError:
                    salle.sorties.supprimer_sortie(sortie.direction)
                else:
                    if salle_dest is None or not salle_dest.e_existe:
                        salle.sorties.supprimer_sortie(sortie.direction)
                    else:
                        sortie.salle_dest = salle_dest

            zone = salle.zone
            zone.ajouter(salle)
            for personnage in salle.personnages:
                if personnage.salle is not salle:
                    salle.retirer_personnage(personnage)

            # On ajoute les salles au renouvellement automatique
            self.inscrire_salle(salle)

        # On recrée les obstacles
        for nom, terrain in self.terrains.items():
            if nom not in self.obstacles:
                self.creer_obstacle(terrain.nom, terrain.desc_survol)

            # Ajout des affections
            for affection in salle.affections.values():
                affection.prevoir_tick()

        # On parcour les étendues
        for etendue in self.etendues.values():
            x, y = etendue.origine
            if x is not None and y is not None:
                etendue.trouver_contour()

            etendue.determiner_segments_liens()

    def detruire(self):
        """Destruction du module.

        * On détruit toutes les zones vides

        """
        for zone in self._zones.values():
            if not zone.salles:
                zone.detruire()

    def __len__(self):
        """Retourne le nombre de salles"""
        return len(self._salles)

    def __getitem__(self, cle):
        """Retourne la salle correspondante à la clé.
        Celle-ci peut être de différents types :
        *   une chaîne : c'est l'identifiant 'zone:mnemonic'
        *   un objet Coordonnees
        *   un tuple représentant les coordonnées

        """
        if type(cle) is str:
            return self._salles[cle]
        elif type(cle) is Coordonnees:
            return self._coords[cle.tuple()]
        elif type(cle) is tuple:
            return self._coords[cle]
        else:
            raise TypeError("un type non traité sert d'identifiant " \
                    "({})".format(repr(cle)))

    def __contains__(self, cle):
        """Retourne True si la clé se trouve dans l'un des dictionnaires de
        salles. Voir la méthode __getitem__ pour connaître les types acceptés.

        """
        if type(cle) is str:
            return cle in self._salles.keys()
        elif type(cle) is Coordonnees:
            return cle.tuple() in self._coords.keys()
        elif type(cle) is tuple:
            return cle in self._coords.keys()
        else:
            raise TypeError("un type non traité sert d'identifiant " \
                    "({})".format(repr(cle)))

    def ajouter_salle(self, salle):
        """Ajoute la salle aux deux dictionnaires
        self._salles et self._coords.

        """
        self._salles[salle.ident] = salle
        if salle.coords.valide:
            self._coords[salle.coords.tuple()] = salle

    def creer_salle(self, zone, mnemonic, x=0, y=0, z=0, valide=True):
        """Permet de créer une salle"""
        ident = zone + ":" + mnemonic
        if ident in self._salles.keys():
            raise ValueError("la salle {} existe déjà".format(ident))
        if not re.search(ZONE_VALIDE, zone):
            raise ValueError("Zone {} invalide".format(zone))
        if not re.search(MNEMONIC_VALIDE, mnemonic):
            raise ValueError("Mnémonique {} invalide ({})".format(mnemonic,
                    MNEMONIC_VALIDE))

        salle = Salle(zone, mnemonic, x, y, z, valide)
        salle.zone.ajouter(salle)
        self.ajouter_salle(salle)
        return salle

    def supprimer_salle(self, cle):
        """Supprime la salle.
        La clé est l'identifiant de la salle.

        """
        salle = self._salles[cle]
        coords = salle.coords
        if coords.valide and coords.tuple() in self._coords.keys():
            del self._coords[coords.tuple()]
        del self._salles[cle]
        salle.detruire()

    def creer_decor(self, cle):
        """Créée un nouveau prototype de décor."""
        cle = cle.lower()
        if cle in self.decors:
            raise ValueError("le décor {} existe déjà".format(repr(cle)))

        decor = PrototypeDecor(cle)
        self.ajouter_decor(decor)
        return decor

    def ajouter_decor(self, decor):
        """Ajoute un prototype de décor."""
        if decor.cle in self.decors:
            raise ValueError("le décor {} existe déjà".format(repr(decor.cle)))

        self.decors[decor.cle] = decor

    def supprimer_decor(self, cle):
        """Supprime un prototype de décor."""
        if cle not in self.decors:
            raise ValueError("le décor {} n'existe pas".format(repr(cle)))

        decor = self.decors[cle]
        del self.decors[cle]
        decor.detruire()

    def creer_bonhomme_neige(self, cle):
        """Créée un nouveau prototype de bonhomme de neige."""
        cle = cle.lower()
        if cle in self.bonhommes_neige or cle in self.decors:
            raise ValueError("le bonhomme de neige {} existe déjà".format(
                    repr(cle)))

        bonhomme = PrototypeBonhommeNeige(cle)
        self.ajouter_bonhomme_neige(bonhomme)
        return bonhomme

    def ajouter_bonhomme_neige(self, bonhomme):
        """Ajoute un prototype de bonhomme de neige."""
        if bonhomme.cle in self.bonhommes_neige:
            raise ValueError("le bonhomme de neige {} existe déjà".format(
                    repr(bonhomme.cle)))

        self.bonhommes_neige[bonhomme.cle] = bonhomme
        self.decors[bonhomme.cle] = bonhomme

    def supprimer_bonhomme_neige(self, cle):
        """Supprime un prototype de bonhomme de neige."""
        if cle not in self.bonhommes_neige:
            raise ValueError("le bonhomme de neige {} n'existe pas".format(
                    repr(cle)))

        bonhomme = self.bonhommes_neige[cle]
        del self.bonhommes_neige[cle]
        bonhomme.detruire()

    def traiter_commande(self, personnage, commande):
        """Traite les déplacements"""

        # Si la commande est vide, on ne se déplace pas
        if len(commande) == 0:
            return False

        commande = supprimer_accents(commande).lower()
        salle = personnage.salle
        try:
            sortie = salle.sorties.get_sortie_par_nom(commande,
                    cachees=False)
        except KeyError:
            pass
        else:
            personnage.deplacer_vers(sortie.nom)
            return True

        for nom, sortie in salle.sorties.iter_couple():
            if sortie and sortie.salle_dest:
                nom = supprimer_accents(sortie.nom).lower()
                if (sortie.cachee and nom == commande) or ( \
                        not sortie.cachee and nom.startswith(commande)):
                    personnage.deplacer_vers(sortie.nom)
                    return True

        if commande in NOMS_SORTIES.keys():
            personnage << "Vous ne pouvez aller par là..."
            return True

        return False

    def changer_ident(self, ancien_ident, nouveau_ident):
        """Change l'identifiant d'une salle"""
        salle = self._salles[ancien_ident]
        del self._salles[ancien_ident]
        self._salles[nouveau_ident] = salle

        # On change la salle de zone si la zone est différente
        a_zone = ancien_ident.split(":")[0]
        n_zone = nouveau_ident.split(":")[0]
        if a_zone != n_zone:
            self.get_zone(a_zone).retirer(salle)
            self.get_zone(n_zone).ajouter(salle)

    def changer_coordonnees(self, ancien_tuple, nouvelles_coords):
        """Change les coordonnées d'une salle.
        Les anciennes coordonnées sont données sous la forme d'un tuple
            (x, y, z, valide)
        Les nouvelles sont un objet Coordonnees.

        """
        a_x, a_y, a_z, a_valide = ancien_tuple
        salle = nouvelles_coords.parent
        if a_valide and (a_x, a_y, a_z) in self._coords:
            # on va supprimer les anciennes coordonnées
            del self._coords[a_x, a_y, a_z]
        if salle and nouvelles_coords.valide:
            self._coords[nouvelles_coords.tuple()] = salle

    def ajouter_terrain(self, nom, survol):
        """Ajoute un terrain."""
        if nom in self.terrains:
            raise KeyError("le terrain {] existe déjà".format(repr(nom)))

        terrain = Terrain(nom, survol)
        self.terrains[nom] = terrain
        return terrain

    def get_terrain(self, nom):
        """Retourne le terrain si trouvé.

        La recherche se fait indépendemment des accents, majuscules et
        minuscules. Si le terrain n'est pas trouvé, retourne None.

        """
        nom = supprimer_accents(nom).lower()
        for terrain in self.terrains.values():
            if supprimer_accents(terrain.nom).lower() == nom:
                return terrain

        return None

    def creer_etendue(self, cle):
        """Crée une étendue d'eau."""
        if cle in self.etendues.keys():
            raise KeyError("l'étendue d'eau {} existe déjà".format(cle))

        etendue = Etendue(cle)
        self.ajouter_etendue(etendue)
        return etendue

    def ajouter_etendue(self, etendue):
        """Ajoute une étendue au dictionnaire."""
        if etendue.cle in self.etendues.keys():
            raise KeyError("l'étendue d'eau {} existe déjà".format(
                    etendue.cle))

        self.etendues[etendue.cle] = etendue

    def supprimer_etendue(self, cle):
        """Supprime l'étendue d'eau."""
        etendue = self.etendues[cle]
        etendue.detruire()
        del self.etendues[cle]

    def creer_obstacle(self, *args, **kw_args):
        """Création d'un obstacle."""
        obstacle = Obstacle(*args, **kw_args)
        self.ajouter_obstacle(obstacle)
        return obstacle

    def ajouter_obstacle(self, obstacle):
        """Ajoute un obstacle dans le dictionnaire du module."""
        if obstacle.nom in self.obstacles:
            raise ValueError("l'obstacle {} existe déjà".format(obstacle.nom))

        self.obstacles[obstacle.nom] = obstacle

    def supprimer_obstacle(self, nom):
        """Détruit l'obstacle."""
        obstacle = self.obstacles[nom]
        obstacle.detruire()
        del self.obstacles[nom]

    def get_zone(self, cle):
        """Retourne la zone correspondante ou la crée."""
        zone = self._zones.get(cle)
        if zone is None:
            zone = Zone(cle)
            self._zones[cle] = zone

        return zone

    def nettoyer_salles(self):
        """Nettoyage des salles et des objets trop vieux."""
        if not self.p_nettoyer:
            return

        importeur.diffact.ajouter_action("net_salles", 300,
                self.nettoyer_salles)
        maintenant = datetime.now()
        for s in self.salles.values():
            objets = [o for o in s.objets_sol._objets if o.nettoyer]
            for o in objets:
                if (maintenant - o.ajoute_a).seconds >= NB_MIN_NETTOYAGE * 60:
                    importeur.objet.supprimer_objet(o.identifiant)

    def repop_salles(self):
        """Méthode chargée de repop les salles."""
        importeur.diffact.ajouter_action("repop_salles", 900,
                self.repop_salles)
        for s in self.salles.values():
            try:
                s.repop()
            except Exception:
                pass

    def allumer_feu(self, salle, puissance=10):
        """Allume un feu dans salle."""
        if not salle.ident in self.feux:
            feu = Feu(salle, puissance)
            self.feux[salle.ident] = feu
        else:
            feu = salle.feux[salle.ident]
        return feu

    def eteindre_feu(self, salle):
        """Eteint un éventuel feu dans salle."""
        if salle.ident in self.feux:
            self.feux[salle.ident].detruire()
            del self.feux[salle.ident]

    def feu_present(self, salle, liste_messages, flags):
        """Si un feu se trouve dans la salle, on l'affiche"""
        if self.feux:
            for feu in self.feux.values():
                if salle is feu.salle:
                    liste_messages.insert(0, str(feu))
                    return

    def tick(self, no):
        """Exécute un tick."""
        self.importeur.diffact.ajouter_action("stick_{}".format(no),
                60, self.tick, no)

        # On sélectionne les salles à tick
        salles = list(self._salles.values())
        tick = []
        i = no - 1
        while i < len(salles):
            try:
                s = salles[i]
            except IndexError:
                pass
            else:
                tick.append(s)
            i += NB_TICKS

        for s in tick:
            s.tick()

    def peut_allumer_feu(self, salle):
        """Retourne si on peut allumer un feu dans cette salle ou non."""
        if not salle.a_detail_flag("cheminée") and (salle.interieur or \
                salle.nom_terrain in self.TERRAINS_SANS_FEU):
            return False

        for affection in salle.affections.values():
            if affection.affection.a_flag("humide"):
                return False

        return True

    def allumer_ou_recharger(self, personnage, utiliser_pierre=True,
            utiliser_niveau=True):
        """Allume ou recharge un feu."""
        salle = personnage.salle
        if "neige" in salle.affections:
            personnage << "|err|Il fait trop humide.|ff|"
            return

        objets_sol = list(salle.objets_sol)
        somme_combu = 0
        for objet in list(objets_sol):
            if objet.est_de_type("combustible"):
                somme_combu += objet.qualite
        if not somme_combu:
            personnage << "|err|Il n'y a rien qui puisse brûler par ici.|ff|"
            return

        # On tente d'allumer ou de nourrir le feu
        if salle.ident in self.feux:
            feu = self.feux[salle.ident]
            feu.puissance += somme_combu
            personnage << "Vous poussez du bois dans le feu et celui-ci " \
                    "gagne en vigueur et en éclat."
            for objet in objets_sol:
                if objet.est_de_type("combustible"):
                    importeur.objet.supprimer_objet(objet.identifiant)
        else:
            if not self.peut_allumer_feu(salle):
                personnage << "|err|Vous ne pouvez pas faire de feu ici.|ff|"
                return

            efficacite_pierre = 100
            if utiliser_pierre:
                pierre = None
                for objet, qtt, t_conteneur in \
                        personnage.equipement.inventaire.iter_objets_qtt(
                        conteneur=True):
                    if objet.est_de_type("pierre à feu"):
                        pierre = objet
                        conteneur = t_conteneur
                        break

                if not pierre:
                    personnage << "|err|Vous ne tenez rien pour allumer.|ff|"
                    return

                efficacite_pierre = pierre.efficacite
                if pierre.efficacite > 0:
                    pierre.efficacite -= 1

            if utiliser_niveau:
                personnage.pratiquer_talent("feu_camp")
                niveau = sqrt(personnage.get_talent("feu_camp") / 100)
            else:
                niveau = 1

            efficace = efficacite_pierre / 50
            proba_marche = random()

            # Si la pierre fonctionne
            if proba_marche <= efficace:
                proba_reussit = round(random(), 1)
                if proba_reussit <= niveau:
                    personnage << "Une étincelle vole et le feu prend."
                    feu = importeur.salle.allumer_feu(salle, somme_combu)
                    personnage.gagner_xp("survie", somme_combu * 20)
                    for objet in objets_sol:
                        if objet.est_de_type("combustible"):
                            if objet.identifiant:
                                importeur.objet.supprimer_objet(
                                        objet.identifiant)
                    feu.stabilite = 1 - niveau ** (1 / 3)
                    return

            personnage << "Le feu refuse de démarrer."
            proba_casse = random()
            solidite = efficace ** (1 / 5)
            if proba_casse >= solidite and utiliser_pierre:
                personnage << "{} se brise en mille morceaux.".format(
                        pierre.nom_singulier)
                conteneur.retirer(pierre)
                importeur.objet.supprimer_objet(pierre.identifiant)

    def inscrire_salle(self, salle):
        """Inscrit la salle dans le changement de temps."""
        if salle.script["changer"]["minute"].tests:
            if salle not in self.ch_minute:
                self.ch_minute.append(salle)
        elif salle in self.ch_minute:
            self.ch_minute.remove(salle)

        if salle.script["changer"]["heure"].tests:
            if salle not in self.ch_heure:
                self.ch_heure.append(salle)
        elif salle in self.ch_heure:
            self.ch_heure.remove(salle)

        if salle.script["changer"]["jour"].tests:
            if salle not in self.ch_jour:
                self.ch_jour.append(salle)
        elif salle in self.ch_jour:
            self.ch_jour.remove(salle)

        if salle.script["changer"]["mois"].tests:
            if salle not in self.ch_mois:
                self.ch_mois.append(salle)
        elif salle in self.ch_mois:
            self.ch_mois.remove(salle)

        if salle.script["changer"]["année"].tests:
            if salle not in self.ch_annee:
                self.ch_annee.append(salle)
        elif salle in self.ch_annee:
            self.ch_annee.remove(salle)

    def changer_minute(self, temps):
        """Hook appelé à chaque changement de minute."""
        minute, heure, jour, mois, annee = temps.minute, temps.heure, \
                temps.jour + 1, temps.mois + 1, temps.annee
        minute = Fraction(minute)
        heure = Fraction(heure)
        jour = Fraction(jour)
        mois = Fraction(mois)
        annee = Fraction(annee)
        for salle in self.ch_minute:
            salle.script["changer"]["minute"].executer(salle=salle,
                    minute=minute, heure=heure, jour=jour, mois=mois,
                    annee=annee)

    def changer_heure(self, temps):
        """Hook appelé à chaque changement d'heure."""
        minute, heure, jour, mois, annee = temps.minute, temps.heure, \
                temps.jour + 1, temps.mois + 1, temps.annee
        minute = Fraction(minute)
        heure = Fraction(heure)
        jour = Fraction(jour)
        mois = Fraction(mois)
        annee = Fraction(annee)
        for salle in self.ch_heure:
            salle.script["changer"]["heure"].executer(salle=salle,
                    minute=minute, heure=heure, jour=jour, mois=mois,
                    annee=annee, exc_interruption=False)

    def changer_jour(self, temps):
        """Hook appelé à chaque changement de jour."""
        minute, heure, jour, mois, annee = temps.minute, temps.heure, \
                temps.jour + 1, temps.mois + 1, temps.annee
        minute = Fraction(minute)
        heure = Fraction(heure)
        jour = Fraction(jour)
        mois = Fraction(mois)
        annee = Fraction(annee)
        for salle in self.ch_jour:
            salle.script["changer"]["jour"].executer(salle=salle,
                    minute=minute, heure=heure, jour=jour, mois=mois,
                    annee=annee)

    def changer_mois(self, temps):
        """Hook appelé à chaque changement de mois."""
        minute, heure, jour, mois, annee = temps.minute, temps.heure, \
                temps.jour + 1, temps.mois + 1, temps.annee
        minute = Fraction(minute)
        heure = Fraction(heure)
        jour = Fraction(jour)
        mois = Fraction(mois)
        annee = Fraction(annee)
        for salle in self.ch_mois:
            salle.script["changer"]["mois"].executer(salle=salle,
                    minute=minute, heure=heure, jour=jour, mois=mois,
                    annee=annee)

    def changer_annee(self, temps):
        """Hook appelé à chaque changement d'année."""
        minute, heure, jour, mois, annee = temps.minute, temps.heure, \
                temps.jour + 1, temps.mois + 1, temps.annee
        minute = Fraction(minute)
        heure = Fraction(heure)
        jour = Fraction(jour)
        mois = Fraction(mois)
        annee = Fraction(annee)
        for salle in self.ch_annee:
            salle.script["changer"]["annee"].executer(salle=salle,
                    minute=minute, heure=heure, jour=jour, mois=mois,
                    annee=annee)

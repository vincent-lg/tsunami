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


"""Fichier contenant le module secondaire navigation."""

# Configuration des loggers
type(importeur).man_logs.creer_logger("navigation", "ordres", "ordres.log")
type(importeur).man_logs.creer_logger("navigation", "monstres", "monstres.log")

import os

from vector import *

from abstraits.module import *
from corps.fonctions import valider_cle
from primaires.format.fonctions import format_nb
from primaires.salle.chemin import Chemin
from primaires.salle.salle import Salle
from primaires.vehicule.vecteur import Vecteur
from secondaires.navigation.config import CFG_TEXTE
from .navire import Navire
from .navire_automatique import NavireAutomatique
from .elements import types as types_elements
from .elements.base import BaseElement
from .vent import Vent
from .visible import Visible
from . import cherchables
from . import commandes
from . import editeurs
from . import masques
from . import types
from .modele import ModeleNavire
from .constantes import *
from .equipage.equipage import Equipage
from .equipage.fiche import FicheMatelot
from .monstre.prototype import PrototypeMonstreMarin, types_monstres
from .chantier_naval import ChantierNaval
from .navires_vente import NaviresVente
from .matelots_vente import MatelotsVente
from .repere import Repere
from .trajet import Trajet

class Module(BaseModule):

    """Module secondaire définissant la navigation.

    Ce module définit les navires, modèles de navires et objets liés.

    """

    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "navigation", "secondaire")
        self.preparer_apres = ["salle"]
        self.commandes = []
        self.cfg = None
        self.fichier_suivi = None
        self.modeles = {}
        self.nav_logger = type(self.importeur).man_logs.creer_logger(
                "navigation", "navires", "navires.log")
        self.navires = {}
        self.navires_automatiques = {}
        self.elements = {}
        self.types_elements = types_elements
        self.vents = {}
        self.vents_par_etendue = {}
        self.fiches = {}
        self.chantiers = {}
        self.trajets = {}
        self.reperes = {}
        self.matelots = {}
        self.types_monstres = types_monstres
        self.monstres = {}
        self.points_ovservables = {
                "cotes": Visible.trouver_cotes,
                "navires": Visible.trouver_navires,
                "reperes": Repere.trouver_reperes,
        }

    def config(self):
        """Configuration du module."""
        self.cfg = type(self.importeur).anaconf.get_config("navigation",
                "navigation/navigation.cfg", "modele navigationt", CFG_TEXTE)
        self.fichier_suivi = self.cfg.fichier_suivi
        self.importeur.scripting.a_charger.append(self)
        his_voile = self.importeur.perso.ajouter_etat("hisser_voile")
        his_voile.msg_refus = "Vous êtes en train de hisser la voile"
        his_voile.msg_visible = "hisse une voile ici"
        his_voile.act_autorisees = ["regarder", "parler"]
        pli_voile = self.importeur.perso.ajouter_etat("plier_voile")
        pli_voile.msg_refus = "Vous êtes en train de replier la voile"
        pli_voile.msg_visible = "replie une voile ici"
        pli_voile.act_autorisees = ["regarder", "parler"]
        ten_gouv = self.importeur.perso.ajouter_etat("tenir_gouvernail")
        ten_gouv.msg_refus = "Vous tenez actuellement le gouvernail"
        ten_gouv.msg_visible = "tient le gouvernail ici"
        ten_gouv.act_autorisees = ["regarder", "parler"]
        u_loch = self.importeur.perso.ajouter_etat("utiliser_loch")
        u_loch.msg_refus = "Vous êtes en train de manipuler le loch"
        u_loch.msg_visible = "manipule le loch ici"
        u_loch.act_autorisees = ["regarder", "parler"]

        ten_rames = self.importeur.perso.ajouter_etat("tenir_rames")
        ten_rames.msg_refus = "Vous tenez actuellement les rames"
        ten_rames.msg_visible = "rame ici"
        ten_rames.act_autorisees = ["regarder", "parler"]

        # Ajout du niveau
        importeur.perso.ajouter_niveau("navigation", "navigation")

        # Ajout des services
        importeur.commerce.types_services["navire"] = NaviresVente()
        importeur.commerce.aides_types["navire"] = \
            "Ce service permet la vente de navires. Vous devez tout " \
            "simplement préciser la clé du modèle de navire. Attention " \
            "cependant : pour que la vente de navires dans ce magasin " \
            "puisse se faire, le magasin doit être relié à un chantier " \
            "naval."
        importeur.commerce.types_services["matelot"] = MatelotsVente()
        importeur.commerce.aides_types["matelot"] = \
            "Ce service permet la vente de matelots. Vous devez tout " \
            "simplement préciser la clé du matelot à mettre en vente " \
            "(sa clé de prototype de PNJ). La fiche du matelot " \
            "correspondant à ce prototype doit avoir été définie au " \
            "préalable."

        BaseModule.config(self)

    def init(self):
        """Chargement des navires et modèles."""
        self.importeur.hook["salle:regarder"].ajouter_evenement(
                self.navire_amarre)
        self.importeur.hook["salle:regarder"].ajouter_evenement(
                self.navire_accoste)
        self.importeur.hook["objet:peut_boire"].ajouter_evenement(
                Navire.peut_boire)
        self.importeur.interpreteur.categories["navire"] = \
                "Commandes de navigation"
        self.importeur.hook["pnj:arrive"].ajouter_evenement(
                self.combat_matelot)
        self.importeur.hook["pnj:meurt"].ajouter_evenement(
                self.rendre_equipage)
        self.importeur.hook["pnj:nom"].ajouter_evenement(
                Equipage.get_nom_matelot)
        self.importeur.hook["salle:trouver_chemins_droits"].ajouter_evenement(
                self.trouver_chemins_droits)
        self.importeur.hook["stats:infos"].ajouter_evenement(
                self.stats_navigation)

        # Ajout des talents
        importeur.perso.ajouter_talent("calfeutrage", "calfeutrage",
                "navigation", 0.5)

        # On récupère les modèles
        modeles = self.importeur.supenr.charger_groupe(ModeleNavire)
        for modele in modeles:
            self.modeles[modele.cle] = modele

        nb_modeles = len(modeles)
        self.nav_logger.info(format_nb(nb_modeles,
                "{nb} modèle{s} de navire récupéré{s}"))

        # On récupère les navires
        navires = self.importeur.supenr.charger_groupe(Navire)
        for navire in navires:
            self.navires[navire.cle] = navire

        nb_navires = len(navires)
        self.nav_logger.info(format_nb(nb_navires,
                "{nb} navire{s} récupéré{s}"))

        # On récupère les navires automatiques
        fiches = self.importeur.supenr.charger_groupe(NavireAutomatique)
        for fiche in fiches:
            self.ajouter_navire_automatique(fiche)

        nb_autos = len(fiches)
        self.nav_logger.info(format_nb(nb_autos,
                "{nb} fiche{s} de navire{s} automatique{s} " \
                "récupérée{s}", fem=True))

        # On récupère les éléments
        elements = self.importeur.supenr.charger_groupe(BaseElement)
        for element in elements:
            self.elements[element.cle] = element

        nb_elements = len(elements)
        self.nav_logger.info(format_nb(nb_elements,
                "{nb} élément{s} de navire récupéré{s}"))

        # On récupère les vents
        vents = self.importeur.supenr.charger_groupe(Vent)
        for vent in vents:
            self.ajouter_vent(vent)

        nb_vents = len(self.vents)
        self.nav_logger.info(format_nb(nb_vents,
                "{nb} vent{s} récupéré{s}"))

        # On récupère les fiches
        fiches = self.importeur.supenr.charger_groupe(FicheMatelot)
        for fiche in fiches:
            self.ajouter_fiche_matelot(fiche)

        nb_mat = len(self.fiches)
        self.nav_logger.info(format_nb(nb_mat,
                "{nb} fiche{s} de matelot récupérée{s}", fem=True))

        # On récupère les trajets
        trajets = self.importeur.supenr.charger_groupe(Trajet)
        for trajet in trajets:
            self.ajouter_trajet(trajet)

        nb_trajets = len(self.trajets)
        self.nav_logger.info(format_nb(nb_trajets,
                "{nb} trajet{s} maritime{s} récupéré{s}"))

        # On récupère les repères
        reperes = self.importeur.supenr.charger_groupe(Repere)
        for repere in reperes:
            self.ajouter_repere(repere)

        nb_reperes = len(self.reperes)
        self.nav_logger.info(format_nb(nb_reperes,
                "{nb} repère{s} récupéré{s}"))

        # On récupère les chantiers navals
        chantiers = self.importeur.supenr.charger_groupe(ChantierNaval)
        for chantier in chantiers:
            self.ajouter_chantier_naval(chantier)

        nb_chantiers = len(chantiers)
        self.nav_logger.info(format_nb(nb_chantiers,
                "{nb} chantier{s} naval{s} récupéré{s}"))

        # On récupère les monstres marins
        # On charge les prototypes
        chemin = os.path.join(self.chemin, "monstre", "types")
        pychemin = "secondaires.navigation.monstre.types"
        print("Explore", chemin)
        for nom_fichier in os.listdir(chemin):
            if nom_fichier.startswith("_") or not nom_fichier.endswith(".py"):
                continue

            nom_fichier = pychemin + "." + nom_fichier[:-3]
            print("Charge", nom_fichier)
            __import__(nom_fichier)

        #modeles = self.importeur.supenr.charger_groupe(ModeleNavire)
        #for modele in modeles:
        #    self.modeles[modele.cle] = modele

        # Ajout des actions différées
        self.importeur.diffact.ajouter_action("dep_navire", TPS_VIRT,
                self.avancer_navires)
        self.importeur.diffact.ajouter_action("vir_navire", 3,
                self.virer_navires)
        self.importeur.diffact.ajouter_action("nauffrages", 5,
                self.nauffrages)
        self.importeur.diffact.ajouter_action("tick_chantiers", 60,
                self.tick_chantiers)
        self.importeur.diffact.ajouter_action("tick_equipages", 1,
                self.tick_equipages)
        self.importeur.diffact.ajouter_action("controle_equipages", 3,
                self.controle_equipages)

        # Ajout des bateaux au module salle
        self.importeur.salle.salles_a_cartographier.append(
                self.get_navires_presents)

        BaseModule.init(self)

    def ajouter_commandes(self):
        """Ajout des commandes dans l'interpréteur"""
        self.commandes = [
            commandes.allure.CmdAllure(),
            commandes.amarre.CmdAmarre(),
            commandes.ancre.CmdAncre(),
            commandes.cale.CmdCale(),
            commandes.calfeutrer.CmdCalfeutrer(),
            commandes.canon.CmdCanon(),
            commandes.chantier.CmdChantier(),
            commandes.debarquer.CmdDebarquer(),
            commandes.detailler.CmdDetailler(),
            commandes.ecoper.CmdEcoper(),
            commandes.eltedit.CmdEltedit(),
            commandes.embarquer.CmdEmbarquer(),
            commandes.equipage.CmdEquipage(),
            commandes.gouvernail.CmdGouvernail(),
            commandes.loch.CmdLoch(),
            commandes.matelot.CmdMatelot(),
            commandes.navire.CmdNavire(),
            commandes.passerelle.CmdPasserelle(),
            commandes.rames.CmdRames(),
            commandes.saborder.CmdSaborder(),
            commandes.shedit.CmdShedit(),
            commandes.vent.CmdVent(),
            commandes.voile.CmdVoile(),
        ]

        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)

        # Ajout des éditeurs
        self.importeur.interpreteur.ajouter_editeur(
                editeurs.matedit.EdtMatedit)
        self.importeur.interpreteur.ajouter_editeur(
                editeurs.eltedit.EdtEltedit)
        self.importeur.interpreteur.ajouter_editeur(editeurs.shedit.EdtShedit)

    def preparer(self):
        """Préparation du module.

        Actions effectuées :
        -   Mise à jour systématique des éléments du navire
        -   Écriture des matelots

        """
        self.nav_logger.info("Mise à jour des navires...")
        for navire in self.navires.values():
            for salle in navire.salles.values():
                for element in salle.elements:
                    element.mettre_a_jour_attributs()
            navire.construire_depuis_modele()
            if not navire.modele.graph:
                navire.modele.generer_graph()
        self.nav_logger.info("... mise à jour des navires terminée.")

        for navire in self.navires.values():
            for matelot in navire.equipage.matelots.values():
                if matelot.personnage:
                    self.matelots[matelot.personnage.identifiant] = matelot
                if matelot.ordres:
                    matelot.nettoyer_ordres()
                    matelot.executer_ordres()

        # On renseigne le terrain récif
        Navire.obs_recif = self.importeur.salle.obstacles["récif"]

    def creer_modele(self, cle):
        """Crée un modèle de navire et l'ajoute dans le dictionnaire.

        Retourne le modèle créé.

        Lève une exception KeyError si le modèle existe déjà.

        """
        valider_cle(cle)
        if cle in self.modeles:
            raise KeyError("le modèle de navire {} existe déjà".format(cle))

        modele = ModeleNavire(cle)
        self.ajouter_modele(modele)
        return modele

    def ajouter_modele(self, modele):
        """Ajoute le modèle de navire dans le dictionnaire."""
        self.modeles[modele.cle] = modele

    def supprimer_modele(self, cle):
        """Supprime le modèle de navire portant la clé passée en paramètre."""
        if cle not in self.modeles:
            raise KeyError("le modèle de navire de clé {} est inconnue".format(
                    cle))

        modele = self.modeles[cle]
        del self.modeles[cle]
        modele.detruire()

    def creer_navire(self, modele):
        """Crée un navire sur le modèle.

        Retourne le navire créé.

        """
        navire = Navire(modele)
        self.ajouter_navire(navire)
        return navire

    def ajouter_navire(self, navire):
        """Ajoute le navire à la liste."""
        self.navires[navire.cle] = navire

    def supprimer_navire(self, cle):
        """Supprime le navire dont la clé est passée en paramètre."""
        if cle not in self.navires:
            raise KeyError("le navire de clé {} est introuvable".format(cle))

        navire = self.navires[cle]
        navire.detruire()
        del self.navires[cle]

    def creer_navire_automatique(self, cle):
        """Crée un navire automatique."""
        fiche = NavireAutomatique(cle)
        self.ajouter_navire_automatique(fiche)
        return fiche

    def ajouter_navire_automatique(self, fiche):
        """Ajoute le navire automatique à la liste."""
        self.navires_automatiques[fiche.cle] = fiche

    def supprimer_navire_automatique(self, cle):
        """Supprime le navire automatique dont la clé est précisée."""
        self.navires_automatiques.pop(cle).detruire()

    def creer_element(self, cle, type_elt):
        """Crée un élément du type indiqué.

        Retourne l'élément créé.

        """
        elt = type_elt(cle)
        self.ajouter_element(elt)
        return elt

    def ajouter_element(self, element):
        """Ajoute l'élément au dictionnaire."""
        self.elements[element.cle] = element

    def supprimer_element(self, cle):
        """Supprime l'élément dont la clé est passée en paramètre."""
        if cle not in self.elements:
            raise KeyError("l'élément de clé {} est introuvable".format(cle))

        element = self.elements[cle]
        element.detruire()
        del self.elements[cle]

    def get_vents_etendue(self, cle):
        """Retourne une liste des vents de l'étendue."""
        return self.vents_par_etendue.get(cle, [])

    def creer_vent(self, etendue, x, y, z, vitesse=1, direction=0):
        """Crée un vent dans une étendue.

        Pour les paramètres, se référez au constructeur de la classe Vent.

        """
        vent = Vent(etendue, x, y, z, vitesse, direction)
        self.ajouter_vent(vent)
        return vent

    def ajouter_vent(self, vent):
        """Ajoute le vent."""
        self.vents[vent.cle] = vent
        self.vents_par_etendue[vent.etendue.cle] = self.vents_par_etendue.get(
                vent.etendue.cle, []) + [vent]

    def supprimer_vent(self, cle):
        """Supprime le vent."""
        vent = self.vents[cle]
        self.vents_par_etendue[vent.etendue.cle].remove(vent)
        del self.vents[cle]
        vent.detruire()

    def creer_fiche_matelot(self, prototype):
        """Crée une fiche de matelot sur un prototype de PNJ."""
        fiche = FicheMatelot(prototype)
        self.ajouter_fiche_matelot(fiche)
        return fiche

    def ajouter_fiche_matelot(self, fiche):
        """Ajoute le matelot."""
        self.fiches[fiche.cle] = fiche

    def supprimer_fiche_matelot(self, cle):
        """Supprime le matelot."""
        self.fiches.pop(cle).detruire()

    def creer_trajet(self, cle):
        """Crée un trajet maritime."""
        if cle in self.trajets:
            raise ValueError("la clé {} est déjà utilisée".format(cle))

        trajet = Trajet(cle)
        self.ajouter_trajet(trajet)
        return trajet

    def ajouter_trajet(self, trajet):
        """Ajoute le trajet."""
        self.trajets[trajet.cle] = trajet

    def supprimer_trajet(self, cle):
        """Supprime le trajet."""
        self.trajets.pop(cle).detruire()

    def creer_repere(self, x, y):
        """Crée un repère."""
        if (x, y) in self.reperes:
            raise ValueError("le repère en {}.{} existe déjà".format(x, y))

        repere = Repere(x, y)
        self.ajouter_repere(repere)
        return repere

    def ajouter_repere(self, repere):
        """Ajoute le repère."""
        self.reperes[(repere.x, repere.y)] = repere

    def supprimer_repere(self, x, y):
        """Supprime le repère."""
        self.reperes.pop((x, y)).detruire()

    def creer_chantier_naval(self, cle):
        """Crée un chantier naval."""
        if cle in self.chantiers:
            raise ValueError("la clé {} est déjà utilisée par un autre " \
                    "chantier".format(cle))

        chantier = ChantierNaval(cle)
        self.ajouter_chantier_naval(chantier)
        return chantier

    def ajouter_chantier_naval(self, chantier):
        """Ajoute un chantier naval."""
        if chantier.cle in self.chantiers:
            raise ValueError("la clé {} est déjà utilisée par un autre " \
                    "chantier".format(chantier.cle))

        self.chantiers[chantier.cle] = chantier

    def supprimer_chantier_naval(self, cle):
        """Suppression d'un chantier naval."""
        if cle not in self.chantiers:
            raise ValueError("la clé {} n'est utilisée par aucun " \
                    "chantier".format(cle))

        self.chantiers.pop(cle).detruire()

    def get_chantier_naval(self, salle):
        """Retourne, si trouvé, le chantier naval lié à cette salle."""
        for chantier in self.chantiers.values():
            if chantier.salle_magasin is salle:
                return chantier

        return None

    def avancer_navires(self):
        """Fait avancer les navires."""
        self.importeur.diffact.ajouter_action("dep_navire", TPS_VIRT,
                self.avancer_navires)
        for navire in self.navires.values():
            if navire.etendue:
                navire.avancer(DIST_AVA)

    def virer_navires(self):
        """Fait virer les navires."""
        self.importeur.diffact.ajouter_action("vir_navire", 3,
                self.virer_navires)
        for navire in self.navires.values():
            if not navire.immobilise:
                orientation = navire.orientation
                if orientation != 0:
                    navire.virer(orientation)

    def nauffrages(self):
        """Gère les nauffrages."""
        self.importeur.diffact.ajouter_action("nauffrages", 5,
                self.nauffrages)
        for navire in list(self.navires.values()):
            for salle in navire.salles.values():
                if salle.noyable and salle.voie_eau == COQUE_OUVERTE:
                    salle.poids_eau = int(salle.poids_eau * 1.1)

            poids = navire.poids
            poids_max = navire.poids_max
            if poids >= poids_max:
                navire.sombrer()
            elif poids > poids_max / 3:
                navire.envoyer("L'eau emplit le navire de plus en plus vite.")

    def tick_chantiers(self):
        """Tick des chantiers navals."""
        self.importeur.diffact.ajouter_action("tick_chantiers", 60,
                self.tick_chantiers)
        for chantier in self.chantiers.values():
            chantier.executer_commandes()

    def tick_equipages(self):
        """Tick des équipages."""
        self.importeur.diffact.ajouter_action("tick_equipages", 1,
                self.tick_equipages)
        equipages = [n.equipage for n in self.navires.values() if \
                len(n.equipage.matelots) > 0]
        for equipage in equipages:
            equipage.tick()

    def controle_equipages(self):
        """Contrôle des équipages."""
        self.importeur.diffact.ajouter_action("controle_equipages", 3,
                self.controle_equipages)
        equipages = [n.equipage for n in self.navires.values() if \
                len(n.equipage.matelots) > 0]
        for equipage in equipages:
            for controle in equipage.controles.values():
                controle.controler()

    def navire_amarre(self, salle, liste_messages, flags):
        """Si un navire est amarré, on l'affiche."""
        if salle.etendue is None or salle.nom_terrain not in TERRAINS_QUAI:
            return

        etendue = salle.etendue
        navires = [n for n in self.navires.values() if n.etendue is etendue]
        for navire in navires:
            for t_salle in navire.salles.values():
                if t_salle.amarre and t_salle.amarre.attachee is salle:
                    e = "" if navire.modele.masculin else "e"
                    liste_messages.insert(0, "{} est amarré{e} ici.".format(
                            navire.desc_survol.capitalize(), e=e))
                    return

    def navire_accoste(self, salle, liste_messages, flags):
        """Si un navire est accosté, on l'affiche."""
        if salle.etendue is None or salle.nom_terrain not in TERRAINS_QUAI:
            return

        try:
            sortie = salle.sorties.get_sortie_par_nom("passerelle")
        except KeyError:
            return

        if sortie and sortie.salle_dest and hasattr(sortie.salle_dest,
                "navire"):
            navire = sortie.salle_dest.navire
            e = "" if navire.modele.masculin else "e"
            liste_messages.insert(0, "{} a accosté{e} ici.".format(
                        navire.desc_survol.capitalize(), e=e))

    def combat_matelot(self, pnj, arrive):
        """Méthode appelé quand un PNJ arrive dans la salle d'un autre.

        On profite de cette méthode (reliée à un hook) pour demander
        à deux matelots de différents équipages de s'attaquer.

        """
        if pnj is not arrive and hasattr(pnj, "identifiant") and \
                hasattr(arrive, "identifiant"):
            if pnj.identifiant in self.matelots and arrive.identifiant in \
                    self.matelots:
                matelot = self.matelots[pnj.identifiant]
                arrive = self.matelots[arrive.identifiant]

    def rendre_equipage(self, pnj, adversaire):
        """Méthode appelée quand un PNJ meurt.

        Cette méthode est appelée quand un PNJ meurt et permet de
        déterminer, si le PNJ est un matelot, si l'équipage doit se
        rendre.

        """
        print(pnj, "meurt tué par", adversaire)

    def get_symbole(self, point):
        """Retourne le symbole correspondant."""
        if isinstance(point, Salle) and point.nom_terrain in \
                TERRAINS_ACCOSTABLES:
            return "#"
        elif isinstance(point, Navire):
            return "*"
        elif isinstance(point, Repere):
            return "~"

        return ""

    def points_navires(self, navire):
        """Retourne un tuple de couples (cooreds, salle).

        Le navire passé en paramètre est à la fois l'exception qui
        n'apparaîtra pas dans le tuple retourné et celui sur lequel
        on se base pour savoir quelle étendue tester.

        """
        etendue = navire.etendue
        navires = [n for n in self.navires.values() if \
                n.etendue is etendue and n is not navire]
        points = []
        for navire in navires:
            for salle in navire.salles.values():
                x, y, z = salle.coords.tuple()
                points.append(((x, y), salle))

        return tuple(points)

    def get_navires_presents(self):
        """Retourne les navires présents sous la forme d'une liste de tuples
        (nom, False, (x, y)) (voir module salle, commande cartographier).

        """
        l_navires = []
        for navire in self.navires.values():
            l_navires.append(("Navire", False, \
                    (round(navire.position.x), round(navire.position.y))))
        return l_navires

    def dernier_ID(self, cle):
        """Retourne la prochaine clé non utilisée d'un modèle.

        Si par exemple on passe en paramètre de cette fonction la clé
        "voilier" et qu'il existe déjà un "voilier_1" et "voilier_2" alors
        on retourne "voilier_3".

        """
        ids = [int(n.cle[len(cle) + 1:]) for n in self.navires.values() if \
                n.cle.startswith(cle + "_")]
        n_id = max(ids) + 1 if ids else 1
        return "{}_{}".format(cle, n_id)

    def distance_min_avec_navires(self, vecteur):
        """Retourne la distance minimum avec tous les navires présents."""
        distances = []
        for navire in self.navires.values():
            for salle in navire.salles.values():
                t_x, t_y, t_z = salle.coords.x, salle.coords.y, salle.coords.z
                t_vecteur = Vector(t_x, t_y, t_z)
                distances.append((t_vecteur - vecteur).mag)

        if distances:
            return min(distances)

        return None

    def ecrire_suivi(self, message):
        """Écrit le message dans le fichier de suivi si défin."""
        try:
            if self.fichier_suivi:
                with open(self.fichier_suivi, "a") as fichier:
                    fichier.write(message + "\n")
        except Exception as err:
            print(err)

    def get_navires_possedes(self, personnage):
        """Retour les navires proches et possédés par le personnage.

        Deux cas sont à distinguer :
        * La salle du personnage est une salle de la terre ferme.
          Dans ce cas, les navires récupérés sont ceux accostés
          (amarrés ou ancrés) dans la même zone. On part du principe
          que, si ils sont dans la même zone, alors ils peuvent être
          joints par sorties.
        * La salle du personnage est une salle de navire : dans ce
          cas, on retourne les autres navires autour, c'est-à-dire
          qui ont une salle à moins de 5 brasses. Cela demande de
          vérifier chaque salle de chaque navire et est surtout utile
          pour recruter des matelots d'un autre navire en mer.

        """
        salle = personnage.salle
        navires = []
        if getattr(salle, "navire", None) is None:
            # Premier cas, salle de la terre ferme
            for navire in importeur.navigation.navires.values():
                if navire.proprietaire is not personnage:
                    continue

                if not navire.accoste:
                    continue

                if navire.point_accostage.nom_zone == salle.nom_zone:
                    navires.append(navire)
        else:
            # Second cas, c'est une salle de navire
            navire = salle.navire
            if navire.accoste:
                return []

            coords = [s.coords.tuple() for s in navire.salles.values()]
            for autre in importeur.navigation.navires.values():
                if navire is autre or autre.proprietaire is not personnage:
                    continue

                for autre_salle in autre.salles.values():
                    tup = salle.coords.tuple()
                    distance = min(mag(tup + c) for c in coords)
                    if distance < 2:
                        navires.append(autre)

        navires.sort(key=lambda n: n.cle)
        return navires

    def trouver_chemins_droits(self, salle, chemins, rayon):
        """Ajoute aux chemins droits."""
        if salle.etendue is None and not hasattr(salle, "navire"):
            return

        o_x, o_y, o_z = salle.coords.tuple()
        salles = []
        if getattr(salle, "navire", None):
            for etendue in importeur.salle.etendues.values():
                salles.extend(list(etendue.cotes.values()))

        if salle.etendue:
            for navire in self.navires.values():
                for t_salle in navire.salles.values():
                    salles.append(t_salle)

        for t_salle in salles:
            if salle is t_salle:
                continue

            d_x, d_y, d_z = t_salle.coords.tuple()
            vecteur = Vecteur(d_x - o_x, d_y - o_y, d_z - o_z)
            if vecteur.norme < rayon:
                sortie = salle.get_sortie(vecteur, t_salle)
                chemin = Chemin()
                chemin.sorties.append(sortie)
                chemins.chemins.append(chemin)

    def stats_navigation(self, infos):
        """Ajoute les stats concernant la navigation."""
        navires = len(self.navires)
        modeles = len(self.modeles)
        matelots = []
        for navire in self.navires.values():
            if navire.equipage:
                matelots.extend(navire.equipage.matelots.values())

        ordres = []
        for matelot in matelots:
            if matelot.ordres:
                ordres.append((matelot, matelot.ordres))

        ordres = sorted(ordres, key=lambda c: len(c[1]), reverse=True)
        nb_ordres = sum(len(c[1]) for c in ordres)
        msg = "|tit|Navigation :|ff|"
        msg += "\n  {} navires construits sur {} modèles".format(
                navires, modeles)
        msg += "\n  {} matelots en jeu".format(len(matelots))
        msg += "\n  {} ordres en cours".format(nb_ordres)
        i = 0
        if ordres:
            msg += "\n  Matelots les plus solicités :"
            for matelot, t_ordres in ordres:
                if i > 2:
                    break

                msg += "\n    {} en {} : {} ordres".format(
                        matelot.personnage and matelot.personnage.identifiant \
                        or "inconnu", matelot.equipage and \
                        matelot.equipage.navire.cle or "inconnu", len(t_ordres))
                i += 1

        infos.append(msg)

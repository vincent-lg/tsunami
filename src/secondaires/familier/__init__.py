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


"""Fichier contenant le module secondaire familier."""

from random import choice

from abstraits.module import *
from primaires.format.fonctions import format_nb
from primaires.salle.salle import FLAGS as FLAGS_SALLE
from secondaires.familier import cherchables
from secondaires.familier import commandes
from secondaires.familier import editeurs
from secondaires.familier.familier import Familier
from secondaires.familier.fiche import FicheFamilier
from secondaires.familier import masques
from secondaires.familier.templates.chevauche import Chevauche
from secondaires.familier.templates.guide import Guide
from secondaires.familier.templates.guide_par import GuidePar
from secondaires.familier import types

class Module(BaseModule):

    """Module secondaire définissant les familiers.

    Les familiers sont, avant tout, des PNJ avec des attributs
    particuliers, comme les matelots pour l'équipage. Ils obéissent
    à un maître et peuvent être utilisés pour certaines actions.
    Ils ont un régime alimentaire particulier et à la différence des
    PNJ stanrads, peuvent mourir de faim ou de soif.

    Les familiers peuvent aussi être des montures (on peut les
    chevaucher pour se déplacer). Il s'agit juste d'un attribut
    supplémentaire des familiers.

    """

    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "familier", "secondaire")
        self.fiches = {}
        self.familiers = {}
        self.commandes = []
        self.logger = self.importeur.man_logs.creer_logger(
                "familier", "familier")

    def config(self):
        """Configuration du module."""
        # Ajout des flags de salle
        FLAGS_SALLE.ajouter("écurie")
        FLAGS_SALLE.ajouter("peut chevaucher")
        FLAGS_SALLE.ajouter("accueille familiers")

        # Ajout des états
        chevauche = self.importeur.perso.ajouter_etat("chevauche", Chevauche)
        chevauche.msg_refus = "Vous chevauchez une monture."
        chevauche.act_autorisees = ["regarder", "poser", "parler", "ingerer",
                "lancersort", "geste", "bouger", "enfourcher"]

        broute = self.importeur.perso.ajouter_etat("broute")
        broute.msg_refus = "Vous broutez de l'herbe..."
        broute.msg_visible = "broute l'herbe ici"
        broute.act_autorisees = ["regarder", "parler", "ingerer",
                "lancersort", "geste", "bouger"]

        chasse = self.importeur.perso.ajouter_etat("chasse")
        chasse.msg_refus = "Vous êtes en train de chasser."
        chasse.msg_visible = "chasse furtivement ici"
        chasse.act_autorisees = ["regarder", "parler", "ingerer",
                "lancersort", "geste", "bouger", "tuer"]

        self.importeur.perso.ajouter_etat("guide", Guide)
        self.importeur.perso.ajouter_etat("guide_par", GuidePar)

        # Ajout du niveau
        importeur.perso.ajouter_niveau("dressage", "dressage")

        BaseModule.config(self)

    def init(self):
        """Chargement des objets du module."""
        # Ajout des talents
        importeur.perso.ajouter_talent("apprivoisement", "apprivoisement",
                "dressage", 0.4)
        # On récupère les fiches de familier
        fiches = self.importeur.supenr.charger_groupe(FicheFamilier)
        for fiche in fiches:
            self.ajouter_fiche_familier(fiche)

        self.logger.info(format_nb(len(fiches),
                "{nb} fiche{s} de familier récupérée{s}", fem=True))

        # On récupère les familiers
        familiers = self.importeur.supenr.charger_groupe(Familier)
        for familier in familiers:
            self.ajouter_familier(familier)

        self.logger.info(format_nb(len(familiers),
                "{nb} familier{s} récupéré{s}"))

        # Ajout de la catégorie de commande
        self.importeur.interpreteur.categories["familier"] = \
                "Familiers et montures"

        # Abonne le module à plusieurs hooks PNJ
        self.importeur.hook["pnj:arrive"].ajouter_evenement(
                self.arrive_PNJ)
        self.importeur.hook["pnj:meurt"].ajouter_evenement(
                self.meurt_PNJ)
        self.importeur.hook["pnj:détruit"].ajouter_evenement(
                self.detruire_pnj)
        self.importeur.hook["pnj:nom"].ajouter_evenement(
                self.get_nom_familier)
        self.importeur.hook["pnj:doit_afficher"].ajouter_evenement(
                self.doit_afficher_pnj)
        self.importeur.hook["pnj:tick"].ajouter_evenement(
                self.tick_PNJ)
        self.importeur.hook["pnj:gagner_xp"].ajouter_evenement(
                self.gagner_xp_PNJ)

        # Abonne le module au déplacement de personnage
        self.importeur.hook["personnage:peut_deplacer"].ajouter_evenement(
                self.peut_deplacer_personnage)
        self.importeur.hook["personnage:deplacer"].ajouter_evenement(
                self.deplacer_personnage)
        self.importeur.hook["personnage:calculer_endurance"].ajouter_evenement(
                self.calculer_endurance)
        self.importeur.hook["personnage:verbe_deplacer"].ajouter_evenement(
                self.get_verbe_deplacer)
        self.importeur.hook["personnage:verbe_arriver"].ajouter_evenement(
                self.get_verbe_arriver)

        BaseModule.init(self)

    def ajouter_commandes(self):
        """Ajout des commandes dans l'interpréteur"""
        self.commandes = [
            commandes.apprivoiser.CmdApprivoiser(),
            commandes.enfourcher.CmdEnfourcher(),
            commandes.familier.CmdFamilier(),
        ]

        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)

        # Ajout des éditeurs
        self.importeur.interpreteur.ajouter_editeur(
                editeurs.famedit.EdtFamedit)

    def creer_fiche_familier(self, cle):
        """Crée une nouvelle fiche de familier."""
        if cle in self.fiches:
            raise ValueError("la fiche de familier {} existe déjà".format(
                    repr(cle)))

        fiche = FicheFamilier(cle)
        self.ajouter_fiche_familier(fiche)
        return fiche

    def ajouter_fiche_familier(self, fiche):
        """Ajoute une fiche de familier."""
        if fiche.cle in self.fiches:
            raise ValueError("la fiche de familier {} existe déjà".format(
                    repr(fiche.cle)))

        self.fiches[fiche.cle] = fiche

    def supprimer_fiche_familier(self, cle):
        """Supprime une fiche de familier."""
        if cle not in self.fiches:
            raise ValueError("la fiche de familier {} n'existe pas".format(
                    repr(cle)))

        self.fiches.pop(cle).detruire()

    def creer_familier(self, pnj):
        """Crée un familier sur un PNJ."""
        if pnj.identifiant in self.familiers:
            raise ValueError("le familier {} existe déjà".format(
                    repr(pnj.identifiant)))

        if pnj.cle not in self.fiches:
            raise ValueError("le pnj {} n'a pas de fiche de familier".format(
                    repr(pnj.cle)))

        familier = Familier(pnj)
        self.ajouter_familier(familier)
        return familier

    def ajouter_familier(self, familier):
        """Ajoute le familier."""
        if familier.identifiant in self.familiers:
            raise ValueError("le familier d'identifiant {} est " \
                    "déjà défini".format(repr(familier.identifiant)))

        self.familiers[familier.identifiant] = familier

    def supprimer_familier(self, identifiant):
        """Supprime un familier."""
        if identifiant not in self.familiers:
            raise ValueError("le familier {} n'existe pas".format(
                    repr(identifiant)))

        self.familiers.pop(identifiant).detruire()

    def arrive_PNJ(self, pnj, personnage):
        """Quand personnage arrive dans la salle de pnj."""
        if "chasse" in pnj.etats and pnj.identifiant in self.familiers:
            familier = self.familiers[pnj.identifiant]
            if familier.peut_attaquer(personnage):
                familier.attaquer(personnage)

    def meurt_PNJ(self, pnj, adversaire):
        """PNJ meurt, tué par personnage.

        Si personnage est un familier carnivore, le nourit.

        """
        identifiant = getattr(adversaire, "identifiant", "")
        salle = pnj.salle
        if identifiant in self.familiers:
            familier = self.familiers[identifiant]
            fiche = familier.fiche
            if fiche.regime == "carnivore":
                # Cherche le cadavre
                cadavres = [o for o in salle.objets_sol if \
                        o.est_de_type("cadavre") and o.pnj is pnj.prototype]
                if len(cadavres) == 0:
                    self.logger.warning("Le familier {} ne peut trouver " \
                            "le cadavre de {}.".format(familier.identifiant,
                            pnj.identifiant))
                    return

                cadavre = cadavres[0]
                salle.envoyer("{{}} dévore promptement {}.".format(
                        cadavre.get_nom()), adversaire)
                familier.diminuer_faim(pnj.niveau / 3)
                familier.diminuer_soif(pnj.niveau / 3)
                salle.objets_sol.retirer(cadavre)
                importeur.objet.supprimer_objet(cadavre.identifiant)

    def detruire_pnj(self, pnj):
        """Détruit le familier si nécessaire."""
        if pnj.identifiant in self.familiers:
            familier = self.familiers[pnj.identifiant]
            if "guide_par" in pnj.etats and familier.maitre:
                personnage = familier.maitre
                personnage.etats.retirer("guide")

            self.supprimer_familier(pnj.identifiant)

    def familiers_de(self, personnage):
        """Retourne une liste des familiers de personnage."""
        return [f for f in self.familiers.values() if f.maitre is personnage]

    def peut_deplacer_personnage(self, personnage, destination, sortie,
            endurance):
        """Retourne True si le personnage peut se déplacer, False sinon.

        Cette méthode est utile pour ajouter la contrainte de déplacement du
        personnage si il est à dos de familier (on ne peut pas rentrer avec
        sa monture dans une pièce en intérieur, sauf certains cas).

        """
        familier = None
        if "chevauche" in personnage.etats:
            etat = personnage.etats.get("chevauche")
            familier = etat.monture
        elif "guide" in personnage.etats:
            etat = personnage.etats.get("guide")
            familier = etat.familier

        if familier:
            pnj = familier.pnj
            if pnj:
                if destination.interieur and not (destination.a_flag(
                        "écurie") or destination.a_flag("peut chevaucher")):
                    personnage.envoyer("|err|{} ne peut aller là.|ff|",
                            pnj)
                    return False
                elif sortie.direction in ("haut", "bas"):
                    personnage.envoyer("|err|{} ne peut aller là.|ff|",
                            pnj)
                    return False
                elif endurance > pnj.stats.endurance:
                    personnage.envoyer("|err|{} est trop fatigué.|ff|", pnj)
                    return False

        return True

    def calculer_endurance(self, personnage, endurance):
        """Retourne l'endurance réelle consommée."""
        if "chevauche" in personnage.etats:
            etat = personnage.etats.get("chevauche")
            monture = etat.monture
            pnj = monture.pnj
            if pnj:
                return 0

    def deplacer_personnage(self, personnage, destination, sortie, endurance):
        """Déplace aussi la monture."""
        familier = None
        if "chevauche" in personnage.etats:
            etat = personnage.etats.get("chevauche")
            familier = etat.monture
        elif "guide" in personnage.etats:
            etat = personnage.etats.get("guide")
            familier = etat.familier

        if familier:
            pnj = familier.pnj
            if pnj:
                pnj.stats.endurance -= endurance
                pnj.salle = destination

    def get_verbe_deplacer(self, personnage, destination):
        """Retourne le verbe de déplacement."""
        if "chevauche" in personnage.etats:
            etat = personnage.etats.get("chevauche")
            monture = etat.monture
            pnj = monture.pnj
            if pnj:
                return "chevauche vers"
        elif "guide" in personnage.etats:
            etat = personnage.etats.get("guide")
            familier = etat.familier
            pnj = familier.pnj
            if pnj:
                return "mène " + pnj.nom_singulier + " vers"

    def get_verbe_arriver(self, personnage, destination):
        """Retourne le verbe d'arriver."""
        if "chevauche" in personnage.etats:
            etat = personnage.etats.get("chevauche")
            monture = etat.monture
            pnj = monture.pnj
            if pnj:
                return "arrive, chevauchant " + pnj.nom_singulier
        elif "guide" in personnage.etats:
            etat = personnage.etats.get("guide")
            familier = etat.familier
            pnj = familier.pnj
            if pnj:
                return "arrive, menant " + pnj.nom_singulier

    def get_nom_familier(self, pnj, personnage):
        """Retourne le nom du familier si personnage est son maître."""
        familier = self.familiers.get(pnj.identifiant)
        if familier and familier.maitre is personnage:
            return familier.nom

    def doit_afficher_pnj(self, pnj):
        """Retourne True si doit afficher le PNJ, False sinon."""
        familier = self.familiers.get(pnj.identifiant)
        if familier and familier.chevauche_par:
            return False
        if "guide_par" in pnj.etats:
            return False

        return True

    def tick_PNJ(self, pnj):
        """Si le PNJ est un familier, lui donne faim et soif.

        Si le familier est en train de brouter l'herbe ou de chasser,
        il le fait bouger également.
        Sinon, le familier va peut-être se mettre à chasser ou à brouter de
        sa propre initiative.

        """
        identifiant = getattr(pnj, "identifiant", "")
        if identifiant in self.familiers:
            familier = self.familiers[identifiant]
            fiche = familier.fiche
            if "chasse" in pnj.etats:
                self.faire_chasser(familier)
            elif "broute" in pnj.etats:
                self.faire_brouter(familier)
            elif familier.maitre is None or not \
                    familier.maitre.est_connecte():
                if pnj.etats:
                    pass
                elif fiche.regime == "carnivore":
                    pnj.etats.ajouter("chasse")
                elif fiche.regime == "herbivore":
                    pnj.etats.ajouter("broute")

            if fiche.regime in ("herbivore", "carnivore"):
                self.donner_faim_soif(familier)

    def faire_chasser(self, familier):
        """Fait chasser le familier."""
        pnj = familier.pnj
        salle = pnj.salle

        if "combat" in pnj.etats:
            return

        # On cherche les sorties possible de déplacement
        preferes = []
        sorties = []
        for sortie in salle.sorties:
            if sortie.direction not in ("bas", "haut") and \
                    sortie.salle_dest and sortie.salle_dest.nom_terrain == \
                    salle.nom_terrain and not sortie.salle_dest.interieur:
                sorties.append(sortie)

                for personnage in sortie.salle_dest.personnages:
                    if familier.peut_attaquer(personnage):
                        preferes.append(sortie)
                        break

        if preferes:
            sortie = choice(preferes)
        elif sorties:
            sortie = choice(sorties)
        else:
            return

        pnj.deplacer_vers(sortie.nom)

        # On analyse le nouvel environnement
        for personnage in pnj.salle.personnages:
            if familier.peut_attaquer(personnage):
                familier.attaquer(personnage)
                return

    def faire_brouter(self, familier):
        """Fait brouter un familier herbivore."""
        pnj = familier.pnj
        salle = pnj.salle

        if "combat" in pnj.etats:
            return

        # On cherche les sorties possible de déplacement
        sorties = []
        for sortie in salle.sorties:
            if sortie.direction not in ("bas", "haut") and \
                    sortie.salle_dest and sortie.salle_dest.nom_terrain in \
                    ("rive", "plaine") and not sortie.salle_dest.interieur:
                sorties.append(sortie)

        if sorties:
            sortie = choice(sorties)
        else:
            return

        pnj.deplacer_vers(sortie.nom)
        familier.diminuer_faim(1)
        familier.diminuer_soif(1)

    def donner_faim_soif(self, familier):
        """Donne faim et soif au familier."""
        pnj = familier.pnj
        salle = pnj.salle
        if not salle.a_flag("écurie"):
            familier.augmenter_faim(0.07)
            familier.augmenter_soif(0.12)
            if familier.faim > 100 or familier.soif > 100:
                pnj = familier.pnj
                if pnj is None:
                    return

                salle = pnj.salle
                salle.envoyer("{} est terrassé par le manque de nourriture.",
                        pnj)
                pnj.mourir()

    def gagner_xp_PNJ(self, pnj, niveau, xp, retour):
        """Le PNJ gagne de l'XP."""
        identifiant = getattr(pnj, "identifiant", "")
        salle = pnj.salle
        if identifiant in self.familiers:
            familier = self.familiers[identifiant]
            while pnj.points_entrainement != 0:
                stats = ["force", "agilite", "robustesse", "intelligence"]
                selections = []
                for nom in stats:
                    stat = pnj.stats[nom]
                    if stat.base < stat.marge_max:
                        selections.append(nom)

                if not selections:
                    return

                stat = choice(selections)
                self.logger.info("{} gagne en {}.".format(pnj.identifiant,
                        stat))
                pnj.gagner_stat(stat)

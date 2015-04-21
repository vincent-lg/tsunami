# -*-coding:Utf-8 -*

# Copyright (c) 2015 LE GOFF Vincent
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


"""Fichier contenant le module secondaire crafting."""

from abstraits.module import *
from corps.fonctions import valider_cle
from primaires.format.fonctions import format_nb
from primaires.interpreteur.editeur.tableau import Tableau
from secondaires.crafting import commandes
from secondaires.crafting.configuration import Configuration
from secondaires.crafting import editeurs
from secondaires.crafting.extension import Extension
from secondaires.crafting.guilde import Guilde
from secondaires.crafting.membres import Membres
from secondaires.crafting import type as def_type
from secondaires.crafting.type import Type

class Module(BaseModule):

    """Module gérant l'ensemble du crafting sur Vancia.

    Le crafting recouvre la gestion de guildes artisanales ou
    politiques. Une définition complète, ainsi que le plan de
    développement de cette amélioration, se trouve ici :
    http://redmine.kassie.fr/issues/130

    """

    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "crafting", "secondaire")
        self.guildes = {}
        self.membres = None
        self.types = {}
        self.logger = self.importeur.man_logs.creer_logger(
                "crafting", "guilde")

    def config(self):
        """Configuration du module."""
        # Extension du crafting
        self.importeur.scripting.a_charger.append(self)

        # Ajout du niveau
        importeur.perso.ajouter_niveau("profession", "profession")

        # Récupération de la configuration crafting YML
        crafting = importeur.supenr.fichiers.get("crafting")
        if crafting:
            self.types = crafting.get("types", [])
        else:
            self.logger.info("Création du fichier YML de crafting")
            self.enregistrer_YML()

        # Création des types dynamiques
        complet = False
        while not complet:
            complet = True
            for nom, informations in self.types.items():
                parent = informations["parent"]
                try:
                    importeur.objet.get_type(parent)
                except KeyError:
                    complet = False
                    continue

                try:
                    importeur.objet.get_type(nom)
                except KeyError:
                    attributs = informations.get("attributs", [])
                    classe = Type.creer_type(parent, nom, attributs)
                    setattr(def_type, classe.__name__, classe)

        BaseModule.config(self)

    def init(self):
        """Chargement des objets du module."""
        guildes = self.importeur.supenr.charger_groupe(Guilde)
        for guilde in guildes:
            self.ajouter_guilde(guilde)

        self.logger.info(format_nb(len(guildes),
                "{nb} guilde{s} récupérée{s}", fem=True))

        self.membres = self.importeur.supenr.charger_unique(Membres)
        if self.membres is None:
            self.membres = Membres()

        self.configuration = self.importeur.supenr.charger_unique(
                Configuration)
        if self.configuration is None:
            self.configuration = Configuration()

        # Connexion aux hooks
        self.importeur.hook["personnage:score"].ajouter_evenement(
                self.etendre_score)
        self.importeur.hook[
                "personnage:points_apprentissage"].ajouter_evenement(
                self.ajouter_points_apprentissage)
        self.importeur.hook["editeur:etendre"].ajouter_evenement(
                self.ajouter_attributs)
        self.importeur.hook["editeur:etendre"].ajouter_evenement(
                Extension.etendre_editeur)

        # Ajout de la catégorie de commande
        self.importeur.interpreteur.categories["profession"] = \
                "Commandes de profession"

        BaseModule.init(self)

    def ajouter_commandes(self):
        """Ajout des commandes dans l'interpréteur"""
        self.commandes = [
            commandes.guilde.CmdGuilde(),
        ]

        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)

        # Ajout des éditeurs
        self.importeur.interpreteur.ajouter_editeur(
                editeurs.gldedit.GldEdit)

    def preparer(self):
        """On ajoute les guildes déjà ouvertes."""
        guildes = self.guildes_ouvertes
        for guilde in guildes:
            guilde.ouvrir()

        self.logger.info(format_nb(len(guildes),
                "{nb} guilde{s} ouverte{s}", fem=True))

        # Ajout des commandes dynamiques
        nb_cmd = 0
        for guilde in self.guildes.values():
            for commande in guilde.commandes:
                commande.ajouter()
                commande.maj()
                nb_cmd += 1

        self.logger.info(format_nb(nb_cmd,
                "{nb} commande{s} dynamique{s} créée{s}", fem=True))

    @property
    def guildes_ouvertes(self):
        """Retourne la liste des guildes ouvertes."""
        return [g for g in self.guildes.values() if g.ouverte]

    def creer_guilde(self, cle):
        """Crée une guilde."""
        valider_cle(cle)

        if cle in self.guildes:
            raise ValueError("la guilde {} existe déjà".format(
                    repr(cle)))

        guilde = Guilde(cle)
        self.ajouter_guilde(guilde)
        return guilde

    def ajouter_guilde(self, guilde):
        """Ajoute la guilde."""
        if guilde.cle in self.guildes:
            raise ValueError("la guilde de clé {} est " \
                    "déjà définie".format(repr(guilde.cle)))

        self.guildes[guilde.cle] = guilde

    def supprimer_guilde(self, cle):
        """Supprime une guilde."""
        if cle not in self.guildes:
            raise ValueError("la guilde {} n'existe pas".format(
                    repr(cle)))

        self.guildes.pop(cle).detruire()

    def get_points_guilde_disponibles(self, personnage):
        """Retourne les points de guilde disponibles.

        La somme des points de guilde déjà consommés (en fonction
        des guildes rejointes et du rang dans chacune) est soustraite
        au nombre de points disponibles. Cette méthode retourne
        un nombre négatif si il y a eu trop de points consommés
        par rapport aux points disponibles.

        """
        points = self.membres.points_guilde
        malus = self.membres.malus.get(personnage, 0)
        points -= malus

        for progression in self.membres.membres.get(personnage, []):
            points -= progression.rang.total_points_guilde

        return points

    def etendre_score(self, personnage, msgs):
        """Extension du score pour le crafting.

        On affiche deux informations :
            Le nombre de points de guilde disponibles
            Les différents rangs actuels

        """
        points = self.get_points_guilde_disponibles(personnage)
        if points < 0:
            points = 0

        msgs.append("Points de guilde disponibles : {:>3}".format(
                points))

        progressions = self.membres.membres.get(personnage, [])
        if progressions:
            msgs.append("")

            progressions = sorted(progressions,
                    key=lambda p: p.rang.guilde.nom)
            for progression in progressions:
                msgs.append("{} de {}".format(
                        progression.rang.nom.capitalize(),
                        progression.rang.guilde.nom))

        msgs.append("")

    def ajouter_points_apprentissage(self, personnage):
        """Ajoute des points d'apprentissage disponibles.

        Cette méthode retourne 0 si le personnage n'est dans aucune
        guilde. Sinon, retourne un nombre (50 fois le nombre de
        talents disponibles dans la guilde).

        """
        nb = 0
        progressions = self.membres.membres.get(personnage, [])
        for progression in progressions:
            guilde = progression.rang.guilde
            nb += len(guilde.talents_fermes) * 50

        return nb

    def enregistrer_YML(self):
        """Enregistrement de la configuration YML."""
        self.types = {}

        for guilde in self.guildes.values():
            for type in guilde.types:
                self.types[type.nom] = {
                        "parent": type.parent,
                        "attributs": type.attributs,
                }

        importeur.supenr.sauver_fichier("crafting", {
                "types": self.types,
        })

    def ajouter_attributs(self, editeur, presentation, objet):
        """Ajoute l'éditeur d'attributs à l'objet."""
        if editeur == "objet":
            lst_attributs = list(getattr(objet,
                    "attributs_crafting", []))
            attributs = presentation.ajouter_choix("attributs", "at",
                    Tableau, importeur.crafting.configuration[objet],
                    "attributs", (("attribut", lst_attributs),
                    ("valeur", "chaîne")))
            attributs.parent = presentation
            attributs.aide_courte = \
                "Vous pouvez configurer ici les attributs de " \
                "l'objet.\nLa liste d'attributs configurée dans le " \
                "type est la suivante :\n" + ", ".join(lst_attributs) + "\n" \
                "Entrez |ent|le nom de l'attribut|ff|, un signe |ent|/|ff| " \
                "et\nsa valeur pour la modifier. Par exemple : " \
                "|cmd|couleur / rouge|ff|.\n\nAttributs actuels :\n{valeur}"

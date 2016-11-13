# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 LE GOFF Vincent
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


"""Package contenant l'éditeur 'famedit'.

Si des redéfinitions de contexte-éditeur standard doivent être faites, elles
seront placées dans ce package

"""

from textwrap import dedent

from primaires.interpreteur.editeur.choix import Choix
from primaires.interpreteur.editeur.entier import Entier
from primaires.interpreteur.editeur.flag import Flag
from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.selection import Selection
from primaires.interpreteur.editeur.tableau import Tableau
from primaires.interpreteur.editeur.uniligne import Uniligne
from primaires.scripting.editeurs.edt_script import EdtScript
from secondaires.familier.tours import TOURS
from secondaires.familier.constantes import *

class EdtFamedit(Presentation):

    """Classe définissant l'éditeur de fiche de familier famedit."""

    nom = "famedit"

    def __init__(self, personnage, fiche):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None

        Presentation.__init__(self, instance_connexion, fiche)
        if personnage and fiche:
            self.construire(fiche)

    def __getnewargs__(self):
        return (None, None)

    def construire(self, fiche):
        """Construction de l'éditeur"""
        # Régimes
        regime = self.ajouter_choix("régime alimentaire", "r", Choix, fiche,
                "regime", REGIMES)
        regime.parent = self
        regime.prompt = "Régime alimentaire du familier : "
        regime.apercu = "{objet.regime}"
        regime.aide_courte = \
            "Entrez le |ent|régime|ff| du familier ou |cmd|/|ff| pour revenir " \
            "à la fenêtre parente.\n\nRégimes disponibles : {}.\n\n" \
            "Régime actuel : |bc|{{objet.regime}}|ff|".format(
            ", ".join(REGIMES))

        # Tours
        noms = ", ".join(list(TOURS.keys()))
        tours = self.ajouter_choix("tours", "t", Tableau,
                fiche, "aptitudes",
                (("Tour", list(TOURS.keys())), ("Niveau", "entier")))
        tours.parent = self
        tours.apercu = "{valeur}"
        tours.aide_courte = dedent("""
            Entrez |cmd|/|ff| pour revenir à la fenêtre parente.

            Vous pouvez configurer ici les tours du familier. Le
            tableau ci-dessous représente les tours du familier
            et le niveau à partir duquel ce tour est active.
            Notez qu'un familier peut posséder un tour avant d'atteindre
            le niveau spécifié, si le maître a suffisamment de charisme.
            Si vous voulez qu'un familier ait l'tour dès son apparition,
            précisez un niveau de 1 (les PNJ ne peuvent pas avoir un niveau
            inférieur). Un niveau au-delà de 100 n'aura aucun effet.
            Tours existantes : {noms}.
            Pour ajouter une ligne dans le tableau, entrez le nom du
            tour, un signe |cmd|/|ff| et le niveau d'activation
            du tour. Par exemple :
             |ent|suivre_maitre / 30|ff|
            Utilisez l'option |ent|/s|ff| suivi du nom du tour
            pour l'effacer de ce tableau. Par exemple :
             |cmd|/s suivre_maitre|ff|
            Tours configurées pour ce familier :
            {{valeur}}
        """.strip("\n").format(noms=noms))

        # Harnachements supportés
        harnachements = self.ajouter_choix("harnachement supportés", "h",
                Selection, fiche, "harnachements", TYPES_HARNACHEMENT)
        harnachements.parent = self
        harnachements.prompt = "Harnachements supportés : "
        harnachements.apercu = "{objet.str_harnachements}"
        harnachements.aide_courte = \
            "Entrez un |ent|harnachement supporté|ff| pour l'ajouter " \
            "ou le retirer\nou |cmd|/|ff| pour revenir à la fenêtre " \
            "parente.\n\nHarnachements possibles : " + \
            ", ".join(sorted(TYPES_HARNACHEMENT)) + "\nHarnachements " \
            "supportés actuellement : {objet.str_harnachements}"

        # Stats pouvant progresser
        stats = self.ajouter_choix("stats pouvant progresser", "s",
                Tableau, fiche, "stats_progres",
                ((("Stat", ["force", "agilite", "robustesse", "intelligence",
                "charisme", "sensibilite"])), ("Probabilité", "entier")))
        stats.parent = self
        stats.prompt = "Stats pouvant augmenter automatiquement : "
        stats.apercu = "\n{objet.str_stats_progres}"
        stats.aide_courte = dedent("""
            Entrez |cmd|/|ff| pour revenir à la fenêtre parente.

            Vous pouvez ici préciser les stats à entaîner automatiquement
            au passage du niveau du familier, selon certaines probabilités.
            Vous pouvez configurer certaines stats pour être plus probables
            que d'autres dans l'entraînement. Précisez en premier paramètre
            le nom de la stat (comme force, agilité, ...) et en second,
            après un signe |cmd|/|ff|, la probabilité. Au passage du
            niveau, la probabilité de choisir cette stat dépendra de la
            probabilité totale.

            Pour ajouter ou modifier une ligne :
                |ent|nom de la stat / probabilité|ff|

            Vous pouvez supprimer une ligne en entrant l'option |cmd|/s|ff|
            suivie du numéro de la ligne à supprimer.

            Probabilités actuelles :
            {valeur}
        """.strip("\n"))

        # Aliments supplémentaires
        aliments_sup = []
        noms_types = ["appât"] + list(importeur.objet.get_types_herites(
                "nourriture"))
        for nom_type in noms_types:
            aliments_sup.append("+" + nom_type)
            for prototype in importeur.objet.get_prototypes_de_type(nom_type):
                aliments_sup.append(prototype.cle)

        aliments = self.ajouter_choix("aliments supplémentaires", "al",
                Selection, fiche, "peut_manger", aliments_sup)
        aliments.parent = self
        aliments.prompt = "Aliments que l'on peut donner au familier " \
                "pour qu'il se nourrisse : "
        aliments.apercu = "{valeur}"
        aliments.aide_courte = dedent("""\
            Entrez |cmd|/|ff| pour revenir à la fenêtre parente.

            Pour ajouter ou retirer un aliment, entrez simplement sa clé,
            comme |ent|pomme_rouge|ff|, ou son type précédé d'un signe
            |ent|+|ff|, comme |ent|+légume|ff|. Si un nom de type est
            précisé, le maître du familier pourra nourrir celui-ci en
            utilisant n'importe quel objet de ce type.

            Aliments actuels : {valeur}""")

        # Monture
        monture = self.ajouter_choix("peut être monté", "m", Flag, fiche,
                "monture")
        monture.parent = self

        # Sorties verticales
        verticales = self.ajouter_choix(
                "peut emprunter les sorties verticales", "v", Flag, fiche,
                "sorties_verticales")
        verticales.parent = self

        # Aller en intérieur
        interieur = self.ajouter_choix("peut aller en intérieur", "l",
                Flag, fiche, "aller_interieur")
        interieur.parent = self

        # Difficulté d'apprivoisement
        difficulte = self.ajouter_choix("difficulté d'apprivoisement", "d",
                Entier, fiche, "difficulte_apprivoisement")
        difficulte.parent = self
        difficulte.apercu = "{objet.difficulte_apprivoisement}%"
        difficulte.prompt = "Entrez la difficulté d'apprivoisement du " \
                "familier : "
        difficulte.aide_courte = \
            "Entrez |ent|la difficulté d'apprivoisement|ff| du familier\n" \
            "(entre |ent|1|ff| et |ent|100|ff|) ou |cmd|/|ff| pour " \
            "revenir à la fenêtre parente.\n\nDifficulté actuelle : " \
            "{objet.difficulte_apprivoisement}%"

        # Prix unitaire
        prix = self.ajouter_choix("prix unitaire", "u",
                Entier, fiche, "m_valeur")
        prix.parent = self
        prix.apercu = "{objet.m_valeur} pièces de bronze"
        prix.prompt = "Entrez le prix unitaire du familier : "
        prix.aide_courte = \
            "Entrez |ent|le prix unitaire|ff| du familier" \
            "ou |cmd|/|ff| pour revenir à la fenêtre parente.\n\n" \
            "Prix unitaire actuel : {objet.m_valeur}"

        # Script
        scripts = self.ajouter_choix("scripts", "sc", EdtScript,
                fiche.script)
        scripts.parent = self

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


"""Fichier contenant le contexte éditeur EdtStats"""

from textwrap import dedent

from corps.aleatoire import choix_probable_liste
from primaires.interpreteur.editeur import Editeur
from primaires.format.fonctions import contient

class EdtStats(Editeur):

    """Classe définissant le contexte éditeur 'stats'.

    Ce contexte permet d'éditer les stats d'une race.

    """

    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.ajouter_option("e", self.opt_egaliser)

    def opt_egaliser(self, arguments):
        """Égalise les stats.

        Syntaxe :
            /e (<modificateurs de stat>)

        """
        # Restore les stats à leur valeur par défaut
        modele = importeur.perso.modele_stats
        for stat in self.objet:
            defaut = getattr(modele, "_{}".format(stat.nom)).defaut
            stat.defaut = defaut
            stat.courante = defaut

        dispo = importeur.perso.gen_niveaux.points_entrainement_disponibles(
                self.objet.parent.niveau)
        consommes = importeur.perso.gen_niveaux.points_entrainement_consommes(
                self.objet.parent)
        nb = dispo - consommes
        stats = list(importeur.perso.gen_niveaux.stats_entrainables.keys())
        if not arguments.strip():
            arguments = " ".join(stats)


        # Traitement des modificateurs
        modificateurs = arguments.split(" ")
        poids = {}
        for modificateur in modificateurs:
            nombre = 1
            try:
                modificateur, nombre = modificateur.split("=")
            except ValueError:
                pass

            # On recherche la stat
            stat = None
            for nom in stats:
                if contient(nom, modificateur):
                    stat = nom
                    break

            if stat is None:
                self.pere << "|err|Stat {} inconnue.|ff|".format(
                        repr(modificateur))
                return

            # Conversion du nombre
            try:
                nombre = int(nombre)
                assert nombre >= 0
            except (ValueError, AssertionError):
                self.pere << "Nombre {} invalide.|ff|".format(nombre)
                return

            # Modification du poids
            ancien = poids.get(stat)
            if nombre == 0:
                if ancien:
                    del poids[stat]
            else:
                ancien = ancien if ancien else 0
                nombre = ancien + nombre
                poids[stat] = nombre

        print("Poids de modification", poids)
        i = 0
        while i < nb:
            i += 1
            selections = []
            for nom in list(poids.keys()):
                stat = self.objet[nom]
                if stat.base >= stat.marge_max:
                    del poids[stat.nom]

            if not poids:
                self.pere << "|err|Impossible de répartir les stats.|ff|"
                return

            noms = list(poids.keys())
            probas = list(poids.values())
            stat = choix_probable_liste(noms, probas)
            stat = self.objet[stat]
            courante = stat.courante + 1
            stat.courante = courante
            stat.defaut = courante

            # On entraîne la stat liée
            liee = importeur.perso.cfg_stats.entrainement_liees.get(stat.nom)
            if liee:
                stat_liee = self.objet[liee]
                stat_liee.courante = stat_liee.courante + stat.courante
                stat_liee.defaut = stat_liee.courante + stat.courante

        self.actualiser()

    def accueil(self):
        """Message d'accueil"""
        dispo = importeur.perso.gen_niveaux.points_entrainement_disponibles(
                self.objet.parent.niveau)
        consommes = importeur.perso.gen_niveaux.points_entrainement_consommes(
                self.objet.parent)
        msg = dedent("""
            Entrez |cmd|/|ff| pour revenir à la fenêtre parente.

            Vous pouvez ici modifier les |ent|stats|ff| de ce prototype
            de PNJ. Entrez le nom de la stat, un espace et sa nouvelle
            valeur pour la modifier. Par exemple |cmd|force 30|ff|.
            Vous pouvez aussi utiliser les signes |cmd|+|ff| et |cmd|-|ff|
            pour ajouter ou retirer des valeurs aux stats, comme par
            exemple |cmd|force + 5|ff|. Dans tous les cas, vous pouvez
            abréger le nom des stats.

            Si vous avez configuré le niveau du PNJ, vous pouvez utiliser
            l'option |ent|/e|ff| qui est un égaliseur de stats. Les
            stats sont calculées aléatoirement en fonction du niveau
            et des points d'entraînement disponibles. Vous pouvez aussi
            utiliser l'égaliseur en précisant des probabilités pour
            jouer sur l'aléatoire. Par exemple :
                |cmd|/e force=3 agilite=2 intelligence charisme sensibilité|ff|
            Utilisera l'égaliseur aléatoire de stats, avec la force
            ayant un poids de 3, l'agilité un poids de 2 et les autres
            stats un poids de 1. Là encore, vous pouvez abréger le nom
            des stats.

            Points d'entraînements consommés : {} / {} ({}%)

        """).lstrip("\n").format(consommes, dispo,
                round(consommes / dispo * 100))

        stats = self.objet
        msg += "+-" + "-" * 20 + "-+-" + "-" * 6 + "-+\n"
        msg += "| " + "Nom".ljust(20) + " | " + "Valeur".ljust(6) + " |\n"
        msg += "| " + " ".ljust(20) + " | " + " ".ljust(6) + " |"
        for stat in stats:
            if not stat.max:
                msg += "\n| |ent|" + stat.nom.ljust(20) + "|ff| | "
                msg += str(stat.defaut).rjust(6) + " |"

        return msg

    def interpreter(self, msg):
        """Interprétation du message"""
        operateur = "="

        if "+" in msg:
            operateur = "+"
            msg = msg.replace("+", "")
        elif "-" in msg:
            operateur = "-"
            msg = msg.replace("-", "")

        while "  " in msg:
            msg = msg.replace("  ", " ")

        try:
            nom_stat, valeur = msg.split(" ")
        except ValueError:
            self.pere << "|err|Syntaxe invalide.|ff|"
        else:
            # On cherche la stat
            stat = None
            for t_stat in self.objet:
                if not t_stat.max and contient(t_stat.nom, nom_stat):
                    stat = t_stat
                    break

            if not stat:
                self.pere << "|err|Cette stat est introuvable.|ff|"
            else:
                # Convertion
                try:
                    valeur = int(valeur)
                except ValueError:
                    self.pere << "|err|Valeur invalide.|ff|"
                else:
                    if operateur == "+":
                        valeur = stat.courante + valeur
                    elif operateur == "-":
                        valeur = stat.courante - valeur

                    try:
                        assert valeur > 0
                        assert valeur >= stat.marge_min
                        assert valeur <= stat.marge_max
                    except ValueError:
                        self.pere << "|err|Valeur invalide.|ff|"
                    else:
                        stat.defaut = valeur
                        stat.courante = valeur
                        self.actualiser()

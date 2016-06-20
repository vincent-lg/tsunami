# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 DAVY Guillaume
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


"""Fichier contenant la classe Sort, détaillée plus bas."""

from fractions import Fraction
from math import ceil
from random import random

from abstraits.obase import *
from corps.aleatoire import varier
from primaires.format.description import Description
from primaires.scripting.exceptions import InterrompreCommande
from .script import ScriptSort

STANDARD = 0
OFFENSIF = 1

class Sort(BaseObj):

    """Classe représentant un sortilège.

    """

    nom_scripting = "le sort"
    def __init__(self, cle, parent=None):
        """Constructeur du sort"""
        BaseObj.__init__(self)
        self.parent = parent
        self.cle = cle
        self.nom = "sortilège"
        self.description = Description(parent=self)
        self.offensif = False
        self.elements = []
        self.stats = []
        self.type = "destruction"
        self._type_cible = "aucune"
        self.cout = 10
        self.duree = 3
        self.difficulte = 0
        self.distance = False
        self.points_tribut = 1
        self.script = ScriptSort(self)
        self._construire()

    def __getnewargs__(self):
        return ("", )

    def __repr__(self):
        return self.cle

    def __str__(self):
        return "sort:" + self.cle

    def _get_type_cible(self):
        """Retourne le type de cible."""
        return self._type_cible
    def _set_type_cible(self, nouveau_type):
        """Change le type de cible et la variable cible du script."""
        self._type_cible = nouveau_type
        if nouveau_type == "aucune":
            for evt in self.script.evenements.values():
                evt.supprimer_variable("cible")
        elif nouveau_type == "personnage":
            for evt in self.script.evenements.values():
                var_cible = evt.ajouter_variable("cible", "Personnage")
                var_cible.aide = "le personnage ciblé par le sort"
        elif nouveau_type == "objet":
            for evt in self.script.evenements.values():
                var_cible = evt.ajouter_variable("cible", "Objet")
                var_cible.aide = "l'objet ciblé par le sort"
        elif nouveau_type == "salle":
            for evt in self.script.evenements.values():
                var_cible = evt.ajouter_variable("cible", "Salle")
                var_cible.aide = "la salle ciblée par le sort"
    type_cible = property(_get_type_cible, _set_type_cible)

    @property
    def str_elements(self):
        return ", ".join(sorted(self.elements))

    @property
    def str_stats(self):
        if self.stats:
            return ", ".join(self.stats)

        return "aucune"

    @classmethod
    def get_variables(self, cible=None):
        """Retourne un dictionnaire de variables pré-rempli avec la cible.

        Si la cible est None, le dictionnaire sera vide.

        """
        variables = {}
        if cible is not None:
            variables["cible"] = cible

        return variables

    def echoue(self, personnage, cible):
        """Détermine si personnage réussit ou non à lancer ce sort."""
        maitrise = (100 - personnage.sorts.get(self.cle, 0)) / 100
        difficulte = self.difficulte / 100
        if random() < difficulte * maitrise:
            return True

        if self.offensif and self.type_cible == "personnage":
            stat_lanceur = 0
            stat_cible = 0
            for nom_stat in self.stats:
                stat_lanceur += varier(getattr(personnage.stats, nom_stat), 10)
                stat_cible += varier(getattr(cible.stats, nom_stat), 10)

            if stat_lanceur < stat_cible:
                return True

        return False

    def concentrer(self, personnage, cible, apprendre=True,
            lattence_min=True, maitrise=None):
        """Fait concentrer le sort à 'personnage'."""
        if maitrise is None:
            maitrise = 100

        if apprendre:
            p_maitrise = personnage.sorts[self.cle]
            if maitrise < 1 or maitrise > p_maitrise:
                maitrise = p_maitrise

        maitrise = Fraction(maitrise)

        if self.cout > personnage.mana:
            personnage << "Vous n'avez pas assez de mana pour lancer ce sort."
            self.dissiper(personnage, maitrise, cible)
            personnage.etats.retirer("magie")
            return

        personnage.mana -= self.cout
        variables = self.get_variables(cible)
        variables["personnage"] = personnage
        variables["maitrise"] = maitrise
        variables["salle"] = personnage.salle
        try:
            self.executer_script(personnage, "concentration", **variables)
        except InterrompreCommande:
            return
        else:
            if apprendre:
                personnage.pratiquer_sort(self.cle)

        action = self.lancer
        if self.echoue(personnage, cible) and apprendre:
            action = self.echouer
        nom_act = "sort_" + self.cle + "_" + personnage.nom
        duree = ceil(self.duree * (100 - maitrise) / 100)
        if lattence_min:
            duree += 2

        importeur.diffact.ajouter_action(nom_act, duree,
                action, personnage, maitrise, cible)

    def echouer(self, personnage, maitrise, cible):
        """Fait rater le sort à personnage."""
        personnage.etats.retirer("magie")
        variables = self.get_variables(cible)
        variables["personnage"] = personnage
        variables["maitrise"] = maitrise
        variables["salle"] = personnage.salle
        self.executer_script(personnage, "echec", **variables)

    def lancer(self, personnage, maitrise, cible):
        """Fait lancer le sort à personnage."""
        dest = personnage.salle
        sorties = []
        personnage.etats.retirer("magie")
        variables = self.get_variables(cible)
        variables["personnage"] = personnage
        variables["maitrise"] = maitrise
        variables["salle"] = personnage.salle
        if hasattr(cible, "salle"):
            dest = cible.salle
            if dest is not personnage.salle:
                chemin = personnage.salle.trouver_chemin(dest)
                if chemin is None:
                    self.dissiper(personnage, maitrise, cible)
                    return

                sorties = chemin.sorties

        self.executer_script(personnage, "lancement", **variables)
        for sortie in sorties:
            origine = sortie.parent
            destination = sortie.salle_dest
            nom_complet = sortie.nom_complet
            t_variables = variables.copy()
            t_variables["salle"] = origine
            t_variables["destination"] = destination
            t_variables["direction"] = nom_complet
            self.executer_script(personnage, "part", **t_variables)
            t_variables = variables.copy()
            t_variables["origine"] = origine
            t_variables["salle"] = destination
            self.executer_script(personnage, "arrive", **t_variables)
        self.toucher(personnage, maitrise, cible)

    def toucher(self, personnage, maitrise, cible):
        """Active les effets du sort."""
        dest = personnage.salle
        if hasattr(cible, "salle"):
            dest = cible.salle

        variables = self.get_variables(cible)
        variables["personnage"] = personnage
        variables["maitrise"] = maitrise
        variables["salle"] = dest
        self.executer_script(personnage, "effet", **variables)
        if self.offensif and self.type_cible == "personnage" and \
                cible.est_vivant():
            cible.reagir_attaque(personnage)
            print(cible, "doit réagir")

    def dissiper(self, personnage, maitrise, cible):
        """Dissipe le sort."""
        variables = self.get_variables(cible)
        variables["personnage"] = personnage
        variables["maitrise"] = maitrise
        variables["salle"] = personnage.salle
        self.executer_script(personnage, "dissipe", **variables)

    def executer_script(self, lanceur, evenement, **variables):
        """Exécute le script passé en paramètre.

        Si une exception InterrompreCommande est levée lors
        du scripting, retire l'état au personnage.

        """
        variables.update({
                "sort": self,
        })

        try:
            self.script[evenement].executer(**variables)
        except InterrompreCommande as err:
            if "magie" in lanceur.etats:
                lanceur.etats.retirer("magie")

            raise err

    def peut_lancer(self, personnage):
        """Le personnage peut-il lancer le sort ?"""
        if personnage.est_immortel():
            return True

        if self.elements and self.elements[0] != personnage.element:
            return False

        if self.cle in personnage.sorts_verrouilles:
            return False

        return True

    def detruire(self):
        """Destruction du sort."""
        BaseObj.detruire(self)
        self.description.detruire()
        self.script.detruire()

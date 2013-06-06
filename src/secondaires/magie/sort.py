# -*-coding:Utf-8 -*

# Copyright (c) 2010 DAVY Guillaume
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
from primaires.format.description import Description
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
        self.type = "destruction"
        self._type_cible = "aucune"
        self.cout = 10
        self.duree = 3
        self.difficulte = 0
        self.distance = False
        self.points_tribut = 1
        self.script = ScriptSort(self)

        # On passe le statut en CONSTRUIT
        self._statut = CONSTRUIT

    def __getnewargs__(self):
        return ("", )

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

    @classmethod
    def get_variables(self, cible=None):
        """Retourne un dictionnaire de variables pré-rempli avec la cible.

        Si la cible est None, le dictionnaire sera vide.

        """
        variables = {}
        if cible is not None:
            variables["cible"] = cible

        return variables

    def echoue(self, personnage):
        """Détermine si personnage réussit ou non à lancer ce sort."""
        maitrise = (100 - personnage.sorts.get(self.cle, 0)) / 100
        difficulte = self.difficulte / 100
        if random() < difficulte * maitrise:
            return True
        return False

    def concentrer(self, personnage, cible, apprendre=True):
        """Fait concentrer le sort à 'personnage'."""
        if self.cout > personnage.mana:
            personnage << "Vous n'avez pas assez de mana pour lancer ce sort."
            self.dissiper(personnage, maitrise)
            personnage.cle_etat = ""
            return

        personnage.mana -= self.cout
        maitrise = 100
        if apprendre:
            maitrise = personnage.pratiquer_sort(self.cle)

        maitrise = Fraction(maitrise)
        variables = self.get_variables(cible)
        variables["personnage"] = personnage
        variables["maitrise"] = maitrise
        variables["salle"] = personnage.salle
        self.script["concentration"].executer(**variables)
        action = self.lancer
        if self.echoue(personnage) and apprendre:
            action = self.echouer
        nom_act = "sort_" + self.cle + "_" + personnage.nom
        duree = ceil(self.duree * (100 - maitrise) / 100)
        importeur.diffact.ajouter_action(nom_act, duree,
                action, personnage, maitrise, cible)

    def echouer(self, personnage, maitrise, cible):
        """Fait rater le sort à personnage."""
        personnage.cle_etat = ""
        variables = self.get_variables(cible)
        variables["personnage"] = personnage
        variables["maitrise"] = maitrise
        variables["salle"] = personnage.salle
        self.script["echec"].executer(**variables)

    def lancer(self, personnage, maitrise, cible):
        """Fait lancer le sort à personnage."""
        dest = personnage.salle
        sorties = []
        personnage.cle_etat = ""
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

        self.script["lancement"].executer(**variables)
        for sortie in sorties:
            origine = sortie.parent
            destination = sortie.salle_dest
            nom_complet = sortie.nom_complet
            t_variables = variables.copy()
            t_variables["salle"] = origine
            t_variables["destination"] = destination
            t_variables["direction"] = nom_complet
            self.script["part"].executer(**t_variables)
            t_variables = variables.copy()
            t_variables["origine"] = origine
            t_variables["salle"] = destination
            self.script["arrive"].executer(**t_variables)
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
        self.script["effet"].executer(**variables)

    def dissiper(self, personnage, maitrise, cible):
        """Dissipe le sort."""
        variables = self.get_variables(cible)
        variables["personnage"] = personnage
        variables["maitrise"] = maitrise
        variables["salle"] = personnage.salle
        self.script["dissipe"].executer(**variables)

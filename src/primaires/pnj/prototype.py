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


"""Ce fichier contient la classe Prototype, détaillée plus bas."""

from collections import OrderedDict

from abstraits.obase import BaseObj
from primaires.format.description import Description
from primaires.perso.stats import Stats
from .script import ScriptPNJ

class Prototype(BaseObj):

    """Classe représentant un prototype de PNJ.

    """

    enregistrer = True
    nom_scripting = "le prototype de PNJ"
    def __init__(self, cle):
        """Constructeur d'un type"""
        BaseObj.__init__(self)
        self.cle = cle
        self._attributs = {}
        self.no = 0 # nombre de PNJ créés sur ce prototype
        self.pnj = []

        # Prototypes
        self.nom_singulier = "quelqu'un"
        self.etat_singulier = "se tient ici"
        self.nom_pluriel = "quelques-uns"
        self.etat_pluriel = "se tiennent ici"
        self.noms_sup = []
        self.description = Description(parent=self)
        self._race = None
        self.genre = "aucun"
        self.stats = Stats(self)
        self.squelette = None
        self.equipement = OrderedDict()
        self.niveau = 1
        self.gain_xp = 0
        self.script = ScriptPNJ(self)
        self.a_depecer = {}
        self.entraine_stats = {}
        self.talents = {}

        # Salles repop
        self.salles_repop = {}

    def __getnewargs__(self):
        return ("", )

    def __repr__(self):
        return "<prototype PNJ '{}'>".format(self.cle)

    def __str__(self):
        return self.cle

    @property
    def nom_race(self):
        """Retourne le nom de la race si existant ou une chaîne vide."""
        return (self.race and self.race.nom) or ""

    @property
    def gain_xp_absolu(self):
        return int(importeur.perso.gen_niveaux.grille_xp[self.niveau - 1][1] \
                * self.gain_xp / 100)

    def _get_race(self):
        return self._race
    def _set_race(self, race):
        self._race = race
        self.squelette = race.squelette
    race = property(_get_race, _set_race)

    def get_nom(self, nombre):
        """Retourne le nom complet en fonction du nombre.
        Par exemple :
        Si nombre == 1 : retourne le nom singulier
        Sinon : retourne le nombre et le nom pluriel

        """
        if nombre <= 0:
            raise ValueError("la fonction get_nom a été appelée avec un " \
                    "nombre négatif ou nul")
        elif nombre == 1:
            return self.nom_singulier
        else:
            if self.noms_sup:
                noms_sup = list(self.noms_sup)
                noms_sup.reverse()
                for nom in noms_sup:
                    if nombre >= nom[0]:
                        return nom[1]
            return str(nombre) + " " + self.nom_pluriel

    def get_nom_etat(self, personnage, nombre):
        """Retourne le nom et l'état en fonction du nombre."""
        nom = self.get_nom(nombre)
        if nombre == 1:
            return nom + " " + self.etat_singulier
        else:
            if self.noms_sup:
                noms_sup = list(self.noms_sup)
                noms_sup.reverse()
                for nom_sup in noms_sup:
                    if nombre >= nom_sup[0]:
                        return nom + " " + nom_sup[2]
            return nom + " " + self.etat_pluriel

    @property
    def genres_possibles(self):
        """Retourne les genres disponibles pour le personnage"""
        if self.race is not None:
            return self.race.genres.str_genres
        else:
            return "masculin, féminin"

    def est_masculin(self):
        """Retourne True si le personnage est masculin, False sinon"""
        if self.race is not None:
            return self.race.genres[self.genre] == "masculin" or \
                    self.genre == "aucun"
        else:
            return self.genre == "masculin" or self.genre == "aucun"

    def est_feminin(self):
        return not self.est_masculin()

    @property
    def nom_squelette(self):
        return self.squelette and self.squelette.nom or "aucun"

    @property
    def cle_squelette(self):
        return self.squelette and self.squelette.cle or "aucun"

    @property
    def nom_etat_singulier(self):
        return self.nom_singulier + " " + self.etat_singulier

    @property
    def str_talents(self):
        if self.talents:
            msg = ""
            for cle_talent, niveau in sorted(self.talents.items()):
                talent = importeur.perso.talents.get(cle_talent)
                if talent is None:
                    continue

                msg += "\n  " + talent.nom.capitalize().ljust(25)
                msg += " : " + str(niveau).rjust(3) + "%"
        else:
            msg = "\n  Aucun"

        return msg

    def est_immortel(self):
        return False

    def detruire(self):
        """Destruction du prototype."""
        for objet, nb in self.a_depecer:
            if self in objet.depecer_de:
                objet.depecer_de.remove(self)

        BaseObj.detruire(self)

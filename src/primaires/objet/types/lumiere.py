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


"""Fichier contenant le type Lumiere."""

from datetime import datetime

from bases.objet.attribut import Attribut
from corps.aleatoire import *
from primaires.interpreteur.editeur.entier import Entier
from primaires.interpreteur.editeur.selection import Selection
from .base import BaseType

# Constantes
TYPES_COMBUSTIBLES = [
        "pierre",
        "foyer",
]

class Lumiere(BaseType):

    """Type d'objet: lumière."""

    nom_type = "lumière"

    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        BaseType.__init__(self, cle)
        self.duree_max = 1
        self.types_combustibles = ["pierre"]
        self.etendre_editeur("x", "durée max", Entier, self, "duree_max", 0)
        self.etendre_editeur("ty", "types de combustibles", Selection,
                self, "types_combustibles", TYPES_COMBUSTIBLES)

        # Attributs propres à l'objet (non au prototype)
        self._attributs = {
            "duree": Attribut(None),
            "allumee_depuis": Attribut(None),
        }

    @property
    def str_types_combustibles(self):
        if self.types_combustibles:
            return ", ".join(sorted(self.types_combustibles))
        else:
            return "Aucun"

    def a_brulee(self):
        """Cette propriété est vraie si la lumière est épuisée."""
        if self.duree_max == 0:
            return False

        duree = getattr(self, "duree", None)
        allumee_depuis = getattr(self, "allumee_depuis", None)

        if duree is None:
            duree = 0

        if allumee_depuis is None:
            allumee_depuis = datetime.now()

        if duree > self.duree_max:
            return True

        actuellement = datetime.now()
        diff = (actuellement - allumee_depuis).total_seconds()
        if duree + diff > self.duree_max:
            return True

        return False

    def etendre_script(self):
        """Extension du scripting."""
        evt_allume = self.script.creer_evenement("allume")
        evt_allume.aide_courte = "le personnage allume l'objet"
        evt_allume.aide_longue = \
            "Cet évènement est appelé quand le personnage allume l'objet " \
            "lumière avec la commande associée. On ne peut pas empêcher " \
            "la commande de s'exécuter dans ce script mais on peut " \
            "traiter certains cas et éventuellement forcer l'objet " \
            "à s'éteindre de nouveau."
        var_perso = evt_allume.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage allumant l'objet"
        var_objet = evt_allume.ajouter_variable("objet", "Objet")
        var_objet.aide = "l'objet allumé"

        evt_eteint = self.script.creer_evenement("éteint")
        evt_eteint.aide_courte = "le personnage éteint l'objet"
        evt_eteint.aide_longue = \
            "Cet évènement est appelé quand le personnage éteint l'objet " \
            "lumière avec la commande associée. On ne peut pas empêcher " \
            "la commande de s'exécuter dans ce script. Notez que " \
            "l'objet est automatiquement éteint quand le combustible " \
            "s'épuise, ce qui appelle aussi ce script. Notez que " \
            "dans ce cas, la variable personnage peut être nulle " \
            "(la lumière peut être posée à terre, par exemple). Testez " \
            "si le personnage existe (si personnage:) avant de lui " \
            "envoyer un message."
        var_perso = evt_eteint.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage éteignant l'objet"
        var_objet = evt_eteint.ajouter_variable("objet", "Objet")
        var_objet.aide = "l'objet éteint"

    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes"""
        duree_max = enveloppes["x"]
        duree_max.apercu = "{objet.duree_max} minute(s)"
        duree_max.prompt = "Durée de vie maximum de la lumière en minutes : "
        duree_max.aide_courte = \
            "Entrez la |ent|durée maximum|ff| en minutes de la lumière " \
            "ou bien\n|cmd|/|ff| pour revenir à la fenêtre parente.\n\n" \
            "Vous pouvez préciser une durée de |ent|0|ff| pour indiquer " \
            "que la lumière\nsera infinie.\n\nDurée maximum actuelle : " \
            "{objet.duree_max} minute(s)"

        types = enveloppes["ty"]
        types.apercu = "{objet.str_types_combustibles}"
        types.prompt = "Type de combustible à ajouter ou supprimer : "
        types.aide_courte = \
            "Entrez un |ent|type de combustible|ff| de la lumière " \
            "pour l'ajouter ou le supprimer, ou bien\n|cmd|/|ff| pour " \
            "revenir à la fenêtre parente.\n\nLes types de combustible " \
            "déterminent les objets nécessaires pour\nallumer la " \
            "lumière. Si le type choisi est |cmd|pierre|ff|, cela\nsignifie " \
            "qu'une pierre à feu est nécessaire pour allumer la lumière. " \
            "Si\nc'est le type |cmd|foyer|ff| qui est choisi, cela " \
            "signifie qu'un feu doit\nêtre présent dans la salle (soit " \
            "un feu de camp soit une cheminée).\nIl est possible d'avoir " \
            "une lumière sans aucun type, dans ce cas aucun\nobjet " \
            "n'est nécessaire pour l'allumer, ou bien d'avoir une " \
            "lumière\npossédant plusieurs types possibles.\n\n" \
            "Types actuels : {objet.str_types_combustibles}"

    def nettoyage_cyclique(self):
        """Nettoyage cyclique de la lumière."""
        if not self.a_brulee():
            return

        parent = self.grand_parent
        from primaires.perso.personnage import Personnage
        if isinstance(parent, Personnage):
            self.script["éteint"].executer(objet=self, personnage=parent)
            self.allumee_depuis = None

# -*-coding:Utf-8 -*

# Copyright (c) 2013 LE GOFF Vincent
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


"""Package contenant l'éditeur 'affedit'.

Si des redéfinitions de contexte-éditeur standard doivent être faites, elles
seront placées dans ce package

Note importante : ce package contient la définition d'un éditeur, mais
celui-ci peut très bien être étendu par d'autres modules. Au quel cas,
les extensions n'apparaîtront pas ici.

"""

from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.flag import Flag
from primaires.interpreteur.editeur.entier import Entier
from primaires.interpreteur.editeur.uniligne import Uniligne
from primaires.scripting.editeurs.edt_script import EdtScript

class EdtAffedit(Presentation):

    """Classe définissant l'éditeur d'affection 'affedit'.

    """

    nom = "affedit"

    def __init__(self, personnage, affection):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None

        Presentation.__init__(self, instance_connexion, affection)
        if personnage and affection:
            self.construire(affection)

    def __getnewargs__(self):
        return (None, None)

    def construire(self, affection):
        """Construction de l'éditeur"""
        # Résumé
        resume = self.ajouter_choix("résumé", "r", Uniligne, affection,
                "resume")
        resume.parent = self
        resume.apercu = "{objet.resume}"
        resume.prompt = "Entrez le résumé de l'affection : "
        resume.aide_courte = \
            "Entrez |ent|le résumé|ff| de l'affection.\n\nrésumé actuel : " \
            "{objet.resume}"

        # Durée d'un tick en secondes
        duree_tick = self.ajouter_choix("durée d'un tick en secondes",
                "t", Entier, affection, "duree_tick")
        duree_tick.parent = self
        duree_tick.apercu = "{objet.duree_tick} seconde(s)"
        duree_tick.prompt = "Entrez la durée d'un tick de l'affection : "
        duree_tick.aide_courte = \
            "Entrez |ent|la durée d'un tick en secondes|ff| de " \
            "l'affection.\n\nDurée actuelle : {objet.duree_tick}"

        # Durée max
        duree_max = self.ajouter_choix("durée maximum", "x", Entier,
                affection, "duree_max_en_ticks", None)
        duree_max.parent = self
        duree_max.apercu = "{objet.aff_duree_max_en_ticks}"
        duree_max.prompt = "Entrez la durée max de l'affection en ticks : "
        duree_max.aide_courte = \
            "Entrez |ent|la durée max en ticks|ff| de l'affection.\n\n" \
            "La durée maximum doit être donnée en ticks. Si par " \
            "exemple la durée d'un tick\n" \
            "est de 5 secondes, alors donner une durée maximum de 20 " \
            "ticks fera une affection qui\n" \
            "durera 100 secondes au maximum.\n" \
            "Si la durée max est inférieure à 1, alors il n'y a " \
            "pas de limite.\n\n" \
            "Durée maximum actuelle : {objet.aff_duree_max_en_ticks}"

        # Infinie
        infinie = self.ajouter_choix("infinie", "inf", Flag, affection,
                "infinie")
        infinie.parent = self

        # Variation
        variation = self.ajouter_choix("variation", "v", Entier, affection,
                "variation", None)
        variation.parent = self
        variation.apercu = "{objet.variation}"
        variation.prompt = "Entrez la variation de l'affection : "
        variation.aide_courte = \
            "Entrez |ent|la variation|ff| de l'affection.\n\n" \
            "Si la variation est supérieure à 0, alors quand la durée\n" \
            "de l'affection diminue la force augmente, cela de plus en\n" \
            "plus. Si au contraire la variation est inférieure à 0, alors\n" \
            "la force diminue avec la durée. Enfin si la variation est\n" \
            "nulle, la durée diminue mais la force ne change pas.\n\n" \
            "Variation actuelle : {objet.variation}"

        # Script
        scripts = self.ajouter_choix("scripts", "sc", EdtScript,
                affection.script)
        scripts.parent = self

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


"""Fichier contenant le type Nourriture."""

from bases.objet.attribut import Attribut
from corps.aleatoire import *
from primaires.interpreteur.editeur.uniligne import Uniligne
from primaires.interpreteur.editeur.entier import Entier
from .base import BaseType

class Nourriture(BaseType):

    """Type d'objet: nourriture.

    """

    nom_type = "nourriture"

    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        BaseType.__init__(self, cle)
        self.qualite = 1
        self.nourrissant = 1
        self.message_mange = "Vous mangez {}.".format(self.nom_singulier)
        self.etendre_editeur("a", "qualité", Entier, self, "qualite", 1, 10)
        self.etendre_editeur("o", "nourrissant", Entier, self, "nourrissant",
                1, 10)
        self.etendre_editeur("m", "message d'ingestion", Uniligne, self,
                "message_mange")

    def etendre_script(self):
        """Extension du scripting."""
        evt_mange = self.script.creer_evenement("mange")
        evt_mange.aide_courte = "le personnage mange l'objet"
        evt_mange.aide_longue = \
            "Cet évènement est appelé quand le personnage mange l'objet."
        var_perso = evt_mange.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage mangeant l'objet"
        var_objet = evt_mange.ajouter_variable("objet", "Objet")
        var_objet.aide = "l'objet mangé"

    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes"""
        qualite = enveloppes["a"]
        qualite.apercu = "{objet.qualite}"
        qualite.prompt = "Qualité de la nourriture : "
        qualite.aide_courte = \
            "Entrez la |ent|qualité|ff| de la nourriture, entre |cmd|1|ff| " \
            "et |cmd|10|ff|\nou |cmd|/|ff| pour revenir à la fenêtre " \
            "parente.\n\n" \
            "Qualité actuelle : {objet.qualite}"

        nourrissant = enveloppes["o"]
        nourrissant.apercu = "{objet.nourrissant}"
        nourrissant.prompt = "Valeur nourrissante : "
        nourrissant.aide_courte = \
            "Entrez la |ent|valeur nourrissante|ff| de la nourriture, entre " \
            "|cmd|1|ff| et |cmd|10|ff|\nou |cmd|/|ff| pour revenir à la " \
            "fenêtre parente.\n\n" \
            "Valeur nourrissante actuelle : {objet.nourrissant}"

        message_mange = enveloppes["m"]
        message_mange.prompt = "Message lors de l'ingestion : "
        message_mange.aide_courte = \
            "Entrez le |ent|texte|ff| affiché au joueur lorsqu'il mange la nourriture ou |cmd|/|ff| pour revenir à la " \
            "fenêtre parente.\n\n" \
            "Message présent : {objet.message_mange}"

    def veut_jeter(self, personnage, sur):
        """Le personnage veut jeter l'objet sur sur."""
        from primaires.perso.personnage import Personnage
        if not isinstance(sur, Personnage):
            return ""

        return "jeter_personnage"

    def jeter(self, personnage, elt):
        """Jète la nourriture sur un élément."""
        fact = varier(personnage.agilite, 20) / 100
        fact *= (1.6 - personnage.poids / personnage.poids_max)
        fact_adv = varier(elt.agilite, 20) / 100
        fact_adv *= (1.6 - elt.poids / elt.poids_max)
        reussite = fact >= fact_adv
        if reussite:
            personnage.envoyer("Vous lancez {} sur {{}}.".format(
                    self.get_nom()), elt)
            elt.envoyer("{{}} lance {} droit sur vous.".format(
                    self.get_nom()), personnage)
            personnage.salle.envoyer("{{}} envoie {} sur {{}}.".format(
                    self.get_nom()), personnage, elt)
        else:
            personnage.envoyer("Vous lancez {} mais manquez {{}}.".format(
                    self.get_nom()), elt)
            elt.envoyer("{{}} lance {} mais vous manque.".format(
                    self.get_nom()), personnage)
            personnage.salle.envoyer("{{}} envoie {} mais manque {{}}.".format(
                    self.get_nom()), personnage, elt)

        personnage.salle.objets_sol.ajouter(self)
        return reussite

    def jeter_personnage(self, personnage, cible):
        """Jète la nourriture sur un personnage."""
        pass

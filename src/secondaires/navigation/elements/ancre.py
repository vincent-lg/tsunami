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


"""Fichier contenant la classe Ancre, détaillée plus bas."""

from bases.objet.attribut import Attribut
from primaires.interpreteur.editeur.entier import Entier
from secondaires.navigation.constantes import *
from .base import BaseElement

class Ancre(BaseElement):

    """Classe représentant une ancre.

    """

    nom_type = "ancre"

    def __init__(self, cle=""):
        """Constructeur d'un type"""
        BaseElement.__init__(self, cle)
        self.longueur = 8
        self.nb_lever = 1

        # Attributs propres aux ancres
        self._attributs = {
            "jetee": Attribut(lambda: False),
        }

    def editer(self, presentation):
        """Édition de l'ancre."""
        # Longueur
        longueur = presentation.ajouter_choix("longueur de l'ancre", None,
                Entier, self, "longueur")
        longueur.apercu = "{valeur} brasse(s)"
        longueur.prompt = "Longueur de l'ancre : "
        longueur.aider("""
            Entrez |ent|la longueur|ff| de l'ancre ou |cmd|/|ff| pour
            revenir à la fenêtre parente.

            La longueur de l'ancre, précisée en brasses, correspond à
            la profondeur de l'étendue. Il est improbable qu'elle soit
            inféireure à 3 brasses. Si le navire portant l'ancre est à
            moins de 3 brasses d'une côte (une salle accostable), la
            profondeur à cet endroit sera toujours de 3 brasses. Si il
            est éloigné d'une trentaine de brasses de toute salle accostable,
            la profondeur tombe à 10 brasses. Ensuite, la profondeur descend
            progressivement jusqu'à atteindre la profondeur maximum
            de l'étendue, telle que définie dans l'éditeur d'étendue.

            Longueur actuelle : {valeur} brasses
        """)

        # Nombre de joueurs
        nb_lever = presentation.ajouter_choix(
                "nombre de matelots pour lever l'ancre", None, Entier,
                self, "nb_lever")
        nb_lever.prompt = "Nombre de matelots nécessaires pour lever l'ancre : "
        nb_lever.aider("""
            Entrez |cmd|/|ff| pour revenir à la fenêtre parente ou |ent|le
            nombre de matelots|ff| nécessaires pour lever l'ancre.

            Les petites ancres n'ont besoin que d'un seul matelot pour
            lever l'ancre. Les ancres plus longues et lourdes pourraient
            avoir besoin de plusieurs matelots qui poussent au cabestan.
            Précisez ici le nombre de matelots nécessaires pour lever l'ancre.

            Nombre de matelots actuel : {valeur}
        """)

    def get_description_ligne(self, personnage):
        """Retourne une description d'une ligne de l'élément."""
        if self.jetee:
            return "L'ancre est jetée."
        else:
            return "La chaîne de l'ancre est enroulée sur le pont."

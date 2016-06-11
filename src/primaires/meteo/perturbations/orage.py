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


"""Ce fichier contient la classe Orage, détaillée plus bas."""

from .base import *

class Orage(BasePertu):

    """Classe abstraite représentant la perturbation 'orage'.

    """

    nom_pertu = "orage"
    rayon_max = 13
    duree_max = 7
    origine = False
    attributs = ("averse", "noir", "nuage", "tiède", "humide", "tempête")

    def __init__(self, pos):
        """Constructeur de la perturbation"""
        BasePertu.__init__(self, pos)
        self.flags = OPAQUE
        self.alea_dir = 7
        self.etat = [
            (5, "Le ciel est noir, zébré d'éclairs, et la pluie tombe dru."),
            (10, "Une violente pluie tombe du ciel, devenant franchement " \
                    "orageuse non loin."),
        ]
        self.message_debut = "Un violent orage éclate au-dessus de votre " \
                "tête."
        self.message_fin = "L'orage s'évanouit comme il a commencé, " \
                "laissant l'air moite et pesant."
        self.message_entrer = "Un orage puissant venant {dir} obscurcit le " \
                "ciel et déverse sa colère."
        self.message_sortir = "Les nuages d'orage s'éloignent vers {dir}, " \
                "laissant le sol détrempé."
        self.fins_possibles = [
            ("pluie", "L'orage se calme peu à peu et laisse place à une " \
                    "pluie agréable.", 23),
        ]

    def action_cycle(self, salles):
        """Définit une ou plusieurs actions effectuées à chaque cycle."""
        messages = [
            "La foudre frappe le sol dans un vacarme infernal !",
            "Un éclair aveuglant zèbre le ciel obscur.",
            "Un roulement de tonnerre, puissant et impérieux, vous fait " \
                    "sursauter.",
            "Soudain, le vent redouble de fureur, et les gouttes vous " \
                    "fouettent violemment."
        ]
        for salle in salles:
            if randint(1, 10) < 3 and salle.exterieur:
                salle.envoyer(choice(messages), prompt=False)

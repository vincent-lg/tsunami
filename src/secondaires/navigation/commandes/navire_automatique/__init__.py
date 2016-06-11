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


"""Package contenant la commande 'navire_automatique'."""

from primaires.interpreteur.commande.commande import Commande
from .apparaitre import PrmApparaitre
from .editer import PrmEditer


class CmdNavireAutomatique(Commande):

    """Commande 'navire_automatique'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "autonavire", "autoship")
        self.groupe = "administrateur"
        self.nom_categorie = "navire"
        self.aide_courte = "manipule les navires automatiques"
        self.aide_longue = \
            "Cette commande permet de créer, éditer et lister les " \
            "navires automatiques. Un navire automatique est une fiche " \
            "décrivant les propriétés semi-aléatoires d'un navire " \
            "automatique, par exemple un navire pirate. Un navire " \
            "automatique a au minimum un modèle de navire, une liste " \
            "de noms, de caps à emprunter, une description d'équipage " \
            "et de cale. Quand on veut créer un navire depuis une " \
            "fiche de navire automatique, le modèle de navire est " \
            "utilisé. Le navire créé est placé sur le cap choisi, " \
            "son équipage est constitué automatiquement ainsi que " \
            "sa cale remplit. Il aura le comportement et la stratégie " \
            "sélectionné."

    def ajouter_parametres(self):
        """Ajout des paramètres."""
        self.ajouter_parametre(PrmApparaitre())
        self.ajouter_parametre(PrmEditer())

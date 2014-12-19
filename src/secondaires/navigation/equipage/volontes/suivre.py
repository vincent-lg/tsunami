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


"""Fichier contenant la volonté Suivre."""

import re

from corps.fonctions import lisser
from primaires.format.fonctions import contient
from secondaires.navigation.equipage.volontes.tirer import Tirer
from secondaires.navigation.equipage.volonte import Volonte

class Suivre(Volonte):

    """Classe représentant une volonté.

    Cette volonté demande au navire cible de suivre le navire courant.
    Le personnage utilisant l'ordre doit avoir le droit de donner
    des objectifs au navire cible. Cette volonté est des plus utile
    pour ramener sa prise au port ainsi que son autre navire.

    """

    cle = "suivre"
    ordre_court = re.compile(r"^s\s+(.*)$", re.I)
    ordre_long = re.compile(r"^suivre\s+(.*)$", re.I)

    def __init__(self, navire, cible=None):
        """Construit une volonté."""
        Volonte.__init__(self, navire)
        self.cible = cible

    @property
    def arguments(self):
        """Propriété à redéfinir si la volonté comprend des arguments."""
        return (self.cible, )

    def choisir_matelots(self, exception=None):
        """Retourne le matelot le plus apte à accomplir la volonté."""
        return None

    def executer(self, matelot):
        """Exécute la volonté."""
        # Vérifie que l'initiateur a le droit de commander à la cible
        cible = self.cible
        personnage = self.initiateur
        if personnage is None:
            print("Aucun initiateur")
            return

        if (self.navire.opt_position - cible.opt_position).mag > 20:
            personnage << "|err|Ce navire se trouve trop loin.|ff|"
            return

        if not cible.a_le_droit(personnage, "officier"):
            personnage << "|err|Vous ne pouvez donner d'ordre sur ce " \
                    "navire.|ff|"
            return

        if cible.equipage.a_objectif("suivre_navire", self.navire):
            personnage << "|err|Ce semble être déjà le cas.|ff|"
            return

        cible.equipage.ajouter_objectif("suivre_navire", self.navire)
        if cible.equipage.matelots:
            self.navire.envoyer(lisser("L'équipage de {} fait signe " \
                    "en réponse.".format(cible.desc_survol)))

    def crier_ordres(self, personnage):
        """On fait crier l'ordre au personnage."""
        cible = self.cible
        msg = "{} s'écrie : envoyez le signal à {}, suivez-nous !".format(
                personnage.distinction_audible, cible.desc_survol)
        self.navire.envoyer(msg)

    @classmethod
    def extraire_arguments(cls, navire, nom_navire):
        """Extrait les arguments de la volonté."""
        for navire in Tirer.trouver_navires(navire):
            if contient(navire.desc_survol, nom_navire):
                return (navire, )

        raise ValueError("Le navire {} n'est pas en vue.".format(
                nom_navire))

# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
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


"""Fichier contenant le type Projectile."""

from .arme import Arme

class Projectile(Arme):

    """Type d'objet: projectile.

    """

    nom_type = "projectile"

    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        Arme.__init__(self, cle)
        self.peut_depecer = False
        self.emplacement = ""
        self.positions = ()

    def etendre_script(self):
        """Extension du scripting."""
        # Évènement atteint
        evt_atteint = self.script.creer_evenement("atteint")
        evt_atteint.aide_courte = "le projectile atteint une cible"
        evt_atteint.aide_longue = \
            "Cet évènement est appelé quand le projectile vient " \
            "d'atteindre une cible (juste après les messages informant " \
            "des dégâts éventuels). Il peut être utile pour par " \
            "exemple placer une affection sur la cible."
        var_auteur = evt_atteint.ajouter_variable("auteur", "Personnage")
        var_auteur.aide = "le personnage à l'auteur du tir"
        var_cible = evt_atteint.ajouter_variable("cible", "Personnage")
        var_cible.aide = "la cible atteinte par le projectile"
        var_arme = evt_atteint.ajouter_variable("arme", "Objet")
        var_arme.aide = "l'arme de jet à l'origine du tir"
        var_projectile = evt_atteint.ajouter_variable("projectile", "Objet")
        var_projectile.aide = "le projectile qui atteint la cible"

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


"""Fichier contenant le type boulet de canon."""

from primaires.interpreteur.editeur.flottant import Flottant
from primaires.objet.types.base import BaseType

class Boulet(BaseType):
    
    """Type d'objet: boulet de canon.
    
    """
    
    nom_type = "boulet de canon"
    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        BaseType.__init__(self, cle)
        self.degats = 50
        self.etendre_editeur("ts", "dégâts", Flottant,
                self, "degats", "kg")
    
    def etendre_script(self):
        """Extension du scripting."""
        evt_atteint = self.script.creer_evenement("atteint")
        evt_atteint.aide_courte = "le boulet atteint sa cible"
        evt_atteint.aide_longue = \
            "Cet évènement est appelé quand le boulet, après avoir " \
            "été tiré, atteint sa cible, si c'est une salle. Notez " \
            "qu'un boulet peut aussi atteindre l'eau ou bien un obstacle " \
            "(comme une falaise), auquel cas l'évènement n'est pas " \
            "appelé. La salle de cible peut être soit sur un navire, " \
            "soit sur la terre ferme."
        var_objet = evt_atteint.ajouter_variable("objet", "Objet")
        var_objet.aide = "le boulet-même"
        var_salle = evt_atteint.ajouter_variable("salle", "Salle")
        var_salle.aide = "la salle cible atteinte par le boulet"
    
    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes"""
        degats = enveloppes["ts"]
        degats.apercu = "{objet.degats}"
        degats.prompt = "Dégâts infligés par le boulet de canon : "
        degats.aide_courte = \
            "Entrez les |ent|dégâts|ff| infligés " \
            "par le boulet.\n" \
            "Entrez |cmd|/|ff| pour revenir à la fenêtre " \
            "parente.\n\n" \
            "Dégâts actuels : {objet.degats}"
